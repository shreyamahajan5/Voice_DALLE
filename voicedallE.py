import streamlit as st
from PIL import Image
import requests
from audio_recorder_streamlit import audio_recorder
import whisper

st.title("Voice-enabled DALL-E Image Generator")

# Initialize Whisper ASR model
whisper_model = whisper.load_model("base")

# Initialize DALL-E API endpoint (modify this to your DALL-E endpoint)
dalle_endpoint = "https://api.openai.com/v1/images/generations"
dalle_api_key = "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"

# Initialize variables
transcription = ""
text_prompt = ""

# Function to transcribe audio
def transcribe_audio(audio_data):
    try:
        result = whisper_model.transcribe(audio_data)
        transcription = result["text"]
        st.write("Transcription: " + transcription)
        return transcription
    except Exception as e:
        st.error("Transcription error: " + str(e))
        return None

# Function to generate an image using DALL-E
def generate_image(prompt, api_key):
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "256x256"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(dalle_endpoint, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        # Access the image URL from the response data
        image_url = response_data['data'][0]['url']
        return image_url
    except requests.exceptions.RequestException as e:
        st.error(f"Image generation error: {e}")
        return None

# Add separate options for text and audio prompts
text_prompt = st.text_input("Enter a text prompt")
if st.button("Generate Image from Text Prompt") and text_prompt:
    with st.spinner("Generating Image..."):
        generated_image_url = generate_image(text_prompt, dalle_api_key)
        if generated_image_url:
            st.image(Image.open(requests.get(generated_image_url, stream=True).raw))
        else:
            st.error("Image generation error. Check your DALL-E API key and endpoint.")

if st.button("Record Audio"):
    audio_data = audio_recorder("Click to record", "Click to stop recording")
    print("Recorded audio data:", audio_data)  # Debugging print statement
    if audio_data:
        transcription = transcribe_audio(audio_data)
        print("Transcription result:", transcription)  # Debugging print statement

if transcription:
    if st.button("Generate Image from Audio"):
        with st.spinner("Generating Image..."):
            generated_image_url = generate_image(transcription, dalle_api_key)
            if generated_image_url:
                st.image(Image.open(requests.get(generated_image_url, stream=True).raw))
            else:
                st.error("Image generation error. Check your DALL-E API key and endpoint.")
