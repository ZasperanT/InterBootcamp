import json
from pathlib import Path

from src.pipeline import verify_meeting_record
from src.documentation import regenerate_meeting_record


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
# Deliberately create a bad candidate record
# --------------------------------------------------

meeting_record = {
    "meeting_summary": (
        "The team discussed designing a new remote control."
    ),

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
# Run verification + regeneration loop
# --------------------------------------------------

max_attempts = 2

for attempt in range(1, max_attempts + 1):

    print("\n" + "=" * 60)
    print(
        f"VERIFICATION ATTEMPT "
        f"{attempt}/{max_attempts}"
    )
    print("=" * 60)

    verification = verify_meeting_record(
        transcript,
        meeting_record
    )

    for result in verification["claims"]:
        print(
            f"{result['claim_id']}: "
            f"{result['status']}"
        )

    has_problem = any(
        result["status"] in {
            "uncertain",
            "contradicted"
        }
        for result in verification["claims"]
    )

    if not has_problem:
        print("\nAll claims are supported.")
        break

    if attempt == max_attempts:
        print(
            "\nMaximum attempts reached."
        )
        break

    print(
        "\nUnsupported/contradicted claims found."
    )
    print(
        "Regenerating meeting record..."
    )

    meeting_record = regenerate_meeting_record(
        transcript,
        meeting_record,
        verification
    )


# --------------------------------------------------
# Display final record
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL RECORD")
print("=" * 60)

print(
    json.dumps(
        meeting_record,
        indent=4,
        ensure_ascii=False
    )
)