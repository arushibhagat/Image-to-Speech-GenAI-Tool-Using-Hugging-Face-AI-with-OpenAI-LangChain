# Image-to-Speech-GenAI-Tool-Using-Hugging-Face-AI-with-OpenAI-LangChain
This is an AI tool that generates an Audio short story based on the context of an uploaded image by prompting a GenAI LLM model, Hugging Face AI models together with OpenAI & LangChain. Deployed on Streamlit.

## Introduction
This is an AI app which executes in three parts:

1. Image to text: an image-to-text transformer model (Salesforce/blip-image-captioning-base) is used to generate a text scenario based on the on the AI understanding of the image context
2. Text to story: OpenAI LLM model is prompted to create a short story (50 words: can be adjusted as reqd.) based on the generated scenario. gpt-3.5-turbo
3. Story to speech: a text-to-speech model (OpenAI Text-To-Speech) is used to convert the generated short story into a voice-narrated audio file

A user interface is built using streamlit to enable uploading the image and playing the audio file.

## Deployment on Streamlit
[Run here on Streamlit](https://image-to-speech-genai-tool.streamlit.app/)

![outputSS](https://github.com/user-attachments/assets/470ed04c-8311-418a-a26c-f3af6c7b327c)

