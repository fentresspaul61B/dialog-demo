import streamlit as st
from audio_recorder_streamlit import audio_recorder

audio_bytes = audio_recorder()
if audio_bytes:
    # st.audio(audio_bytes, format="audio/wav")
    
    if st.button("Test Speakers"):
        autoplay_audio("ElevenLabs_2023-08-11T04_12_56.000Z_Julie_C2md8UcNeLKcOBWEB71e.wav")
        # Embed audio with autoplay
    



import base64

import streamlit as st


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )


if st.button("Test Speakers"):
    autoplay_audio("ElevenLabs_2023-08-11T04_12_56.000Z_Julie_C2md8UcNeLKcOBWEB71e.wav")
    # Embed audio with autoplay
    
    
