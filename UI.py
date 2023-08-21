import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64

# Eleven labs is used for generating realistic sound speech.
from elevenlabs import generate, play, Voices
from elevenlabs import set_api_key
from elevenlabs.api import Voices

# import librosa

import json
import time

from pydub.utils import mediainfo



LOCAL_AUDIO = "ElevenLabs_2023-08-11T04_12_56.000Z_Julie_C2md8UcNeLKcOBWEB71e.wav"


@st.cache_data()
def load_settings():
    
    # Extracting the eleven labs token
    
    try:
        ELEVEN_LABS_TOKEN = st.secrets["ELEVEN_LABS_TOKEN"]
    
    except Exception as error:

        with open("secrets.json") as f:
            ELEVEN_LABS_TOKEN = json.load(f)["ELEVEN_LABS_TOKEN"]


   # Setting the API set_api_key

    
    set_api_key(ELEVEN_LABS_TOKEN)
    voices = Voices.from_api()  
    my_voice = voices[-1]
    my_voice.settings.stability = 1.0
    my_voice.settings.similarity_boost = 1.0
    
    return my_voice


my_voice = load_settings()


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


def get_audio_duration(filename: str) -> float:
    """Get the duration of an audio file in seconds."""
    info = mediainfo(filename)
    duration = float(info['duration'])
    return duration


# Audio recording button.
audio_bytes = audio_recorder(key="123")


# Check if the session state has the 'processed' attribute
if not hasattr(st.session_state, 'processed'):
    st.session_state.processed = False

# audio_bytes = audio_recorder()

# Only process if the 'processed' flag is not set
if audio_bytes and not st.session_state.processed:
    start = time.time()
    response = "My response."

    # Send text to Eleven Labs API.
    audio = generate(
        text=response,
        voice=my_voice,
        model="eleven_monolingual_v1"
    )
    
    end = time.time()
    st.write(end - start)
    autoplay_audio_from_bytes(audio)
   
    # Convert audio bytes into .wav.
    with open('myfile.wav', mode='wb') as f:
        f.write(audio)

    sleep_time = get_audio_duration("myfile.wav")

    time.sleep(sleep_time)

    # Set the 'processed' flag
    st.session_state.processed = True

    # Rerun the app
    st.experimental_rerun()

# Reset audio_bytes and processed flag for the next interaction
audio_bytes = None
st.session_state.processed = False

   
