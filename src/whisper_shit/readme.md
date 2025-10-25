# Structure:
## 1. Input & Cleanup
- Load audio -> resample to standard 16kHz -> normalize
- Denoise, deverb (mb pyannote/audio denoiser)

## 2. Voice Activity Detection (VAD)
- pyannote VAD to find speech regions. Reducing Whisper compute time and improving transcription accuracy.