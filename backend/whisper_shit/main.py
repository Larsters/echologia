import os
from collections import Counter, defaultdict
from typing import Any

from pyannote.audio import Pipeline as PyannotePipeline

def diarize_with_pyannote(audio_file: str, num_speakers: int | None = None):
    """
    Robust speaker diarization using pyannote/speaker-diarization-3.1.
    Requires a Hugging Face token in env: HUGGINGFACE_TOKEN or HF_TOKEN.
    Returns a list of dicts: {"start": float, "end": float, "speaker_id": "SPEAKER_00X"}.
    """
    hf_token = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("Set HUGGINGFACE_TOKEN or HF_TOKEN for pyannote diarization.")

    pipeline = PyannotePipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token
    )
    # Let it infer num speakers unless explicitly provided
    diar = pipeline(audio_file, num_speakers=num_speakers)

    # Build normalized segments with consistent spk labels
    raw = []
    for turn, _, speaker in diar.itertracks(yield_label=True):
        raw.append({
            "start": float(turn.start),
            "end": float(turn.end),
            "speaker_id": speaker
        })

    # Map pyannote labels (e.g., "SPEAKER_00", "SPEAKER_01") deterministically to spk_01... by first occurrence
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
    change_points = sorted({s["start"] for s in diar_segments} | {s["end"] for s in diar_segments})
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

def process_audio_to_personas(audio_file: str, info: Any):
    # 1. Run ASR and get segments
    segments = info.segments

    # 2. (previously) Extract personas from segments - REMOVED

    # 3. Diarize with pyannote (robust)
    diar_segments = diarize_with_pyannote(audio_file)

    # 4. Assign speakers to ASR segments by max-overlap
    asr_with_spk = assign_speakers_by_overlap(segments, diar_segments)

    # 5. Compute fair speaking times from diarization (handles overlaps)
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

    # 7. Create final segments with speaker assignment (for timeline)
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

    meta = {
        "model_asr": info.model_name,
        "model_diarization": "pyannote/speaker-diarization-3.1",
        "audio_file": audio_file,
        "language": info.language,
    }

    return personas, processed_segments, meta