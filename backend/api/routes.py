from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import sys
from pathlib import Path
import shutil
from typing import Dict, Any

# Add whisper_shit to path
sys.path.insert(0, str(Path(__file__).parent.parent / "whisper_shit"))

from processor import (
    process_audio_to_personas,
    transcribe_audio_simple,
    diarize_with_pyannote
)

router = APIRouter(prefix="/api/audio", tags=["audio"])

# Directory for uploaded files
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/process")
async def process_audio(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Complete audio processing pipeline: transcription + diarization + persona extraction
    
    Returns:
        JSON with segments, personas, age/gender, and speaker names
    """
    # Validate file type
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Supported: mp3, wav, m4a, flac, ogg"
        )
    
    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the audio
        result = process_audio_to_personas(str(file_path))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if file_path.exists():
            file_path.unlink()


@router.post("/transcribe")
async def transcribe_only(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Transcription only (no diarization or persona extraction)
    
    Returns:
        Transcription segments with timestamps
    """
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Supported: mp3, wav, m4a, flac, ogg"
        )
    
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        segments, info = transcribe_audio_simple(str(file_path))
        
        return {
            "language": info.language,
            "segments": segments,
            "total_segments": len(segments)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    
    finally:
        if file_path.exists():
            file_path.unlink()


@router.post("/diarize")
async def diarize_only(file: UploadFile = File(...), num_speakers: int = 2) -> Dict[str, Any]:
    """
    Speaker diarization only (who spoke when)
    
    Args:
        num_speakers: Expected number of speakers (default: 2)
    
    Returns:
        Speaker segments with timestamps
    """
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Supported: mp3, wav, m4a, flac, ogg"
        )
    
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        diar_segments = diarize_with_pyannote(str(file_path), num_speakers=num_speakers)
        
        # Calculate speaking times
        speaker_times = {}
        for seg in diar_segments:
            spk = seg["speaker_id"]
            duration = seg["end"] - seg["start"]
            speaker_times[spk] = speaker_times.get(spk, 0) + duration
        
        return {
            "segments": diar_segments,
            "speaker_times": speaker_times,
            "num_speakers": len(speaker_times)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diarization failed: {str(e)}")
    
    finally:
        if file_path.exists():
            file_path.unlink()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "audio-processing-api"}