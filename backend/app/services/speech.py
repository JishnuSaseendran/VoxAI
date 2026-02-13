import io
import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from fastapi import HTTPException
from pydub import AudioSegment

recognizer = sr.Recognizer()

# Supported input formats (pydub/ffmpeg supports many more)
SUPPORTED_FORMATS = [
    'webm', 'mp3', 'mp4', 'm4a', 'ogg', 'oga', 'flac', 'wav', 'aiff', 'aac', 'wma', 'opus'
]


def convert_to_wav(input_path: str) -> str:
    """
    Convert any audio file to WAV format for speech recognition.
    Supports: webm, mp3, mp4, m4a, ogg, flac, wav, aiff, aac, wma, opus, etc.
    """
    try:
        # Get file extension
        ext = os.path.splitext(input_path)[1].lower().lstrip('.')

        # pydub auto-detects format, but we can help it for some formats
        if ext in ['webm', 'ogg', 'opus']:
            audio = AudioSegment.from_file(input_path, format=ext)
        elif ext == 'm4a':
            audio = AudioSegment.from_file(input_path, format='m4a')
        elif ext == 'mp4':
            audio = AudioSegment.from_file(input_path, format='mp4')
        else:
            # Let pydub auto-detect
            audio = AudioSegment.from_file(input_path)

        # Convert to mono and set sample rate for better recognition
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Export as WAV
        wav_path = tempfile.mktemp(suffix='.wav')
        audio.export(wav_path, format='wav')
        return wav_path

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Audio conversion failed. Ensure ffmpeg is installed. Error: {str(e)}"
        )


def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file to text using Google Speech Recognition.
    Automatically converts any audio format to WAV first.
    """
    wav_path = None
    try:
        # Convert to WAV format
        wav_path = convert_to_wav(audio_file_path)

        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand audio. Please speak clearly.")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Speech recognition service error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    finally:
        # Cleanup converted file
        if wav_path and os.path.exists(wav_path):
            try:
                os.unlink(wav_path)
            except:
                pass


def text_to_speech(text: str) -> io.BytesIO:
    """Convert text to speech and return audio bytes."""
    tts = gTTS(text=text, lang="en")
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer
