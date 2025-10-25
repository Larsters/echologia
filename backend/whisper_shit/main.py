import whisperx
import torch
import json
from datetime import datetime

def transcribe_and_diarize(audio_file="test-audio.mp3"):
    """
    Complete transcription and diarization pipeline using WhisperX
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    print(f"Using device: {device}")
    
    # 1. Load audio
    audio = whisperx.load_audio(audio_file)
    
    # 2. Load ASR model
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)
    
    # 3. Transcribe with Whisper
    result = model.transcribe(audio, batch_size=16)
    print(f"Detected language: {result['language']}")
    
    # 4. Load alignment model
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    
    # 5. Align whisper output
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    # 6. Load diarization model (requires HuggingFace token)
    # You'll need to set HF_TOKEN environment variable or pass token here
    try:
        diarize_model = whisperx.DiarizationPipeline(use_auth_token="YOUR_HF_TOKEN", device=device)
        
        # 7. Diarize
        diarize_segments = diarize_model(audio)
        
        # 8. Assign speaker labels
        result = whisperx.assign_word_speakers(diarize_segments, result)
        
    except Exception as e:
        print(f"Diarization failed: {e}")
        print("Continuing without speaker assignment...")
        # Add default speaker for segments without speaker info
        for segment in result["segments"]:
            if "speaker" not in segment:
                segment["speaker"] = "spk_01"
    
    return result, audio

if __name__ == "__main__":
    # Test the transcription
    result, audio = transcribe_and_diarize()
    
    # Save raw result for processing
    with open("raw_transcription.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("Transcription completed. Check raw_transcription.json")
    print(f"Found {len(result['segments'])} segments")