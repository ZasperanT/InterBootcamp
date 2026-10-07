from pathlib import Path

from src.refinement import refine_transcript


# Load the raw transcript
raw_transcript_path = Path("outputs/raw_transcript.txt")

with open(raw_transcript_path, "r", encoding="utf-8") as file:
    raw_transcript = file.read()


print("Raw transcript loaded.")
print(f"Characters: {len(raw_transcript)}")


# Refine the transcript
print("\nSending transcript to refinement LLM...")

refined_transcript = refine_transcript(raw_transcript)


# Save refined transcript
output_path = Path("outputs/refined_transcript.txt")

with open(output_path, "w", encoding="utf-8") as file:
    file.write(refined_transcript)


print("\nRefinement complete.")
print(f"Refined transcript saved to: {output_path}")
print(f"Characters: {len(refined_transcript)}")