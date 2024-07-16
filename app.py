import os
import time
from typing import Any
from pathlib import Path

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from transformers import pipeline

from utils.custom import css_code

client = OpenAI()


st.set_page_config(page_title="IMAGE TO STORY CONVERTER", page_icon="🖼️")

# Load environment variables
dotenv_path = find_dotenv()
if dotenv_path == "":
    st.error("Error: .env file not found.")
else:
    st.write(f".env file found at: {dotenv_path}")

load_dotenv(dotenv_path)

# Getting APIs
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = "sk-proj-SJ428u2MA62d8rYkXZaCT3BlbkFJxZApdSlHZJdVz9HGXJjx"
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
else:
    st.write("OpenAI API key loaded correctly.")
if not HUGGINGFACE_API_TOKEN:
    st.error("Hugging Face API token not found. Please set HUGGINGFACE_API_TOKEN in your environment variables.")
else:
    st.write("Hugging Face API token loaded correctly.")


# For progress bar
def progress_bar(amount_of_time: int) -> Any:
    """
    A very simple progress bar that increases over time,
    then disappears when it reaches completion
    :param amount_of_time: time taken
    :return: None
    """
    progress_text = "Please wait, Generative models hard at work"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(amount_of_time):
        time.sleep(0.04)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()


# For text-to-image generation
def generate_text_from_image(url: str) -> str:
    """
    A function that uses the BLIP model to generate text from an image.
    parameter - image location (url)
    returns - generated text from the image
    """
    image_to_text: Any = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

    try:
        generated_text: str = image_to_text(url)[0]["generated_text"]
        st.write(f"Generated Text: {generated_text}")
        return generated_text
    except Exception as e:
        st.error(f"Error generating text from image: {e}")
        return ""


# For generating story from image text
def generate_story_from_text(scenario: str) -> str:
    """
    A function using LangChain to generate a short story.
    parameter - generated text from the image (scenario)
    returns - generated story from the text
    """

    prompt_template = """
    You are a talented storyteller who can create a story from a simple narrative.
    Create a story using the following scenario; the story should be maximum 50 words long:

    CONTEXT: {scenario}
    STORY:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["scenario"])
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9, api_key=OPENAI_API_KEY)
    story_llm = LLMChain(llm=llm, prompt=prompt, verbose=True)

    try:
        generated_story = story_llm.predict(scenario=scenario)
        st.write(f"Generated Story: {generated_story}")
        return generated_story
    except Exception as e:
        st.error(f"Error generating story from text: {e}")
        return ""


def generate_speech_from_text(message: str) -> None:
    """
    A function using text to speech model from HuggingFace
    parameter - short story generated by the GPT model
    returns - generated audio from the short story
    """

    try:
        response = client.audio.speech.create(
            model="text-to-speech",
            voice="alloy",
            input=message,
        )
        audio_url = response["data"]["url"]
        st.audio(audio_url)
    except Exception as e:
        st.error(f"Error generating speech from text: {e}")



def main() -> None:
    st.markdown(css_code, unsafe_allow_html=True)

    with st.sidebar:
        st.image("cover.png")
        st.write("AI App created by @ Arushi Bhagat")

    st.header("Image-to-Story Converter")
    uploaded_file: Any = st.file_uploader("Please choose a file to upload", type="jpg")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        bytes_data: Any = uploaded_file.getvalue()
        with open(uploaded_file.name, "wb") as file:
            file.write(bytes_data)

        progress_bar(100)

        scenario: str = generate_text_from_image(uploaded_file.name)
        if scenario:
            story: str = generate_story_from_text(scenario)
            if story:
                generate_speech_from_text(story)

                with st.expander("Generated Image scenario"):
                    st.write(scenario)
                with st.expander("Generated short story"):
                    st.write(story)

if __name__ == "__main__":
    main()
