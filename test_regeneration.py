import json
from pathlib import Path

from src.documentation import regenerate_meeting_record
from src.pipeline import verify_meeting_record


# --------------------------------------------------
# Load existing refined transcript
# --------------------------------------------------

transcript_path = Path(
    "outputs/refined_transcript.txt"
)

with open(
    transcript_path,
    "r",
    encoding="utf-8"
) as file:
    transcript = file.read()


# --------------------------------------------------
# Create an intentionally incorrect candidate record
# --------------------------------------------------

candidate_record = {
    "meeting_summary": "The team discussed the design of a new remote control.",

    "topics_discussed": [
        "Remote control design",
        "Touchscreen functionality"
    ],

    "key_decisions": [
        {
            "decision": (
                "The team decided to use a touchscreen remote."
            )
        }
    ],

    "action_items": []
}


# --------------------------------------------------
# Verify the intentionally incorrect record
# --------------------------------------------------

verification = verify_meeting_record(
    transcript,
    candidate_record
)


print("\n" + "=" * 60)
print("INITIAL VERIFICATION")
print("=" * 60)

for result in verification["claims"]:
    print(
        f"\n{result['claim_id']}: "
        f"{result['status']}"
    )

    print(result["reason"])


# --------------------------------------------------
# Regenerate the record
# --------------------------------------------------

print("\n" + "=" * 60)
print("REGENERATING MEETING RECORD")
print("=" * 60)

corrected_record = regenerate_meeting_record(
    transcript,
    candidate_record,
    verification
)


# --------------------------------------------------
# Display corrected record
# --------------------------------------------------

print("\n" + "=" * 60)
print("CORRECTED RECORD")
print("=" * 60)

print(
    json.dumps(
        corrected_record,
        indent=4,
        ensure_ascii=False
    )
)