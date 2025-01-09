information_filter_guided_json = {
    "type": "object",
    "properties": {
        "response": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "A key piece of information extracted from the text."
            },
            "description": "An array of key points extracted from the provided text."
        }
    },
    "required": ["response"]
}