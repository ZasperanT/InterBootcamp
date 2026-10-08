import json
from pathlib import Path

from src.evidence import segment_transcript
from src.evidence_retrieval import retrieve_evidence
from src.claim_extraction import extract_claims
from src.consistency import validate_claim
from src.entities import extract_person_roles


# --------------------------------------------------
# 1. Load refined transcript
# --------------------------------------------------

transcript_path = Path("outputs/refined_transcript.txt")

with open(transcript_path, "r", encoding="utf-8") as file:
    transcript = file.read()


# --------------------------------------------------
# 2. Split transcript into evidence segments
# --------------------------------------------------

segments = segment_transcript(transcript)


# --------------------------------------------------
# 3. Extract person → role relationships
# --------------------------------------------------

person_roles = extract_person_roles(transcript)

print("\n" + "=" * 60)
print("PERSON → ROLE RELATIONSHIPS")
print("=" * 60)

for relationship in person_roles:
    print(
        f"{relationship['person']} → "
        f"{relationship['role']}"
    )


# --------------------------------------------------
# 4. Load candidate meeting record
# --------------------------------------------------

record_path = Path("outputs/meeting_record.json")

with open(record_path, "r", encoding="utf-8") as file:
    meeting_record = json.load(file)


# --------------------------------------------------
# 5. Extract claims from meeting record
# --------------------------------------------------

claims = extract_claims(meeting_record)


# --------------------------------------------------
# 6. Retrieve evidence and validate each claim
# --------------------------------------------------

for claim in claims:

    evidence = retrieve_evidence(
        claim,
        segments,
        top_k=3
    )

    result = validate_claim(
        claim,
        evidence,
        person_roles
    )

    print("\n" + "=" * 60)
    print(f"CLAIM: {claim['claim_id']}")

    if claim["claim_type"] == "action_item":
        print(f"Task: {claim['task']}")
        print(f"Owner: {claim['owner']}")
        print(f"Deadline: {claim['deadline']}")

    elif claim["claim_type"] == "decision":
        print(f"Decision: {claim['decision']}")

    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")

    print("\nEvidence:")

    for item in result["evidence"]:
        print(
            f"- {item['segment_id']} "
            f"(score={item['score']:.3f})"
        )