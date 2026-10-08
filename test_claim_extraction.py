import json
from pathlib import Path

from src.claim_extraction import extract_claims


record_path = Path(
    "outputs/meeting_record.json"
)

with open(
    record_path,
    "r",
    encoding="utf-8"
) as file:

    meeting_record = json.load(file)


claims = extract_claims(meeting_record)


print(f"Number of claims: {len(claims)}")

print("\n--- CLAIMS ---")

for claim in claims:

    print(f"\n[{claim['claim_id']}]")
    print(f"Type: {claim['claim_type']}")

    if claim["claim_type"] == "decision":

        print(f"Decision: {claim['decision']}")

    elif claim["claim_type"] == "action_item":

        print(f"Task: {claim['task']}")
        print(f"Owner: {claim['owner']}")
        print(f"Deadline: {claim['deadline']}")