import streamlit as st
import base64

# Eleven labs is used for generating realistic sound speech.
from elevenlabs import generate, play, Voices
from elevenlabs import set_api_key
from elevenlabs.api import Voices

# import librosa

import json
import time

from pydub.utils import mediainfo

import openai


def set_open_ai_token():
    """
    Configures open AI token.
    """    
    # Openai used for whisper and GPT
    
    try:
        OPEN_AI_TOKEN = st.secrets["OPEN_AI_TOKEN"]
    
    except Exception as error:

        with open("secrets.json") as f:
            OPEN_AI_TOKEN = json.load(f)["OPEN_AI_TOKEN"]

    # Setting the Open AI Key
    openai.api_key = OPEN_AI_TOKEN
    


@st.cache_data()
def load_eleven_labs_voice():
    """
    Loads and configures a voice from eleven labs.
    """
    
    # Extracting the eleven labs token
    
    try:
        ELEVEN_LABS_TOKEN = st.secrets["ELEVEN_LABS_TOKEN"]
    
    except Exception as error:

        with open("secrets.json") as f:
            ELEVEN_LABS_TOKEN = json.load(f)["ELEVEN_LABS_TOKEN"]

    
    set_api_key(ELEVEN_LABS_TOKEN)
    voices = Voices.from_api()  
    my_voice = voices[-1]
    my_voice.settings.stability = 1.0
    my_voice.settings.similarity_boost = 1.0
    
    return my_voice


def generate_eleven_labs_audio(text: str, voice: str) -> bytes:
    """
    Generates realistic speech from eleven labs API, and returns audio 
    bytes.
    """
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_monolingual_v1"
    )
    return audio


def autoplay_audio_from_bytes(audio_data: bytes):
    """
    Autoplays audio from a byte string.
    """

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


def get_audio_duration(filename: str) -> float:
    """
    Get the duration of an audio file in seconds.
    """
    info = mediainfo(filename)
    duration = float(info['duration'])
    return duration



