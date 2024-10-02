from src.config import OPENAI_ACLIENT


async def stt(fp: str):
    # TODO: handle files >25MB in size
    # TODO: handle streaming
    with open(fp, "rb") as fin:
        transcription = await OPENAI_ACLIENT.audio.transcriptions.create(
            model="whisper-1", file=fin
        )
    return transcription
