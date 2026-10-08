from pathlib import Path

from src.evidence import segment_transcript


transcript_path = Path(
    "outputs/refined_transcript.txt"
)

with open(
    transcript_path,
    "r",
    encoding="utf-8"
) as file:

    transcript = file.read()


segments = segment_transcript(transcript)


print(f"Transcript characters: {len(transcript)}")
print(f"Number of segments: {len(segments)}")

print("\n--- FIRST 5 SEGMENTS ---")

for segment in segments[:5]:

    print(f"\n[{segment['segment_id']}]")
    print(segment["text"])