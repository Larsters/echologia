from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import openai
import json
import os

app = FastAPI(title="Meeting Data Processor", version="1.0.0")

# Configure OpenAI (you can also use Anthropic, etc.)
# Set your API key: export OPENAI_API_KEY="your-key"
openai.api_key = os.getenv("OPENAI_API_KEY")

# ===== Pydantic Models =====

class Word(BaseModel):
    word: str
    start: float
    end: float
    confidence: float

class Emotion(BaseModel):
    label: str
    confidence: float

class Segment(BaseModel):
    start: float
    end: float
    speaker_id: str
    text: str
    words: List[Word]
    language: str
    emotion: Emotion

class SexInfo(BaseModel):
    label: str
    confidence: float

class AgeInfo(BaseModel):
    label: str
    mean_estimate: int
    confidence: float

class MoodSummary(BaseModel):
    dominant: str
    variation: Optional[List[str]] = None

class Persona(BaseModel):
    speaker_id: str
    speaking_time_sec: float
    speaking_percent: float
    overlap_ratio: float
    languages: Dict[str, float]
    sex: SexInfo
    age: AgeInfo
    mood_summary: MoodSummary
    embedding_vector: Optional[str] = None

class Meta(BaseModel):
    duration_sec: float
    sampling_rate: int
    model_asr: str
    model_diarization: str
    model_age: str
    model_emotion: str
    date_processed: str

class MeetingData(BaseModel):
    session_id: str
    meta: Meta
    segments: List[Segment]
    personas: List[Persona]
    hierarchy: List[str]
    global_emotion_trend: Dict[str, float]

class LLMAnalysisRequest(BaseModel):
    command: str = Field(..., description="Analysis command/question for the LLM")
    model: str = Field(default="gpt-4o-mini", description="LLM model to use")

# ===== Data Processing Methods =====

