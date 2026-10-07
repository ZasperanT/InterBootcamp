from pathlib import Path

from src.transcription import transcribe_full_audio


audio_path = "ES2002a.Mix-Headset.wav"

transcript = transcribe_full_audio(audio_path)


# Create outputs directory
output_dir = Path("outputs")
output_dir.mkdir(parents=True, exist_ok=True)


# Save raw transcript
raw_transcript_path = output_dir / "raw_transcript.txt"

with open(raw_transcript_path, "w", encoding="utf-8") as file:
    file.write(transcript)


print("\n--- TRANSCRIPT CHARACTER COUNT ---")
print(len(transcript))

print("\n--- RAW TRANSCRIPT SAVED TO ---")
print(raw_transcript_path)