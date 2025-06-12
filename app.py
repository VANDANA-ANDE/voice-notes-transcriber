import streamlit as st
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import tempfile

# Load Azure keys from .env
load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SPEECH_REGION")

# Streamlit UI
st.set_page_config(page_title="AI Voice Notes Transcriber", page_icon="🎙️")
st.title("🎙️ AI Voice Notes Transcriber")
st.write("Upload a .wav or .mp3 file to transcribe it using Azure Speech Service.")

# File uploader
uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Azure speech setup
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=tmp_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    st.info("Transcribing... please wait ⏳")
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        transcript = result.text
        st.success("✅ Transcription Complete!")
        st.text_area("📝 Transcription Result:", transcript, height=200)
        
        # Download button
        st.download_button("📥 Download Transcript", data=transcript, file_name="transcript.txt")
    else:
        st.error(f"❌ Transcription failed: {result.reason}")
