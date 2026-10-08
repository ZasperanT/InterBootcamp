from pathlib import Path

from src.evidence import segment_transcript
from src.evidence_retrieval import retrieve_evidence
from src.consistency import validate_claim


transcript_path = Path("outputs/refined_transcript.txt")

with open(transcript_path, "r", encoding="utf-8") as file:
    transcript = file.read()

segments = segment_transcript(transcript)


false_claim = {
    "claim_id": "fake_decision_001",
    "claim_type": "decision",
    "decision": "The team decided to use a touchscreen remote."
}


evidence = retrieve_evidence(
    false_claim,
    segments,
    top_k=10
)


result = validate_claim(
    false_claim,
    evidence
)


print("\n" + "=" * 60)
print("FALSE CLAIM TEST")
print("=" * 60)

print(f"\nClaim:")
print(false_claim["decision"])

print(f"\nStatus:")
print(result["status"])

print(f"\nReason:")
print(result["reason"])

print("\nRetrieved Evidence:")

for item in evidence:
    print(
        f"\n[{item['segment_id']}] "
        f"score={item['score']:.3f}"
    )
    print(item["text"])