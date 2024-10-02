import logging
import os

import httpx
from dotenv import load_dotenv
from elevenlabs.client import AsyncElevenLabs, ElevenLabs
from openai import AsyncOpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (%(filename)s): %(message)s",
)
logger = logging.getLogger("lang-tutor")

load_dotenv(".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("11LABS_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY env var isn't set")
if not ELEVENLABS_API_KEY:
    raise ValueError("11LABS_API_KEY env var isn't set")


OPENAI_ACLIENT = AsyncOpenAI(
    api_key=OPENAI_API_KEY, max_retries=3, timeout=httpx.Timeout(5, connect=5)
)
ELEVEN_CLIENT_ASYNC = AsyncElevenLabs(api_key=ELEVENLABS_API_KEY)
ELEVEN_CLIENT = ElevenLabs(api_key=ELEVENLABS_API_KEY)
