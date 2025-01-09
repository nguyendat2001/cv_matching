matcher_prompt_template = """
You are a matcher. Your task is to compare and identify matching and unmatching key points between the user's answer and the correct answer.

Here are the key points from the correct answer:
{correct_answer_key_points}

Here are the key points from the user answer:
{user_answer_key_points}

Your task:
1. Identify the key points from the user answer that match with the correct answer.
2. Identify the key points from the user answer that do not match with the correct answer.
3. Provide a comment explaining the matching and unmatching points.

Return the results in the following JSON format:
{{
    "matching_points": [
        "Matching key point 1",
        "Matching key point 2",
        ...
    ],
    "unmatching_points": [
        "Unmatching key point 1",
        "Unmatching key point 2",
        ...
    ],
    "comment": "A comment about the matching and unmatching points."
}}

Current date and time:
{datetime}
"""