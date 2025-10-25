from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
import uvicorn

app = FastAPI(
    title="Echologia Audio Processing API",
    description="Audio transcription, diarization, and persona extraction API",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Echologia Audio Processing API",
        "version": "1.0.0",
        "endpoints": {
            "process": "/api/audio/process - Complete pipeline",
            "transcribe": "/api/audio/transcribe - Transcription only",
            "diarize": "/api/audio/diarize - Diarization only",
            "health": "/api/audio/health - Health check"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)