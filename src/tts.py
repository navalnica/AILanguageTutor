import typing as t

from elevenlabs import VoiceSettings

from src.config import ELEVEN_CLIENT_ASYNC, ELEVEN_CLIENT

# TODO: tune params
default_params = dict(
    voice_id="pNInz6obpgDQGcFmaJgB",  # TODO: select a better voice
    optimize_streaming_latency="0",
    output_format="mp3_22050_32",  # TODO: gradio expects sr=16kHz (? need to check)
    model_id="eleven_multilingual_v2",
    voice_settings=VoiceSettings(
        stability=0.0,
        similarity_boost=1.0,
        style=0.0,
        use_speaker_boost=True,
    ),
)


def tts_stream(text: str) -> t.Iterator[bytes]:
    async_iter = ELEVEN_CLIENT.text_to_speech.convert(text=text, **default_params)
    for chunk in async_iter:
        if chunk:
            yield chunk


def tts(text: str):
    tts_iter = tts_stream(text=text)
    combined = b"".join(tts_iter)
    return combined


async def tts_astream(text: str) -> t.AsyncIterator[bytes]:
    async_iter = ELEVEN_CLIENT_ASYNC.text_to_speech.convert(text=text, **default_params)
    async for chunk in async_iter:
        if chunk:
            yield chunk
