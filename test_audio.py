from src.audio import get_audio_duration, split_audio


audio_path = "ES2002a.Mix-Headset.wav"

duration = get_audio_duration(audio_path)

print(f"Audio duration: {duration:.2f} seconds")
print(f"Audio duration: {duration / 60:.2f} minutes")


chunks = split_audio(audio_path)

print("\nGenerated chunks:")

for chunk in chunks:
    print(chunk)