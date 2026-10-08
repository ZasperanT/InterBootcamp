import re
from src.entities import extract_person_roles

ASSIGNMENT_PHRASES = [
    "you're going to",
    "you are going to",
    "you'll be",
    "you will be",
    "you'll",
    "you will",
    "assigned",
    "responsible for",
]


def tokenize(text: str) -> set[str]:
    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    stopwords = {
        "the", "a", "an", "and", "or", "to", "of",
        "in", "on", "for", "with", "is", "are",
        "was", "were", "be", "before", "after",
        "will", "would", "should", "this", "that",
        "it", "as", "by", "from", "at", "you",
        "your", "their", "they", "he", "she",
        "we", "our"
    }

    return {
        word
        for word in words
        if word not in stopwords
    }

def roles_match(owner_role: str, evidence_text: str) -> bool:
    """
    Check whether a person's stated role is represented
    in the evidence, allowing small wording differences.
    """

    role_words = tokenize(owner_role)
    evidence_words = tokenize(evidence_text)

    if not role_words:
        return False

    overlap = role_words & evidence_words

    # Require at least one meaningful role word to overlap.
    return len(overlap) >= 1

def format_evidence(item: dict) -> dict:
    return {
        "segment_id": item["segment_id"],
        "score": item["score"],
        "text": item["text"]
    }


def validate_action_item(
    claim: dict,
    evidence: list[dict],
    person_roles: list[dict] | None = None
) -> dict:

    if not evidence:
        return {
            "claim_id": claim["claim_id"],
            "status": "uncertain",
            "reason": "No relevant evidence was retrieved.",
            "evidence": []
        }

    if person_roles is None:
        person_roles = []

    owner = claim["owner"].lower()

    owner_roles = [
        item["role"].lower()
        for item in person_roles
        if item["person"].lower() == owner
    ]

    task_words = tokenize(claim["task"])

    for item in evidence:

        text = item["text"].lower()
        evidence_words = tokenize(item["text"])

        task_overlap = task_words & evidence_words

        assignment_present = any(
            phrase in text
            for phrase in ASSIGNMENT_PHRASES
        )

        role_present = any(
          roles_match(role, text)
          for role in owner_roles
         )

        owner_present = owner in text

        if (
            len(task_overlap) >= 2
            and assignment_present
            and (owner_present or role_present)
        ):
            return {
                "claim_id": claim["claim_id"],
                "status": "supported",
                "reason": (
                    "The evidence matches the task, contains "
                    "assignment language, and identifies the owner "
                    "directly or through their stated role."
                ),
                "evidence": [
                    format_evidence(item)
                ]
            }

    return {
        "claim_id": claim["claim_id"],
        "status": "uncertain",
        "reason": (
            "Relevant evidence was retrieved, but the evidence "
            "did not establish the task and owner sufficiently."
        ),
        "evidence": [
            format_evidence(item)
            for item in evidence
        ]
    }

def validate_decision(
    claim: dict,
    evidence: list[dict]
) -> dict:

    if not evidence:
        return {
            "claim_id": claim["claim_id"],
            "status": "uncertain",
            "reason": "No relevant evidence was retrieved.",
            "evidence": []
        }

    decision_phrases = [
        "we decided",
        "we've decided",
        "we have decided",
        "agreed",
        "we agree",
        "let's go with",
        "we will use",
        "we'll use",
        "the decision is",
        "decided to",
        "agreed to",
    ]

    negation_phrases = [
        "not",
        "don't",
        "do not",
        "didn't",
        "did not",
        "won't",
        "will not",
        "wouldn't",
        "would not",
        "never",
    ]

    tentative_phrases = [
        "might",
        "maybe",
        "could",
        "possibly",
        "perhaps",
        "wonder if",
        "worth exploring",
        "consider",
        "suggestion",
        "idea",
        "possible",
    ]

    for item in evidence:

        text = item["text"].lower()

        # First check for explicit decision language.
        has_decision_language = any(
            phrase in text
            for phrase in decision_phrases
        )

        if not has_decision_language:
            continue

        # If the evidence contains negation near the decision,
        # treat it as contradiction rather than support.
        has_negation = any(
            phrase in text
            for phrase in negation_phrases
        )

        if has_negation:
            return {
                "claim_id": claim["claim_id"],
                "status": "contradicted",
                "reason": (
                    "The evidence contains decision language "
                    "but also indicates that the proposed decision "
                    "was rejected or negated."
                ),
                "evidence": [
                    format_evidence(item)
                ]
            }

        # Explicit decision language without negation.
        return {
            "claim_id": claim["claim_id"],
            "status": "supported",
            "reason": (
                "The evidence contains explicit language "
                "indicating an agreed decision."
            ),
            "evidence": [
                format_evidence(item)
            ]
        }

    return {
        "claim_id": claim["claim_id"],
        "status": "uncertain",
        "reason": (
            "The evidence discusses the topic, but does not "
            "contain clear language confirming the decision."
        ),
        "evidence": [
            format_evidence(item)
            for item in evidence
        ]
    } 


def validate_claim(
    claim: dict,
    evidence: list[dict],
    person_roles: list[dict] | None = None
) -> dict:

    if claim["claim_type"] == "action_item":
        return validate_action_item(
            claim,
            evidence,
            person_roles
        )

    if claim["claim_type"] == "decision":
        return validate_decision(
            claim,
            evidence
        )

    return {
        "claim_id": claim["claim_id"],
        "status": "uncertain",
        "reason": (
            f"Validation for claim type "
            f"'{claim['claim_type']}' is not implemented yet."
        ),
        "evidence": []
    }