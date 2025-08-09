import os
from dotenv import load_dotenv
from pathlib import Path

path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=path)

ELEVENLABS = os.getenv('ELEVENLABS')
