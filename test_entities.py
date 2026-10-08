from pathlib import Path

from src.entities import extract_person_roles


transcript_path = Path("outputs/refined_transcript.txt")

with open(transcript_path, "r", encoding="utf-8") as file:
    transcript = file.read()


relationships = extract_person_roles(transcript)


print("\n" + "=" * 60)
print("PERSON → ROLE RELATIONSHIPS")
print("=" * 60)

for relationship in relationships:
    print(
        f"{relationship['person']} → "
        f"{relationship['role']}"
    )