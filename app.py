import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import tempfile

# Load Azure credentials from .env
load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
speech_region = os.getenv("SPEECH_REGION")

# Configure Azure Speech
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

st.set_page_config(page_title="Voice Notes Transcriber", page_icon="🗣️")

st.title("🎙️ AI Voice Notes Transcriber")
st.write("Upload your audio file (.wav or .mp3) and get the transcript using Azure AI.")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])

if uploaded_file:
    st.audio(uploaded_file, format='audio/wav')

    if st.button("Transcribe"):
        with st.spinner("Transcribing... Please wait"):
            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_filename = tmp_file.name

            # Setup audio config
            audio_config = speechsdk.audio.AudioConfig(filename=tmp_filename)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            result = speech_recognizer.recognize_once()

            # Delete temp file after use
            os.remove(tmp_filename)

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                st.success("✅ Transcription Successful!")
                st.text_area("Transcribed Text", result.text, height=200)

                # Download option
                st.download_button("Download Transcript", result.text, file_name="transcript.txt")
            else:
                st.error("❌ Could not transcribe. Please try another file.")
