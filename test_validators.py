from src.validators import validate_audio_file


audio_path = "ES2002a.Mix-Headset.wav"

try:
    validate_audio_file(audio_path)
    print("Audio validation successful.")

except ValueError as error:
    print(f"Validation failed: {error}")