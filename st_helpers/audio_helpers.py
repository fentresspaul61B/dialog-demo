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

from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI

import os

CONTEXT_PROMPT = """You are a helpful assistant."""


template = """The following is a friendly conversation between a human and an AI. The AI is not talkative, and gives concise questions and answers. 
If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{history}

Conversation:
Human: {input}
AI:"""


def create_lang_chain_prompt(
        patient_name: str,
        patient_story: str
    ):
    
    prompt = f"""The following is a friendly conversation between a human and an AI. The AI is not talkative, and gives concise questions and answers. In this conversation the AI is role playing as a compassionate caregiver, who is having a conversation with a Dementia patient named {patient_name}.

The AI's objective is to lead an engaging conversation, by asking {patient_name} about their life and experiences.  

Here is some background information about {patient_name} that you should use to ask engaging questions for your conversation. 

{patient_story}

Some important rules the AI must follow:
    - Only ask one question at a time. 
    - Keep questions short and concise.
    - Do not ask how you can assist them, but lead the conversation by asking them about their life.   

If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

Relevant Information:

{{history}}

Conversation:
Human: {{input}}
AI:"""
    return prompt



@st.cache_data()
def configure_lang_chain(template=template):

    llm = ChatOpenAI(
        model_name='gpt-4',
        temperature=0,
        max_tokens = 256
    )

    prompt = PromptTemplate(
        input_variables=["history", "input"], template=template
    )

    summary_memory = ConversationSummaryMemory(llm=llm)

    conversation = ConversationChain(
        llm=llm,
        verbose=False,
        memory=summary_memory,
        prompt=prompt
    )

    return conversation


def get_chat_lang_chain_response(text, lang_chain_conversation):
    """
    Calls the chat GPT API with context.
    """

    response = lang_chain_conversation.predict(input=text)

    return response



def get_chat_gpt_response(prompt, context=CONTEXT_PROMPT):
    """
    Calls the chat GPT API with context.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response['choices'][0]["message"]["content"]


@st.cache_data()
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
    os.environ['OPENAI_API_KEY'] = OPEN_AI_TOKEN 


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




def main():
    print(create_lang_chain_prompt("Paul", "Pauls older."))

if __name__ == "__main__":
    main()
