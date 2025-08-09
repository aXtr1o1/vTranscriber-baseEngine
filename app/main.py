from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import ORJSONResponse
from pathlib import Path
import shutil, json

from app.models import TranscribeRequest, TranscribeResponse
from app.services import transcribe

app = FastAPI(default_response_class=ORJSONResponse)

@app.post("/transcribe/", response_model=TranscribeResponse)
async def transcribe_endpoint(
    file:     UploadFile = File(...),
    model_id: str        = Form("scribe_v1")
):
    # ensure transcription dir
    save_dir = Path(__file__).resolve().parent.parent / "assets" / "transcription"
    save_dir.mkdir(parents=True, exist_ok=True)
    wav_path = save_dir / file.filename

    try:
        # save incoming audio
        with open(wav_path, "wb") as out_f:
            shutil.copyfileobj(file.file, out_f)

        # transcribe
        req    = TranscribeRequest(modelId=model_id, audioFile=str(wav_path))
        result = transcribe(req)

        # dump JSON to text file
        json_path = save_dir / f"{wav_path.name}_Transcription.txt"
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(result.model_dump(), jf, ensure_ascii=False, indent=2)

        return result

    except HTTPException:
        raise
    except Exception as e:
        if wav_path.exists():
            wav_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))
