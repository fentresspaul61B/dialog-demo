import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64

# Eleven labs is used for generating realistic sound speech.
from elevenlabs import generate, play, Voices
from elevenlabs import set_api_key
from elevenlabs.api import Voices

import json

import time


# @st.cache_data()
def load_settings():
    
    # Extracting the eleven labs token
    
    try:
        ELEVEN_LABS_TOKEN = st.secrets["ELEVEN_LABS_TOKEN"]
    
    except Exception as error:

        with open("secrets.json") as f:
            ELEVEN_LABS_TOKEN = json.load(f)["ELEVEN_LABS_TOKEN"]


   # Setting the API set_api_key
    return ELEVEN_LABS_TOKEN

ELEVEN_LABS_TOKEN = load_settings()

set_api_key(ELEVEN_LABS_TOKEN)
voices = Voices.from_api()
my_voice = voices[-1]
my_voice.settings.stability = 1.0
my_voice.settings.similarity_boost = 1.0
# return my_voice



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
    st.experimental_rerun() 

def autoplay_audio_from_bytes(audio_data: bytes):
    b64 = base64.b64encode(audio_data).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/wav;base64,{b64}" type="audio/wav">
        </audio>
        """
    st.markdown(
        md,
        unsafe_allow_html=True,
    )
    # st.experimental_rerun()
audio_bytes = None
audio_bytes = audio_recorder()
if audio_bytes:
    # st.audio(audio_bytes, format="audio/wav")
     
    # autoplay_audio("ElevenLabs_2023-08-11T04_12_56.000Z_Julie_C2md8UcNeLKcOBWEB71e.wav")

    start = time.time()
    response = "My response."

    # 8. Send text to Eleven Labs API.
    audio = generate(
        text=response,
        voice=my_voice,
        model="eleven_monolingual_v1"
    )
        
    # 9. Play the eleven labs audio.
    play(audio)
    end = time.time()
    st.write(end - start)

    # Embed audio with autoplay
    # with open('myfile.wav', mode='wb') as f:
    #     f.write(audio)

    # autoplay_audio("myfile.wav")
    autoplay_audio_from_bytes(audio)
if st.button("Test Speakers"):
    # autoplay_audio("ElevenLabs_2023-08-11T04_12_56.000Z_Julie_C2md8UcNeLKcOBWEB71e.wav")
    # Embed audio with autoplay
    
    start = time.time()
    response = "My response."

    # 8. Send text to Eleven Labs API.
    audio = generate(
        text=response,
        voice=my_voice,
        model="eleven_monolingual_v1"
    )
        
    # 9. Play the eleven labs audio.
    play(audio)
    end = time.time()
    st.write(end - start)

    # Embed audio with autoplay
    # with open('myfile.wav', mode='wb') as f:
    #     f.write(audio)

    # autoplay_audio("myfile.wav")
    autoplay_audio_from_bytes(audio)
    
    