class MeetingProcessor:
    def __init__(self, data: MeetingData):
        self.data = data
    
    def get_hierarchy(self) -> Dict[str, Any]:
        """Extract and analyze speaker hierarchy"""
        hierarchy_info = []
        
        for rank, speaker_id in enumerate(self.data.hierarchy, 1):
            persona = next((p for p in self.data.personas if p.speaker_id == speaker_id), None)
            if persona:
                hierarchy_info.append({
                    "rank": rank,
                    "speaker_id": speaker_id,
                    "speaking_time_sec": persona.speaking_time_sec,
                    "speaking_percent": persona.speaking_percent,
                    "dominant_mood": persona.mood_summary.dominant,
                    "sex": persona.sex.label,
                    "age_group": persona.age.label
                })
        
        return {
            "hierarchy": hierarchy_info,
            "leader": self.data.hierarchy[0] if self.data.hierarchy else None,
            "total_speakers": len(self.data.hierarchy)
        }
    
    def get_military_mission_indicators(self) -> Dict[str, Any]:
        """Analyze potential military/mission-related indicators"""
        keywords = ['mission', 'objective', 'target', 'operation', 'deploy', 
                    'secure', 'command', 'orders', 'tactical', 'strategic']
        
        mission_segments = []
        keyword_counts = {kw: 0 for kw in keywords}
        
        for segment in self.data.segments:
            text_lower = segment.text.lower()
            found_keywords = []
            
            for keyword in keywords:
                if keyword in text_lower:
                    keyword_counts[keyword] += 1
                    found_keywords.append(keyword)
            
            if found_keywords:
                mission_segments.append({
                    "timestamp": f"{segment.start:.2f}s - {segment.end:.2f}s",
                    "speaker": segment.speaker_id,
                    "text": segment.text,
                    "keywords": found_keywords,
                    "emotion": segment.emotion.label
                })
        
        return {
            "mission_related_segments": mission_segments,
            "keyword_frequency": {k: v for k, v in keyword_counts.items() if v > 0},
            "total_mission_mentions": len(mission_segments),
            "mission_probability": min(len(mission_segments) / len(self.data.segments), 1.0) if self.data.segments else 0
        }
    
    def get_speaker_analysis(self) -> Dict[str, Any]:
        """Detailed speaker analysis"""
        return {
            "total_speakers": len(self.data.personas),
            "speakers": [
                {
                    "speaker_id": p.speaker_id,
                    "demographics": {
                        "sex": p.sex.label,
                        "age_group": p.age.label,
                        "estimated_age": p.age.mean_estimate
                    },
                    "participation": {
                        "speaking_time_sec": p.speaking_time_sec,
                        "speaking_percent": p.speaking_percent,
                        "overlap_ratio": p.overlap_ratio
                    },
                    "communication": {
                        "primary_language": max(p.languages.items(), key=lambda x: x[1])[0],
                        "languages": p.languages,
                        "dominant_mood": p.mood_summary.dominant,
                        "mood_variations": p.mood_summary.variation
                    }
                }
                for p in self.data.personas
            ]
        }
    
    def get_emotion_timeline(self) -> Dict[str, Any]:
        """Analyze emotion progression throughout meeting"""
        timeline = []
        
        for segment in self.data.segments:
            timeline.append({
                "timestamp": segment.start,
                "speaker": segment.speaker_id,
                "emotion": segment.emotion.label,
                "confidence": segment.emotion.confidence
            })
        
        return {
            "emotion_timeline": timeline,
            "global_trend": self.data.global_emotion_trend,
            "dominant_emotion": max(self.data.global_emotion_trend.items(), key=lambda x: x[1])[0]
        }
    
    def get_conversation_dynamics(self) -> Dict[str, Any]:
        """Analyze conversation flow and interactions"""
        speaker_transitions = []
        prev_speaker = None
        
        for segment in self.data.segments:
            if prev_speaker and prev_speaker != segment.speaker_id:
                speaker_transitions.append({
                    "from": prev_speaker,
                    "to": segment.speaker_id,
                    "timestamp": segment.start
                })
            prev_speaker = segment.speaker_id
        
        # Calculate turn-taking frequency
        transition_matrix = {}
        for trans in speaker_transitions:
            key = f"{trans['from']} -> {trans['to']}"
            transition_matrix[key] = transition_matrix.get(key, 0) + 1
        
        return {
            "total_transitions": len(speaker_transitions),
            "transition_matrix": transition_matrix,
            "average_segment_duration": self.data.meta.duration_sec / len(self.data.segments) if self.data.segments else 0,
            "most_active_speaker": max(self.data.personas, key=lambda p: p.speaking_time_sec).speaker_id if self.data.personas else None
        }
    
    def get_full_transcript(self) -> Dict[str, Any]:
        """Get formatted transcript"""
        return {
            "session_id": self.data.session_id,
            "duration": f"{self.data.meta.duration_sec:.2f}s",
            "transcript": [
                {
                    "timestamp": f"[{seg.start:.2f}s - {seg.end:.2f}s]",
                    "speaker": seg.speaker_id,
                    "text": seg.text,
                    "emotion": seg.emotion.label
                }
                for seg in self.data.segments
            ]
        }
    
    async def analyze_with_llm(self, command: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
        """Send meeting data and command to LLM for analysis"""
        try:
            # Prepare context data
            context = {
                "session_id": self.data.session_id,
                "duration_sec": self.data.meta.duration_sec,
                "speakers": len(self.data.personas),
                "hierarchy": self.data.hierarchy,
                "personas": [p.dict() for p in self.data.personas],
                "segments": [s.dict() for s in self.data.segments],
                "global_emotion_trend": self.data.global_emotion_trend
            }
            
            system_prompt = """You are an expert meeting analyst. You analyze meeting transcripts with speaker information, 
            emotions, demographics, and conversation dynamics. Provide detailed, actionable insights based on the data provided."""
            
            user_prompt = f"""Meeting Data:
{json.dumps(context, indent=2)}

Analysis Request: {command}

Please provide a detailed analysis based on the meeting data above."""

            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return {
                "command": command,
                "model": model,
                "analysis": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM analysis failed: {str(e)}")

# ===== API Endpoints =====

# Store meeting data in memory (use database in production)
meeting_storage: Dict[str, MeetingData] = {}

@app.post("/upload", response_model=Dict[str, str])
async def upload_meeting_data(data: MeetingData):
    """Upload meeting data for processing"""
    meeting_storage[data.session_id] = data
    return {
        "status": "success",
        "session_id": data.session_id,
        "message": f"Meeting data uploaded successfully. {len(data.segments)} segments processed."
    }

@app.get("/hierarchy/{session_id}")
async def get_hierarchy(session_id: str):
    """Get speaker hierarchy analysis"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return processor.get_hierarchy()

@app.get("/military-mission/{session_id}")
async def get_military_mission(session_id: str):
    """Analyze potential military/mission indicators"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return processor.get_military_mission_indicators()

@app.get("/speaker-analysis/{session_id}")
async def get_speaker_analysis(session_id: str):
    """Get detailed speaker analysis"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return processor.get_speaker_analysis()

@app.get("/emotion-timeline/{session_id}")
async def get_emotion_timeline(session_id: str):
    """Get emotion progression timeline"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return processor.get_emotion_timeline()

@app.get("/conversation-dynamics/{session_id}")
async def get_conversation_dynamics(session_id: str):
    """Analyze conversation flow and dynamics"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return processor.get_conversation_dynamics()

@app.get("/transcript/{session_id}")
async def get_transcript(session_id: str):
    """Get formatted transcript"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return processor.get_full_transcript()

@app.post("/analyze-llm/{session_id}")
async def analyze_with_llm(session_id: str, request: LLMAnalysisRequest):
    """Analyze meeting data using LLM with custom command"""
    if session_id not in meeting_storage:
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = MeetingProcessor(meeting_storage[session_id])
    return await processor.analyze_with_llm(request.command, request.model)

@app.get("/sessions")
async def list_sessions():
    """List all available sessions"""
    return {
        "sessions": [
            {
                "session_id": session_id,
                "duration_sec": data.meta.duration_sec,
                "speakers": len(data.personas),
                "segments": len(data.segments)
            }
            for session_id, data in meeting_storage.items()
        ]
    }

@app.get("/")
async def root():
    """API information"""
    return {
        "name": "Meeting Data Processor API",
        "version": "1.0.0",
        "endpoints": {
            "POST /upload": "Upload meeting data",
            "GET /hierarchy/{session_id}": "Get speaker hierarchy",
            "GET /military-mission/{session_id}": "Analyze military/mission indicators",
            "GET /speaker-analysis/{session_id}": "Detailed speaker analysis",
            "GET /emotion-timeline/{session_id}": "Emotion progression",
            "GET /conversation-dynamics/{session_id}": "Conversation flow analysis",
            "GET /transcript/{session_id}": "Formatted transcript",
            "POST /analyze-llm/{session_id}": "Custom LLM analysis",
            "GET /sessions": "List all sessions"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)