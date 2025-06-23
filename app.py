import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
from io import BytesIO
from fpdf import FPDF

load_dotenv()

speech_key = st.secrets["SPEECH_KEY"]
service_region = st.secrets["SPEECH_REGION"]
# DEBUG: Show partial keys (remove after testing)
st.write("Speech Key (partial):", speech_key[:5] + "...")
st.write("Service Region:", service_region)

st.set_page_config(
    page_title="AI Voice Notes Transcriber",
    page_icon="🎙️",
    layout="wide",  # Use wide layout for columns
)
st.markdown(
    """
    <style>
    /* Target main app container background */
    .css-1d391kg, .css-18e3th9 {
        background-color: #FFF8DC !important;  /* Cornsilk pastel */
    }
    /* Set text color globally */
    .css-1d391kg, .css-18e3th9, .css-1v3fvcr {
        color: #5D576B !important;  /* Muted purple */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #6B8E23 !important;  /* Olive green */
    }
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #E6E6FA !important;  /* Lavender pastel */
        color: #5D576B !important;
    }
    /* File uploader box */
    .stFileUploader > div {
        background: #F0EAD6 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    /* Buttons */
    button {
        background-color: #B0E0E6 !important;  /* Powder blue pastel */
        color: #4B515D !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🎙️ AI Voice Notes Transcriber</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Transcribe your voice notes to text using Azure Speech Services</p>",
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("📌 How to Use")
    st.write("1. Upload a `.wav` or `.mp3` audio file.")
    st.write("2. Wait for the transcription to complete.")
    st.write("3. Copy or download the transcribed text.")

st.markdown("---")

uploaded_file = st.file_uploader("📤 Upload Audio File (.wav or .mp3)", type=["wav", "mp3"])

if uploaded_file:

    # Columns: Left for upload & audio player, Right for transcript
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write(f"**Uploaded file:** {uploaded_file.name}")

        # Audio playback
        st.audio(uploaded_file, format="audio/wav")  # Works for wav/mp3 automatically

    # Save temp file for Azure recognition
    with open("temp_audio", "wb") as f:
        f.write(uploaded_file.read())

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_input = speechsdk.AudioConfig(filename="temp_audio")
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    with col2:
        # Progress bar & status indicator
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("🎤 Starting transcription...")
        progress_bar.progress(10)

        result = recognizer.recognize_once()

        progress_bar.progress(100)
        status_text.text("")

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            transcript = result.text
            st.success("✅ Transcription complete!")
            st.balloons()

            # Text area to show transcript
            st.text_area("📝 Transcribed Text", value=transcript, height=250)

            # PDF download helper function
            def create_pdf(text):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in text.split('\n'):
                    pdf.cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
                pdf_output = BytesIO()
                pdf.output(pdf_output)
                pdf_output.seek(0)
                return pdf_output

            pdf_file = create_pdf(transcript)

            st.download_button(
                label="📥 Download Transcript as TXT",
                data=transcript,
                file_name=f"{uploaded_file.name.split('.')[0]}_transcript.txt",
                mime="text/plain"
            )

            st.download_button(
                label="📥 Download Transcript as PDF",
                data=pdf_file,
                file_name=f"{uploaded_file.name.split('.')[0]}_transcript.pdf",
                mime="application/pdf"
            )
        elif result.reason == speechsdk.ResultReason.NoMatch:
            st.error("⚠️ Speech could not be recognized. Try another file.")
        else:
            st.error(f"❌ Error during transcription: {result.reason}")

    # Clean up temp file
    try:
        os.remove("temp_audio")
    except Exception:
        pass

else:
    st.info("⬆️ Please upload an audio file to get started.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color: gray;'>Made with ❤️ by Vandana Ande | "
    "<a href='https://github.com/your-username' target='_blank'>GitHub</a></p>",
    unsafe_allow_html=True,
)
