# 🎙️ AI Voice Notes Transcriber

A simple and powerful web app to transcribe voice notes into text using **Azure Speech Services**. Upload an audio file (.wav/.mp3) and get accurate, fast transcription in seconds.

---

## 🚀 Features

- 🎧 Upload `.wav` or `.mp3` files
- 💬 Transcribe audio using Azure Cognitive Services
- 📄 View and edit the transcribed text
- 📥 Download transcription as `.txt`
- 🌐 Built with **Streamlit** for a clean web interface

---

---

## 🧠 Tech Stack

- [Azure Speech-to-Text](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [GitHub](https://github.com)

---

## 🛠️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/your-username/voice-notes-transcriber.git
cd voice-notes-transcriber

Create .env file

Inside the project folder, create a .env file:


SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=your_azure_region
Install dependencies


pip install -r requirements.txt
Run the app


streamlit run app.py

📂 Project Structure


voice-notes-transcriber/
├── app.py               # Main Streamlit app
├── .env                 # Secrets (Azure keys)
├── requirements.txt     # Dependencies
├── README.md            # Project readme
└── screenshot.png       # App screenshot (optional)
