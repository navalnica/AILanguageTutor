import os

from dotenv import load_dotenv
from elevenlabs.client import AsyncElevenLabs, ElevenLabs

load_dotenv(".env")

ELEVENLABS_API_KEY = os.getenv("11LABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("11LABS_API_KEY env var isn't set")

ELEVEN_CLIENT_ASYNC = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)
ELEVEN_CLIENT = ElevenLabs(api_key=ELEVENLABS_API_KEY)
