import json
from pathlib import Path

from src.evidence import segment_transcript
from src.evidence_retrieval import retrieve_evidence
from src.claim_extraction import extract_claims


# -------------------------
# Load transcript
# -------------------------

transcript_path = Path(
    "outputs/refined_transcript.txt"
)

with open(
    transcript_path,
    "r",
    encoding="utf-8"
) as file:

    transcript = file.read()


# -------------------------
# Create evidence segments
# -------------------------

segments = segment_transcript(
    transcript
)


# -------------------------
# Load meeting record
# -------------------------

record_path = Path(
    "outputs/meeting_record.json"
)

with open(
    record_path,
    "r",
    encoding="utf-8"
) as file:

    meeting_record = json.load(file)


# -------------------------
# Extract claims
# -------------------------

claims = extract_claims(
    meeting_record
)


# -------------------------
# Retrieve evidence
# -------------------------

for claim in claims:

    print("\n" + "=" * 60)

    print(
        f"CLAIM: {claim['claim_id']}"
    )

    print(
        f"Task: {claim['task']}"
    )

    print(
        f"Owner: {claim['owner']}"
    )

    print(
        f"Deadline: {claim['deadline']}"
    )

    print("\nRETRIEVED EVIDENCE:")

    evidence = retrieve_evidence(
        claim,
        segments,
        top_k=3
    )

    for item in evidence:

        print(
            f"\n[{item['segment_id']}] "
            f"score={item['score']:.3f}"
        )

        print(item["text"])