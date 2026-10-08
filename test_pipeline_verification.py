import json
from pathlib import Path

from src.pipeline import verify_meeting_record


transcript_path = Path(
    "outputs/refined_transcript.txt"
)

record_path = Path(
    "outputs/meeting_record.json"
)


with open(
    transcript_path,
    "r",
    encoding="utf-8"
) as file:
    transcript = file.read()


with open(
    record_path,
    "r",
    encoding="utf-8"
) as file:
    meeting_record = json.load(file)


verification = verify_meeting_record(
    transcript,
    meeting_record
)


print("\n" + "=" * 60)
print("VERIFICATION TEST")
print("=" * 60)


print("\nPERSON → ROLE")

for relationship in verification["person_roles"]:
    print(
        f"{relationship['person']} → "
        f"{relationship['role']}"
    )


print("\nCLAIMS")

for result in verification["claims"]:

    print("\n" + "-" * 60)

    print(
        f"Claim: {result['claim_id']}"
    )

    print(
        f"Status: {result['status']}"
    )

    print(
        f"Reason: {result['reason']}"
    )

    print("Evidence:")

    for evidence in result["evidence"]:
        print(
            f"  - {evidence['segment_id']} "
            f"(score={evidence['score']:.3f})"
        )