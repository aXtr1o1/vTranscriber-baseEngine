# vTranscriber-baseEngine
Base Engine for MultiLang Voice Transcription Generation


A MultiLang speech-to-text service powered by FastAPI, designed to process and transcribe audio files efficiently. The system uses ElevenLabs' API for transcription, with added features such as diarization (speaker identification), language detection, audio event tagging, and more.

---

## Key Features

- **Diarization**: Automatically identifies multiple speakers in the audio and segments the text accordingly.
- **Language Detection**: Detects the language of the audio and provides a confidence score.
- **Audio Events**: Detects special audio events like laughter, speech, silence, etc.
- **Transcription Output**: Transcriptions are saved as `.txt` files in the format: `assets/transcription/<filename>.m4a_Transcription.txt`.
- **Modular Architecture**: Service and model layers to separate business logic and API calls.
- **Temporary File Cleanup**: Automatically deletes uploaded files after transcription to prevent disk space issues.
- **Real-time Feedback**: Displays a progress bar during file upload and transcription.

---

## Prerequisites

Before you begin, make sure you have the following installed and configured:

- **Python 3.8+**
- **ElevenLabs API Key**: Obtain your key from [ElevenLabs](https://www.elevenlabs.io).
- **FastAPI**: Python framework to build the REST API.
- **Uvicorn**: ASGI server to run the FastAPI application.
- **python-dotenv**: For managing environment variables.
- **requests**: For making HTTP requests.

---

##  Environment Setup


### 1. Add your ElevenLabs API key to `.env`:

```env
ELEVENLABS=your_actual_elevenlabs_api_key_here
```

### 2. Install python-dotenv (if not already included):

```bash
pip install python-dotenv
```


---

## Installation and Setup

### 1. Clone the repository:

```bash
git clone <repository-url>
cd GSQuareASR
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

---

## API Endpoints

### `POST /transcribe/`

**Description:** Uploads an audio file and returns its transcription.

**Parameters:**
- `file` (form-data): Audio file to transcribe

**Supported Formats:** `.mp3`, `.wav`, `.m4a`, `.mp4`

**Response:** JSON object with transcription result

---

## Testing

### Test with `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/transcribe/" \
  -F "file=@/path/to/your/audio.mp4"
```

### Test with Python requests:

```python
import requests

url = "http://127.0.0.1:8000/transcribe/"
file_path = "location\\to\\your\\audio.mp4"

with open(file_path, "rb") as audio_file:
    response = requests.post(
        url,
        files={"file": (file_path, audio_file)},
    )

print("Status:", response.status_code)
print("Response:", response.json())
```

---

## 📄 Example Response

```json
{
  "language_code": "tam",
  "language_probability": 0.9998,
  "diarize": true,
  "num_speakers": 2,
  "audio_events": [
    "laughter", 
    "speech",
    "silence"
  ],
  "segments": [
    {
      "speaker_id": "speaker_1",
      "start": 0.0,
      "end": 5.0,
      "text": "Hello, how are you?"
    },
    {
      "speaker_id": "speaker_2",
      "start": 5.0,
      "end": 10.0,
      "text": "I'm doing great, thanks!"
    }
  ]
}
```

### Error Response Example:

```json
{
  "detail": {
    "Internal Server Error:": "code",
    "Error": "Error"
  }
}
```

---

## Project Structure

```
vTranscriber-baseEngine/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic models and data structures
├── services.py          # Business logic and ElevenLabs integration
├── .env                 # Environment variables (not in version control)
├── .gitignore          # Git ignore file
├── requirements.txt     # Python dependencies
├── assets/
│   └── audio/          # Directory for actual audio fies
|   └── transcription/  # Directory for temporary audio files
└── README.md           # Project documentation
```

---

## 📋 Dependencies

Create a `requirements.txt` file with the following dependencies:

```txt
elevenlabs
python-dotenv
fastapi
uvicorn
python-multipart
requests
```

---

## File Management

The service automatically handles temporary file cleanup. Uploaded files are removed after transcription to prevent disk space issues.

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ELEVENLABS` | Your ElevenLabs API key | Yes |

### API Configuration

You can modify the following settings in your code:
- Upload file size limits
- Supported file formats
- Temporary file storage location

---

## Troubleshooting

### Common Issues:

1. **"API key not found"** - Make sure your `.env` file contains the correct ElevenLabs API key
2. **"File format not supported"** - Check that your audio file is in a supported format
3. **"Connection error"** - Verify your internet connection and ElevenLabs API status

### Debug Mode:

Run with debug logging:

```bash
uvicorn main:app --reload --log-level debug
```

---

##  API Documentation

##  How to Use `curl` to Test the API

You can use the following `curl` command to send an audio file to the `/transcribe/` endpoint for transcription:

```bash
curl -X POST http://127.0.0.1:8000/transcribe/ \
  -F "file=@C:/path/to/your/audio.mp4"
```

---

##  Explanation of Each Part:

| Part | Description |
|------|-------------|
| `curl` | Command-line tool to send HTTP requests |
| `-X POST` | Specifies the HTTP method (POST in this case) |
| `http://127.0.0.1:8000/transcribe/` | The local URL of your FastAPI endpoint |
| `-F "file=@path/to/file"` | Sends the file as a form-data field named `file` |
| `@C:/path/to/your/audio.mp4` | The `@` symbol tells curl to read the file from your local file system |

---

##  Important Note

Replace `C:/path/to/your/audio.mp4` with the actual path to your audio file on your machine.

**Example paths:**
- **Windows:** `C:\Users\YourName\Documents\audio.mp3`
- **macOS/Linux:** `/home/username/audio.wav` or `~/Documents/audio.m4a`

---

##  Supported File Formats:

- `.mp3`
- `.wav`
- `.m4a`
- `.mp4` (audio-only or convertible)

---

##  Expected Response:

A successful request will return a JSON object containing the transcription:

```json
{
  "Message": {
    "language_code": "language",
    "language_probability":"probability of the language",
    "text": "Transcribed audio content here..."
  }
}
```