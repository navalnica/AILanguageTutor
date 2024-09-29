import streamlit as st
from st_audiorec import st_audiorec

with st.chat_message("user"):
    st.write("Hello 👋")
with st.chat_message("ai"):
    st.write("Hello, how can I help you?")
with st.chat_message("user"):
    st.write("What is the current weather in UK?")
with st.chat_message("ai"):
    st.write(
        "This is the sample audio file. If there is anything else I can help you with, please ask"
    )
    st.audio(data="data/sample1.mp3")

wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")
