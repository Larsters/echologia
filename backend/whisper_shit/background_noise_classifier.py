"""
Background noise and environmental sound classification using Audio Spectrogram Transformer (AST).
Uses MIT/ast-finetuned-audioset-10-10-0.4593 model trained on AudioSet (632 classes).
"""

import numpy as np
import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification


AST_MODEL_ID = "MIT/ast-finetuned-audioset-10-10-0.4593"
_ast_feature_extractor = None
_ast_model = None


def _load_ast_model(device: torch.device):
    """Load the AST model and feature extractor (cached globally)."""
    global _ast_feature_extractor, _ast_model
    if _ast_model is None:
        print("🎵 Loading Audio Spectrogram Transformer for background classification...")
        _ast_feature_extractor = ASTFeatureExtractor.from_pretrained(AST_MODEL_ID)
        _ast_model = ASTForAudioClassification.from_pretrained(AST_MODEL_ID).to(device)
        _ast_model.eval()
    return _ast_feature_extractor, _ast_model


def classify_background_audio(
    audio_np: np.ndarray,
    sr: int,
    top_k: int = 5,
    device: torch.device = None
) -> list[dict]:
    """
    Classify background audio into AudioSet categories.

    Args:
        audio_np: Audio waveform as numpy array
        sr: Sample rate (should be 16000)
        top_k: Number of top predictions to return
        device: Torch device (None for auto-detect)

    Returns:
        List of dicts with 'label' and 'confidence' for top-K predictions
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    feature_extractor, model = _load_ast_model(device)

    # Prepare audio input
    # AST expects 16kHz audio, which matches our pipeline
    inputs = feature_extractor(
        audio_np,
        sampling_rate=sr,
        return_tensors="pt"
    )

    # Move to device
    input_values = inputs.input_values.to(device)

    # Get predictions
    with torch.no_grad():
        outputs = model(input_values)
        logits = outputs.logits

    # Apply softmax to get probabilities
    probs = torch.nn.functional.softmax(logits, dim=-1)[0]

    # Get top-k predictions
    top_k_probs, top_k_indices = torch.topk(probs, k=top_k)

    # Convert to list of dicts
    predictions = []
    for prob, idx in zip(top_k_probs.cpu().numpy(), top_k_indices.cpu().numpy()):
        label = model.config.id2label[int(idx)]
        predictions.append({
            "label": label,
            "confidence": round(float(prob), 4)
        })

    return predictions


def classify_background_segments(
    audio_np: np.ndarray,
    sr: int,
    segments: list[dict],
    top_k: int = 3
) -> dict:
    """
    Classify background audio for specific segments.

    Args:
        audio_np: Full audio waveform as numpy array
        sr: Sample rate (should be 16000)
        segments: List of segments with 'start' and 'end' times
        top_k: Number of top predictions per segment

    Returns:
        Dict mapping segment indices to their background classifications
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feature_extractor, model = _load_ast_model(device)

    segment_classifications = {}

    for i, segment in enumerate(segments):
        start_idx = int(segment["start"] * sr)
        end_idx = int(segment["end"] * sr)

        # Skip very short segments
        if end_idx - start_idx < sr * 0.5:  # Less than 0.5 seconds
            continue

        # Extract segment audio
        segment_audio = audio_np[start_idx:end_idx]

        # Classify
        try:
            predictions = classify_background_audio(
                segment_audio,
                sr,
                top_k=top_k,
                device=device
            )
            segment_classifications[i] = predictions
        except Exception as e:
            print(f"⚠️  Failed to classify segment {i}: {e}")
            continue

    return segment_classifications


def get_session_background_summary(
    audio_np: np.ndarray,
    sr: int,
    max_audio_length_sec: int = 30,
    top_k: int = 5
) -> dict:
    """
    Get overall background audio summary for the entire session.
    Uses up to max_audio_length_sec seconds of audio (from beginning).

    Args:
        audio_np: Full audio waveform
        sr: Sample rate
        max_audio_length_sec: Max seconds to analyze (to avoid memory issues)
        top_k: Number of top predictions to return

    Returns:
        Dict with 'dominant_classes' list
    """
    # Limit audio length to avoid memory issues
    max_samples = max_audio_length_sec * sr
    if len(audio_np) > max_samples:
        # Take samples from beginning, middle, and end
        third = len(audio_np) // 3
        samples = []
        samples.append(audio_np[:max_samples // 3])
        samples.append(audio_np[third:third + max_samples // 3])
        samples.append(audio_np[-max_samples // 3:])
        audio_segment = np.concatenate(samples)
    else:
        audio_segment = audio_np

    # Classify
    predictions = classify_background_audio(audio_segment, sr, top_k=top_k)

    return {
        "dominant_classes": predictions
    }


if __name__ == "__main__":
    # Test code
    print("🧪 Testing Background Noise Classifier...")

    # Create dummy audio
    sr = 16000
    duration = 5
    audio = np.random.randn(sr * duration).astype(np.float32) * 0.01

    # Test session-level classification
    print("\n📊 Session-level classification:")
    summary = get_session_background_summary(audio, sr, max_audio_length_sec=5, top_k=5)
    for pred in summary["dominant_classes"]:
        print(f"  - {pred['label']}: {pred['confidence']:.4f}")

    # Test segment classification
    print("\n📊 Segment-level classification:")
    segments = [
        {"start": 0.0, "end": 2.5},
        {"start": 2.5, "end": 5.0}
    ]
    segment_results = classify_background_segments(audio, sr, segments, top_k=3)
    for seg_idx, preds in segment_results.items():
        print(f"\n  Segment {seg_idx}:")
        for pred in preds:
            print(f"    - {pred['label']}: {pred['confidence']:.4f}")

    print("\n✅ Test complete!")
