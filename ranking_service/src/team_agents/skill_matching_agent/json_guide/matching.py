matching_guided_json = {
    "type": "object",
    "properties": {
        "matching_skills": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "A skill provided by the user that matches a required skill in the job description."
            },
            "description": "An array of skills provided by the user that match the required skills in the job description."
        },
        "missing_required_skills": {
            "type": "array",
            "items": {
                "type": "string",
                "description": "A required skill from the job description that is not possessed by the user."
            },
            "description": "An array of required skills from the job description that the user does not possess."
        },
        "comment": {
            "type": "string",
            "description": "A comment about the matching and unmatching skills, and recommendations for improvement."
        }
    },
    "required": ["matching_skills", "missing_required_skills", "comment"]
}
