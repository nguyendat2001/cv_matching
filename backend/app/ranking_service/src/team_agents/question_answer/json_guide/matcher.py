matcher_guided_json = {
    "type": "object",
    "properties": {
        "matching_points": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "A key piece of information from the user answer that matches the correct answer."
            },
            "description": "An array of key points from the user answer that match the correct answer."
        },
        "unmatching_points": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "A key piece of information from the user answer that does not match the correct answer."
            },
            "description": "An array of key points from the user answer that do not match the correct answer."
        },
        "comment": {
            "type": "string",
            "description": "A comment about the matching and unmatching points."
        }
    },
    "required": ["matching_points", "unmatching_points", "comment"]
}