import json
import torch
import librosa
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime
from faster_whisper import WhisperModel
import os
from huggingface_hub import login
from pyannote.audio import Pipeline as PyannotePipeline
from dotenv import load_dotenv
from llm_populate_entries import extract_speaker_names_with_llm
from age_gender_estimation import estimate_age_gender_for_personas
from background_noise_classifier import get_session_background_summary

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

def transcribe_audio_simple(audio_file="test-audio.mp3"):
    """
    Simple transcription using faster-whisper
    """
    print("🔊 Loading Whisper model...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    
    print("📝 Transcribing audio...")
    segments, info = model.transcribe(audio_file, beam_size=5)
    
    print(f"✅ Detected language: {info.language}")
    
    # Convert segments to list for processing
    transcription_segments = []
    for segment in segments:
        transcription_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "confidence": segment.avg_logprob if hasattr(segment, 'avg_logprob') else 0.9
        })
    
    return transcription_segments, info

def diarize_with_pyannote(audio_file: str, num_speakers: int | None = None):
    """
    Robust speaker diarization using pyannote/speaker-diarization-3.1.
    Preloads audio to avoid tensor size mismatches.
    Returns a list of dicts: {"start": float, "end": float, "speaker_id": "SPEAKER_00X"}.
    """
    hf_token = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("Set HUGGINGFACE_TOKEN or HF_TOKEN for pyannote diarization.")

    login(token=hf_token, add_to_git_credential=False)

    pipeline = PyannotePipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1"
    )
    
    # Preload audio to avoid PyAnnote's internal loading issues
    print("🎵 Loading audio for diarization...")
    waveform, sample_rate = librosa.load(audio_file, sr=16000, mono=True)
    waveform = torch.from_numpy(waveform).unsqueeze(0)  # Shape: [1, samples]
    
    # Pass preloaded waveform instead of file path
    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate}, num_speakers=2)

    # Build normalized segments with consistent spk labels
    raw = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        raw.append({
            "start": float(turn.start),
            "end": float(turn.end),
            "speaker_id": speaker
        })

    # Map pyannote labels to spk_01, spk_02, etc.
    spk_order = []
    label_map = {}
    norm = []
    for seg in sorted(raw, key=lambda s: (s["start"], s["end"])):
        spk = seg["speaker_id"]
        if spk not in label_map:
            spk_order.append(spk)
            label_map[spk] = f"spk_{len(spk_order):02d}"
        norm.append({"start": seg["start"], "end": seg["end"], "speaker_id": label_map[spk]})
    return norm

def assign_speakers_by_overlap(asr_segments: list[dict], diar_segments: list[dict]) -> list[dict]:
    """
    For each ASR segment, assign the speaker_id of the diarization segment with max temporal overlap.
    Returns a new list of ASR segments with "speaker_id" attached.
    """
    assigned = []
    for a in asr_segments:
        a_start, a_end = float(a["start"]), float(a["end"])
        best_spk = "spk_01"
        best_ov = 0.0
        for d in diar_segments:
            ov = max(0.0, min(a_end, d["end"]) - max(a_start, d["start"]))
            if ov > best_ov:
                best_ov = ov
                best_spk = d["speaker_id"]
        new_seg = dict(a)
        new_seg["speaker_id"] = best_spk
        assigned.append(new_seg)
    return assigned

def speaking_time_fair(diar_segments: list[dict]) -> dict:
    """
    Compute per-speaker talk time with fair apportioning of overlaps.
    Returns dict {speaker_id: seconds}.
    """
    if not diar_segments:
        return {}
    change_points = sorted(
        {s["start"] for s in diar_segments} | {s["end"] for s in diar_segments}
    )
    talk = {}
    for i in range(len(change_points) - 1):
        a, b = change_points[i], change_points[i + 1]
        if b <= a:
            continue
        active = {s["speaker_id"] for s in diar_segments if s["start"] < b and s["end"] > a}
        if not active:
            continue
        share = (b - a) / len(active)
        for spk in active:
            talk[spk] = talk.get(spk, 0.0) + share
    return {k: float(v) for k, v in talk.items()}

