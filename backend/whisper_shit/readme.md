# Structure:
## 1. Input & Cleanup
- Load audio -> resample to standard 16kHz -> normalize
- Denoise, deverb (mb pyannote/audio denoiser)

## 2. Voice Activity Detection (VAD)
- pyannote VAD to find speech regions. Reducing Whisper compute time and improving transcription accuracy.

## 3. ASR (Automatic Speech Recognition) 
- WhisperX on only the detected speech segments: timestamps + alignment
- language ID should work well here 

## 4. Diarization (who spoke when)
- pyannote diarization (VAD + segmentation + speaker embedding + clustering)
- Output: non-overlap and overlapped speech tracks (for our "%speaking" metric)

## 5. Speaker embeddings for persona features
- for each diarized speaker aggregate embeddings over that speaker's segments

## 6. Attributes per persona
- Language: from WhisperX per segment
- Sex (binary classifier)
- Age (whisper-age-estimator)
- Mood/emotion - idk

## 7. Analytics & hierarchy 
- Compute speaking time per speaker
- handle overlaps 
- rank speakers by speaking time

## 8. Output
- JSON with session summary + per-persona stats