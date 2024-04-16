import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

import os

# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

# Initialize the recognizer
r = sr.Recognizer()

def transcribe_audio(audio_file):
    # Use the audio file as the audio source
    with sr.AudioFile(audio_file) as source:
        # Listen for the data (load audio to memory)
        audio_data = r.record(source)
        # Recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
            print(f"Transcription: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def extract_audio(video_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = "extracted_audio.wav"
    audio.write_audiofile(audio_file)
    return audio_file

def process_file(file_path):
    # Check the file extension
    _, file_extension = os.path.splitext(file_path)
    if file_extension in ['.wav', '.mp3']:
        return transcribe_audio(file_path)
    elif file_extension in ['.mp4', '.avi']:
        audio_file = extract_audio(file_path)
        text = transcribe_audio(audio_file)
        # Delete the extracted audio file
        os.remove(audio_file)
        return text
    else:
        return "Unsupported file type"