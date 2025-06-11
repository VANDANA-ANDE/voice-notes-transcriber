from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk

# Load .env variables
load_dotenv()

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SPEECH_REGION")

# Configure speech service
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Configure audio input (use microphone OR audio file)

# Option A: Microphone live transcription
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Option B: From audio file (replace with your file)
# audio_config = speechsdk.audio.AudioConfig(filename="your_audio_file.wav")

# Create recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Perform recognition
print("Speak into your microphone...")
result = speech_recognizer.recognize_once()

# Display result
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized")
else:
    print("Error: {}".format(result.reason))


# Key = ABTx4gIp9SV86nKEFiDlh8E7GeZJvZxCgpgOTaaNUmYqYLse5BFUJQQJ99BFACYeBjFXJ3w3AAAYACOGpqXY
# region = eastus
