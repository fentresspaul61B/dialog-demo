"""

"""

# Streamlit used to render web UI.
import streamlit as st

# Audio recorder used to record user audio during dialog.
from audio_recorder_streamlit import audio_recorder

# Base64 used to handle audio byte strings.
import base64

# Eleven labs is used for generating realistic sound speech.
from elevenlabs import generate, play, Voices
from elevenlabs import set_api_key
from elevenlabs.api import Voices

# Time is used to sleep, so that audio can finish playing, before st 
# does a re run. 
import time

# Audio helper functions used for the dialog.
from st_helpers.audio_helpers import load_eleven_labs_voice
from st_helpers.audio_helpers import autoplay_audio_from_bytes
from st_helpers.audio_helpers import get_audio_duration
from st_helpers.audio_helpers import generate_eleven_labs_audio 


# Instantiating ElevenLabs voice.
my_voice = load_eleven_labs_voice()


# Audio recording button. Have to set key manually, so widgets do not 
# conflict with eachother.
audio_bytes = audio_recorder(
        key="123", 
        icon_name="microphone",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        text=""
)


# Check if the session state has the 'processed' attribute
if not hasattr(st.session_state, 'processed'):
    st.session_state.processed = False


# Only process if the 'processed' flag is not set
if audio_bytes and not st.session_state.processed:
    response = "My response."


    audio = generate_eleven_labs_audio(response, my_voice)
    
    
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

   
