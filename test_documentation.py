import json
from pathlib import Path

from src.documentation import generate_meeting_record


# Load refined transcript
transcript_path = Path("outputs/refined_transcript.txt")

with open(transcript_path, "r", encoding="utf-8") as file:
    refined_transcript = file.read()


print("Refined transcript loaded.")
print(f"Characters: {len(refined_transcript)}")


# Generate meeting record
print("\nSending transcript to documentation LLM...")

meeting_record = generate_meeting_record(refined_transcript)


# Save structured JSON
output_path = Path("outputs/meeting_record.json")

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(meeting_record, file, indent=4, ensure_ascii=False)


print("\nMeeting record generated.")
print(f"Saved to: {output_path}")

print("\n--- MEETING RECORD ---")
print(json.dumps(meeting_record, indent=4, ensure_ascii=False))