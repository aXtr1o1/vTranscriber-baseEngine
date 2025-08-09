import mimetypes, os, time
from fastapi import HTTPException
from requests import post
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

from app.config import ELEVENLABS
from app.models import (
    TranscribeRequest,
    TranscribeResponse,
    Segment,
    AudioEvent,
)

def transcribe(request: TranscribeRequest) -> TranscribeResponse:
    start_time = time.time()

    # guess MIME
    mime_type, _ = mimetypes.guess_type(request.audioFile)
    if not mime_type:
        mime_type = "application/octet-stream"

    # build form (no num_speakers parameter)
    encoder = MultipartEncoder(fields={
        "model_id":               request.modelId,
        "diarize":                "true",
        "tag_audio_events":       "true",
        "timestamps_granularity": "word",
        "file": (
            os.path.basename(request.audioFile),
            open(request.audioFile, "rb"),
            mime_type
        )
    })

    bar     = tqdm(total=encoder.len, unit="B", unit_scale=True, desc="Uploading")
    monitor = MultipartEncoderMonitor(encoder, lambda m: bar.update(m.bytes_read - bar.n))

    try:
        resp = post(
            "https://api.elevenlabs.io/v1/speech-to-text",
            data=monitor,
            headers={
                "Content-Type": monitor.content_type,
                "xi-api-key":   ELEVENLABS
            },
            timeout=300
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        bar.close()
        if os.path.exists(request.audioFile):
            os.remove(request.audioFile)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
    finally:
        bar.close()
        if os.path.exists(request.audioFile):
            os.remove(request.audioFile)

    # top-level fields
    language_code        = data.get("language_code", "")
    language_probability = data.get("language_probability", 0.0)
    diarize_flag         = data.get("diarize", False)
    num_speakers         = data.get("num_speakers")
    raw_events           = data.get("audio_events", [])
    audio_events         = [AudioEvent(**evt) for evt in raw_events]

    # gather words & build segments
    raw_words = data.get("words", [])
    words     = [w for w in raw_words if w.get("type")=="word" and w.get("text","").strip()]

    segments = []
    if words:
        spk    = words[0]["speaker_id"]
        start  = words[0]["start"]
        end    = words[0]["end"]
        buffer = [words[0]["text"]]

        for w in words[1:]:
            if w["speaker_id"] != spk:
                segments.append(Segment(
                    speaker_id=spk, start=start, end=end, text=" ".join(buffer).strip()
                ))
                spk    = w["speaker_id"]
                start  = w["start"]
                buffer = [w["text"]]
            else:
                buffer.append(w["text"])
            end = w["end"]

        # flush last
        segments.append(Segment(
            speaker_id=spk, start=start, end=end, text=" ".join(buffer).strip()
        ))

    exec_time = round(time.time() - start_time, 3)

    return TranscribeResponse(
        status=                "success" if language_code else "error",
        segments=              segments,
        language_code=         language_code,
        language_probability=  language_probability,
        diarize=               diarize_flag,
        num_speakers=          num_speakers,
        audio_events=          audio_events,
        exec_time=             exec_time
    )
