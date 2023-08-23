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
from st_helpers.audio_helpers import set_open_ai_token 
from st_helpers.audio_helpers import get_chat_gpt_response  

# Open AI used for whisper and chat GPT.
import openai

DIALOG = []

set_open_ai_token()

 # Instantiating ElevenLabs voice.
my_voice = load_eleven_labs_voice()


def main():
    """
    Runs dialog after password is confirmed.
    """
    
    password_placeholder = st.empty()

    if not hasattr(st.session_state, 'password_validated'):
        st.session_state.password_validated = False

    if not st.session_state.password_validated:
        user_input = password_placeholder.text_input("Enter Password", type="password")

    if user_input == st.secrets["DEVA_USER_PW"] or st.session_state.password_validated:
        st.session_state.password_validated = True
        password_placeholder.empty()
        # If the password is correct, then the dialog can start.

        st.write("Press the button below to record audio.")
        # Audio recording button. Have to set key manually, so widgets 
        # do not conflict with eachother.
        audio_bytes = audio_recorder(
                key="123", 
                icon_name="square",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                text=""
        )
           

        # Check if the session state has the 'processed' attribute
        if not hasattr(st.session_state, 'processed'):
            st.session_state.processed = False


        # Only process if the 'processed' flag is not set
        if audio_bytes and not st.session_state.processed:
            
            # Writing audio bytes to the file
            with open("TTS.wav", mode="wb") as f:
                f.write(audio_bytes)

            # Reading from the file and translating
            with open("TTS.wav", mode="rb") as f:  
                response = openai.Audio.translate("whisper-1", f)["text"]
            
            
            # Creating audio byte string.

            DIALOG.append({"user": response})

            # st.chat_input(response)
            # Generate GPP response:

            chatbot_response = get_chat_gpt_response(response)
     
            DIALOG.append({"chat_bot": chatbot_response})

            # st.chat_message(chatbot_response)

            audio = generate_eleven_labs_audio(chatbot_response, my_voice)
            

            st.write(DIALOG)

            # Custom auto play function, made for streamlit.   
            autoplay_audio_from_bytes(audio)
           
            # Convert audio bytes into .wav.
            with open('STT.wav', mode='wb') as f:
                f.write(audio)

            # Sleep time is used, so that st does not re run until audio is 
            # finished playing.
            sleep_time = get_audio_duration("STT.wav")

            time.sleep(sleep_time)

            # Set the 'processed' flag
            st.session_state.processed = True

            # Rerun the app
            st.experimental_rerun()


        # Reset audio_bytes and processed flag for the next interaction
        audio_bytes = None
        st.session_state.processed = False


if __name__ == "__main__":
    main()


