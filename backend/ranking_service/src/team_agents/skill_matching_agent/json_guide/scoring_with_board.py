scoring_with_board_guided_json = {
    "type": "object",
    "properties": {
        "assign_score": {
            "type": "array",
            "items": {
                "type": "number",
                "description": "The score assigned to each candidate skill based on the scoring board."
            },
            "description": "An array of scores assigned to each skill evaluated."
        },
        "comment": {
            "type": "string",
            "description": "A summary comment explaining the evaluation and providing insights or recommendations."
        }
    },
    "required": ["assign_score", "comment"]
}