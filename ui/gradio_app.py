import gradio as gr


def respond(chat_history: list, user_query: str, audio_fp: str):
    user_query = user_query.strip()

    if not user_query and not audio_fp:
        # do nothing
        return chat_history, user_query, audio_fp

    text_resp = (
        f"Sample AI response. "
        f"audio received: {bool(audio_fp)}. "
        f"text received: {bool(user_query)}."
    )
    if user_query:
        text_resp += f' text query: "{user_query}"'

    user_query_to_show = user_query
    if audio_fp:
        user_query_to_show = gr.Audio(audio_fp)
        audio_resp = gr.Audio(audio_fp)
    else:
        audio_resp = None

    chat_history.append(gr.ChatMessage(role="user", content=user_query_to_show))
    chat_history.append(gr.ChatMessage(role="assistant", content=text_resp))
    if audio_resp is not None:
        chat_history.append(gr.ChatMessage(role="assistant", content=audio_resp))

    # update chat history, clear text and audio inputs
    return chat_history, "", None


with gr.Blocks() as demo:
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
