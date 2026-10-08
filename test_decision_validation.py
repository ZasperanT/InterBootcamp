from src.consistency import validate_claim


tests = [
    {
        "claim": {
            "claim_id": "decision_001",
            "claim_type": "decision",
            "decision": "The team decided to use a touchscreen remote."
        },
        "evidence": [
            {
                "segment_id": "test_001",
                "score": 0.9,
                "text": "We decided to use a touchscreen remote."
            }
        ]
    },

    {
        "claim": {
            "claim_id": "decision_002",
            "claim_type": "decision",
            "decision": "The team decided to use a touchscreen remote."
        },
        "evidence": [
            {
                "segment_id": "test_002",
                "score": 0.9,
                "text": "We decided not to use a touchscreen remote."
            }
        ]
    },

    {
        "claim": {
            "claim_id": "decision_003",
            "claim_type": "decision",
            "decision": "The team decided to use a touchscreen remote."
        },
        "evidence": [
            {
                "segment_id": "test_003",
                "score": 0.9,
                "text": "It might be worth exploring a touchscreen remote."
            }
        ]
    }
]


for test in tests:

    result = validate_claim(
        test["claim"],
        test["evidence"]
    )

    print("\n" + "=" * 60)
    print("CLAIM:")
    print(test["claim"]["decision"])

    print("\nEVIDENCE:")
    print(test["evidence"][0]["text"])

    print("\nRESULT:")
    print(result["status"])

    print("REASON:")
    print(result["reason"])