import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe an audio file using the OpenAI speech-to-text API.
    """

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )

    return transcription.text


def transcribe_full_audio(audio_path: str) -> str:
    """
    Split a large audio file into chunks, transcribe each chunk,
    and combine the transcripts.
    """

    from src.audio import split_audio

    chunks = split_audio(audio_path)

    transcripts = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nTranscribing chunk {i}/{len(chunks)}...")

        transcript = transcribe_audio(chunk)

        transcripts.append(transcript)

    return "\n".join(transcripts)