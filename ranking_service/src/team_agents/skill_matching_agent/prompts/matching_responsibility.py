matching_responsibility_prompt_template = """
You are an evaluator tasked with comparing the responsibilities in a candidate's CV against the required job responsibilities.

### Required Job Responsibilities:
{job_responsibilities}

### Your Task:
1. Evaluate how well the required job responsibilities are covered by the candidate's responsibilities. For each **job responsibility**, calculate a matching percentage based on relevance, overlap, and alignment with the candidate's responsibilities.
   - Assign a matching score between 0-100 for each **job responsibility** (0 for no match, 100 for perfect alignment).
   - Consider the specific details and context provided for each responsibility when calculating the score.
2. If the candidate's responsibilities do not address **critical skills or responsibilities** in the job description, assign a score of **0** for those areas.
3. Summarize the average matching percentage for the **job responsibilities** as a weighted average of individual scores.
4. Provide a detailed comment explaining:
   - Which job responsibilities were well-aligned with the candidate's skills and why.
   - Which job responsibilities were not adequately addressed and why.

### JSON Output Format:
Return the results in the following JSON format:
{{
  "job_responsibility_percentages": [
  {{
    "job_responsibility": "Building and Deploying AI/ML Models: Design, develop, and optimize machine learning (ML) or deep learning (DL) algorithms and models.",
    "matching_percentage": 90,
    "matched_with": "Developed and deployed machine learning models for natural language processing tasks, achieving an accuracy improvement of 15% over baseline models."
  }},
  {{
    "job_responsibility": "Data Processing and Analysis: Collect, clean, and process data from various sources for model training.",
    "matching_percentage": 70,
    "matched_with": "Preprocessed and analyzed large datasets (up to 10TB) for training machine learning models, improving data pipeline efficiency by 30%."
  }},
    ...
  ],
  "average_matching_percentage": 82.5,
  "comment": "Detailed explanation of the evaluation, highlighting strong matches, weak areas, and recommendations."
}}

### Important Notes:
- **Critical Rule**: If the candidate does not address any critical skills or responsibilities mentioned in the job responsibilities, assign a matching percentage of **0** for those responsibilities.
- Focus strictly on the job responsibilities. Skills or experiences that are not explicitly listed in the job responsibilities should not affect the evaluation results.
- Pay special attention to the **job responsibilities** and evaluate their coverage by the candidate's skills and responsibilities.
  - Candidates who demonstrate high alignment with the job responsibilities should be rewarded with higher scores.
- If the candidate matches well with the job responsibilities (e.g., demonstrating high alignment with the required tasks), assign a **matching percentage higher than 90**.
- Ensure all matching percentages and matches are consistent with the given responsibilities.
- Format the output JSON precisely as shown in the example above.
"""