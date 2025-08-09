import requests

url = "http://127.0.0.1:8000/transcribe/"
file_path = "C:\\Users\\HP\\Documents\\aXtrLabs\\vTranscriber-baseEngine\\assets\\audio\\audio.mp4"

with open(file_path, "rb") as audio_file:
    response = requests.post(
        url,
        files={"file": (file_path, audio_file)},
    )

print("Status:", response.status_code)
print("Response:", response.json())
