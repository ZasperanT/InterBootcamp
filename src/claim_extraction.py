def extract_claims(meeting_record: dict) -> list[dict]:
    """
    Convert a candidate meeting record into structured claims.

    Claims are extracted deterministically from the candidate record.
    No LLM is used here.
    """

    claims = []

    # -------------------------
    # KEY DECISIONS
    # -------------------------

    for index, decision in enumerate(
        meeting_record.get("key_decisions", []),
        start=1
    ):
        claims.append({
            "claim_id": f"decision_{index:03d}",
            "claim_type": "decision",
            "decision": decision["decision"]
        })

    # -------------------------
    # ACTION ITEMS
    # -------------------------

    for index, item in enumerate(
        meeting_record.get("action_items", []),
        start=1
    ):
        claims.append({
            "claim_id": f"action_{index:03d}",
            "claim_type": "action_item",
            "task": item["task"],
            "owner": item["owner"],
            "deadline": item["deadline"]
        })

    return claims