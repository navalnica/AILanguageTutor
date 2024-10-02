import os
import shutil
from uuid import uuid4

import gradio as gr

from src import stt, tts
from src.config import logger


async def run_stt(audio_fp: str, copy_audio=True):
    if copy_audio is True:
        out_fp = f"data/recordings/{uuid4()}.wav"
        logger.info(f'copying recorded audio to: "{out_fp}"')
        shutil.copy2(audio_fp, out_fp)

    fn = os.path.basename(out_fp)
    logger.info(f'transcribing "{fn}"...')
    transcription_response = await stt.stt(out_fp)
    transcription = transcription_response.text
    logger.info(f'transcription received: "{transcription}')
    return transcription


async def run_tts(text: str):
    logger.info(f'synthesizing audio for the following text: "{text}"')
    tts_iter_bytes = tts.tts_astream(text=text)

    out_fp = f"data/tts_generations/{uuid4()}.wav"
    logger.info(f'saving synthesized audio to: "{out_fp}"')
    with open(out_fp, "wb") as fout:
        async for chunk in tts_iter_bytes:
            if chunk:
                fout.write(chunk)
    logger.info(f'saved audio to "{out_fp}"')

    return out_fp


async def respond(chat_history: list, user_query: str, audio_fp: str):
    user_query = user_query.strip()

    if not user_query and not audio_fp:
        # do nothing
        return chat_history, user_query, audio_fp

    user_chat_message = None  # will be shown in chat
    audio_resp = None

    if user_query:
        out_fp = await run_tts(text=user_query)
        audio_resp = gr.Audio(out_fp)
        text_resp = "I've synthesized the speech for the provided text"
        user_chat_message = user_query
    elif audio_fp:
        transcription = await run_stt(audio_fp=audio_fp, copy_audio=True)
        text_resp = f"Here is what I heard:\n{transcription}"
        user_chat_message = gr.Audio(audio_fp)

    chat_history.append(gr.ChatMessage(role="user", content=user_chat_message))
    chat_history.append(gr.ChatMessage(role="assistant", content=text_resp))
    if audio_resp is not None:
        chat_history.append(gr.ChatMessage(role="assistant", content=audio_resp))

    # update chat history, clear text and audio inputs
    return chat_history, "", None


with gr.Blocks(
    title="Language Tutor",
) as demo:
    gr.Markdown("# Language Tutor")
    gr.Markdown(
        "- Send a text message to synthesize speech\n"
        "- Send an audio message to generate a transcript"
    )

    chat_widget = gr.Chatbot(type="messages", label="Chat history", height=450)

    with gr.Row(variant="compact"):
        with gr.Column():
            text_input = gr.Textbox(label="Type your query", lines=2)
        with gr.Column():
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="Record your message or upload existing audio",
            )

    # NOTE: an alternative to storing conversation in chat_widget is to use state
    # state = gr.State([])

    submit_button = gr.Button("Submit")
    submit_button.click(
        respond,
        [chat_widget, text_input, audio_input],
        [chat_widget, text_input, audio_input],
        # JavaScript code to scroll to the bottom of the updated chat widget.
        # We can't do the same in python callback, so we use additional JS callback.
        # NOTE: it MUST accept and return same parameters as passed to python callback
        # NOTE: we MUST use timer in order to wait until chat widget is populated \
        # with updated chat history from python callback
        js="""
            (c, t, a) => {
                // Add a small delay to ensure the updated chat history is rendered
                setTimeout(() => {
                    var chatContainer = document.querySelector('.bubble-wrap');
                    if (chatContainer) {
                        chatContainer.scrollTo({
                            top: chatContainer.scrollHeight,
                            behavior: 'smooth'  // Smooth scrolling animation
                        });
                    }
                }, 100);  // Delay of 100 milliseconds to ensure the chat is updated
                return [c, t, a];  // Return the values to Gradio
            }
        """,
    )


demo.launch()