def process_audio_to_personas(audio_file="test-audio.mp3"):
    """
    Complete pipeline: transcribe -> diarize -> extract personas -> output JSON
    """
    print("🚀 Starting audio processing pipeline...")
    
    # 1. Transcribe
    segments, info = transcribe_audio_simple(audio_file)
    
    # 2. Load audio at 16kHz (required for age/gender model)
    try:
        audio, sr = librosa.load(audio_file, sr=16000)
        total_duration = len(audio) / sr
        print(f"📊 Audio duration: {total_duration:.1f} seconds")
    except Exception as e:
        print(f"⚠️  Could not load audio for duration: {e}")
        total_duration = segments[-1]["end"] if segments else 0
    
    # 3. Diarize with pyannote
    diar_segments = diarize_with_pyannote(audio_file)

    # 4. Assign speakers to ASR segments by max-overlap
    asr_with_spk = assign_speakers_by_overlap(segments, diar_segments)

    # 5. Compute fair speaking times from diarization
    talk_times = speaking_time_fair(diar_segments)

    # 6. Aggregate per-speaker stats
    personas = []
    lang_counts = defaultdict(Counter)
    for seg in asr_with_spk:
        lang_counts[seg["speaker_id"]][info.language or "und"] += 1

    total_talk = sum(talk_times.values()) or 1.0
    for spk, t in sorted(talk_times.items(), key=lambda kv: kv[1], reverse=True):
        counts = lang_counts[spk]
        denom = sum(counts.values()) or 1
        languages = {k: round(v / denom, 3) for k, v in counts.items()}
        personas.append({
            "speaker_id": spk,
            "speaking_time_sec": round(t, 2),
            "speaking_percent": round(100.0 * t / total_talk, 2),
            "languages": languages or {info.language: 1.0},
            "sex": {"label": "unknown", "confidence": 0.5},
            "age": {"label": "unknown", "mean_estimate": 30, "confidence": 0.5},  
            "mood_summary": {"dominant": "neutral"}
        })

    # 7. Estimate age and gender for each persona
    try:
        personas = estimate_age_gender_for_personas(audio, sr, diar_segments, personas)
        print("✅ Age and gender estimation completed")
    except Exception as e:
        print(f"⚠️ Age and gender estimation failed: {e}")

    # 8. Classify background audio
    background_audio = {}
    try:
        print("🎵 Analyzing background audio...")
        background_audio = get_session_background_summary(audio, sr, max_audio_length_sec=30, top_k=5)
        print("✅ Background audio classification completed")
    except Exception as e:
        print(f"⚠️ Background audio classification failed: {e}")
        background_audio = {"dominant_classes": []}

    # 9. Create final segments with speaker assignment
    processed_segments = []
    for seg in asr_with_spk:
        processed_segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "speaker_id": seg["speaker_id"],
            "text": seg["text"],
            "language": info.language,
            "emotion": {"label": "neutral", "confidence": 0.8}
        })

    processed_segments.sort(key=lambda x: x["start"])

    # 10. Create output structure
    output = {
        "session_id": f"session_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}",
        "meta": {
            "duration_sec": round(total_duration, 1),
            "sampling_rate": 16000,
            "model_asr": "faster-whisper-base",
            "model_diarization": "pyannote/speaker-diarization-3.1",
            "model_age_gender": "audeering/wav2vec2-large-robust-24-ft-age-gender",
            "model_background_classification": "MIT/ast-finetuned-audioset-10-10-0.4593",
            "date_processed": datetime.now().isoformat() + "Z"
        },
        "segments": processed_segments,
        "personas": personas,
        "hierarchy": sorted(personas, key=lambda x: x["speaking_time_sec"], reverse=True),
        "background_audio": background_audio,
        "global_emotion_trend": {"neutral": 1.0}
    }
    
    # 11. Use LLM to extract speaker names
    print("\n🤖 Using LLM to extract speaker names...")
    output["personas"] = extract_speaker_names_with_llm(processed_segments, output["personas"])
    output["hierarchy"] = sorted(output["personas"], key=lambda x: x["speaking_time_sec"], reverse=True)

    return output