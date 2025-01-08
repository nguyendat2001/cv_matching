matching_responsibility_guided_json = {
    "type": "object",
    "properties": {
        "individual_scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "candidate_responsibility": {
                        "type": "string",
                        "description": "Description of the candidate's responsibility."
                    },
                    "matching_score": {
                        "type": "number",
                        "description": "The matching score assigned to each candidate responsibility, based on alignment with the required job responsibilities."
                    },
                    "matched_with": {
                        "type": "string",
                        "description": "The corresponding job responsibility from the required list that the candidate's responsibility is compared with."
                    }
                },
                "required": ["candidate_responsibility", "matching_score", "matched_with"]
            },
            "description": "An array of individual scores for each responsibility, with a description of the matching responsibility."
        },
        "average_matching_percentage": {
            "type": "number",
            "description": "The average matching percentage for the candidate's responsibilities, calculated as a weighted average of individual scores."
        },
        "comment": {
            "type": "string",
            "description": "A summary comment explaining the evaluation, including strong matches, weak areas, and suggestions for improvement."
        }
    },
    "required": ["individual_scores", "average_matching_percentage", "comment"]
}