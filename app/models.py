from pydantic import BaseModel
from typing import List, Optional

class AudioEvent(BaseModel):
    type: str
    start: float
    end: float

class Segment(BaseModel):
    speaker_id: str
    start: float
    end: float
    text: str

class TranscribeRequest(BaseModel):
    modelId: str
    audioFile: str

class TranscribeResponse(BaseModel):
    status: str
    segments: List[Segment]
    language_code: str
    language_probability: float
    diarize: bool
    num_speakers: Optional[int]
    audio_events: Optional[List[AudioEvent]]
    exec_time: float
