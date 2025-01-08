matching_experience_guided_json = {
    "type": "object",
    "properties": {
        "experience_comparison": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "job_responsibility": {
                        "type": "string",
                        "description": "The description of the job responsibility, including the required years of experience."
                    },
                    "required_years": {
                        "type": "number",
                        "description": "The number of years of experience required for this job responsibility."
                    },
                    "candidate_years": {
                        "type": "number",
                        "description": "The number of years of experience the candidate has relevant to this job responsibility."
                    }
                },
                "required": ["job_responsibility", "required_years", "candidate_years"]
            },
            "description": "An array of job responsibilities with the required years of experience and the candidate's corresponding years of experience."
        },
        "comment": {
            "type": "string",
            "description": "A summary comment highlighting areas where the candidate meets or exceeds the required years of experience and areas where they fall short."
        }
    },
    "required": ["experience_comparison", "comment"]
}