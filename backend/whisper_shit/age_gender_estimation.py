import numpy as np
import torch
import torch.nn as nn
from transformers import Wav2Vec2Processor
from transformers.models.wav2vec2.modeling_wav2vec2 import (
    Wav2Vec2Model,
    Wav2Vec2PreTrainedModel,
)


class ModelHead(nn.Module):
    r"""Classification head."""

    def __init__(self, config, num_labels):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.final_dropout)
        self.out_proj = nn.Linear(config.hidden_size, num_labels)

    def forward(self, features, **kwargs):
        x = features
        x = self.dropout(x)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x


class AgeGenderModel(Wav2Vec2PreTrainedModel):
    r"""Speech age and gender classifier."""

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.wav2vec2 = Wav2Vec2Model(config)
        self.age = ModelHead(config, 1)
        self.gender = ModelHead(config, 3)
        self.init_weights()

    def forward(self, input_values):
        outputs = self.wav2vec2(input_values)
        hidden_states = outputs[0]
        hidden_states = torch.mean(hidden_states, dim=1)
        logits_age = self.age(hidden_states)
        logits_gender = torch.softmax(self.gender(hidden_states), dim=1)
        return hidden_states, logits_age, logits_gender


AGE_GENDER_MODEL_ID = "audeering/wav2vec2-large-robust-24-ft-age-gender"
_age_gender_processor = None
_age_gender_model = None


def _load_age_gender_model(device: torch.device):
    """Load the age/gender model (cached globally)."""
    global _age_gender_processor, _age_gender_model
    if _age_gender_model is None:
        print("🧠 Loading age & gender classifier...")
        _age_gender_processor = Wav2Vec2Processor.from_pretrained(AGE_GENDER_MODEL_ID)
        _age_gender_model = AgeGenderModel.from_pretrained(AGE_GENDER_MODEL_ID).to(device)
        _age_gender_model.eval()
    return _age_gender_processor, _age_gender_model


def estimate_age_gender_for_personas(
    audio_np: np.ndarray, 
    sr: int, 
    diar_segments: list[dict], 
    personas: list[dict]
) -> list[dict]:
    """
    Estimate age and gender for each persona using their audio segments.
    
    Args:
        audio_np: Full audio waveform as numpy array
        sr: Sample rate (should be 16000)
        diar_segments: List of diarization segments with speaker_id, start, end
        personas: List of persona dicts to update
        
    Returns:
        Updated personas with age and sex fields populated
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor, model = _load_age_gender_model(device)

    for persona in personas:
        spk_id = persona["speaker_id"]
        
        # Collect all audio segments for this speaker
        spans = [(seg["start"], seg["end"]) for seg in diar_segments if seg["speaker_id"] == spk_id]
        if not spans:
            continue

        # Extract and concatenate audio chunks
        chunks = []
        for start, end in spans:
            s_idx = max(0, int(start * sr))
            e_idx = min(len(audio_np), int(end * sr))
            if e_idx > s_idx:
                chunks.append(audio_np[s_idx:e_idx])

        if not chunks:
            continue

        speaker_audio = np.concatenate(chunks)
        
        # Skip if too short
        if speaker_audio.size < sr * 0.5:
            continue

        # Process audio through the model
        y = processor(speaker_audio, sampling_rate=sr)
        y = y['input_values'][0]
        y = y.reshape(1, -1)
        y = torch.from_numpy(y).to(device)

        with torch.no_grad():
            hidden_states, logits_age, logits_gender = model(y)

        # Extract age (continuous value from 0-1, scale to years)
        age_normalized = logits_age.item()
        age_years = age_normalized * 100  # Scale to 0-100 years
        
        # Extract gender (3 classes: female, male, child)
        gender_probs = logits_gender[0].detach().cpu().numpy()
        gender_labels = ["female", "male", "child"]
        gender_idx = np.argmax(gender_probs)
        gender_label = gender_labels[gender_idx]
        gender_conf = float(gender_probs[gender_idx])

        # Map age to categories - simplified to 4 only
        if age_years < 18:
            age_label = "Child"
            age_mean = 12
        elif age_years < 35:
            age_label = "Teenager"
            age_mean = 25
        elif age_years < 60:
            age_label = "Adult"
            age_mean = int(age_years)
        else:
            age_label = "Senior"
            age_mean = int(age_years)

        # Update persona
        persona["sex"] = {
            "label": gender_label, 
            "confidence": round(gender_conf, 3)
        }
        persona["age"] = {
            "label": age_label,
            "mean_estimate": age_mean,
            "confidence": 0.8,  
        }

    return personas


# Remove test code from module level - it was running on import
if __name__ == "__main__":
    # This is only for manual testing
    device = 'cpu'
    processor = Wav2Vec2Processor.from_pretrained(AGE_GENDER_MODEL_ID)
    model = AgeGenderModel.from_pretrained(AGE_GENDER_MODEL_ID)
    
    sampling_rate = 16000
    signal = np.zeros((1, sampling_rate), dtype=np.float32)
    
    y = processor(signal, sampling_rate=sampling_rate)
    y = y['input_values'][0]
    y = y.reshape(1, -1)
    y = torch.from_numpy(y).to(device)
    
    with torch.no_grad():
        y = model(y)
    
    print(torch.hstack([y[1], y[2]]).detach().cpu().numpy())