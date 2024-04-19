import os
from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import streamlit as st

# Text-to-speech function (improved for efficiency and clarity)
def text_to_speech(text):
    """
    Converts text to speech (TTS) and plays the generated audio.

    Args:
        text (str): The text to be converted to speech.

    Returns:
        None
    """

    filename = 'ai_voice.mp3'  # Consistent filename throughout the code

    # Check if the audio file already exists and remove it (if so)
    if os.path.exists(filename):
        os.remove(filename)

    # Generate speech using gTTS
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    # Play the generated audio using playsound
    playsound(filename)

    # Remove the generated audio file
    os.remove(filename)

# Speech-to-text function
def get_audio():
    """
    Captures audio input using a microphone and converts it to text.

    Returns:
        tuple: A tuple containing the recognized text and any potential error message.
    """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Record audio input
        audio = r.listen(source)

        try:
            # Attempt to recognize the audio using Google Speech Recognition
            said = r.recognize_google(audio)
            return said, None
        except Exception as e:
            error_message = f"Speech recognition error: {e}"
            return "", error_message

# Streamlit Integration (if applicable)
if __name__ == "__main__":  # Wrap Streamlit integration in a conditional block
    st.title("Text-to-Speech and Speech-to-Text Demo")

    text_input = st.text_input("Enter text to convert to speech:")
    if text_input:
        text_to_speech(text_input)

    if st.button("Record Audio"):
        st.write("Listening for audio input...")
        recognized_text, error_message = get_audio()
        if recognized_text:
            st.write("You said:", recognized_text)
        else:
            st.write("Speech recognition failed.")
            if error_message:
                st.write("Error:", error_message)
