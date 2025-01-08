matching_experience_prompt_template = """
You are an evaluator tasked with comparing the years of experience listed in a candidate's CV against the years of experience required for each job responsibility.

### Required Job Responsibilities:
{job_responsibilities}

### Your Task:
1. For each **job responsibility**, extract the required years of experience from the job description.
2. Compare the candidate's years of experience relevant to each **job responsibility**.
3. Summarize the results by providing:
   - The job responsibility description.
   - The required years of experience for that responsibility.
   - The candidate's years of experience relevant to that responsibility.

### JSON Output Format:
Return the results in the following JSON format:
{{
  "experience_comparison": [
    {{
      "job_responsibility": "Building and Deploying AI/ML Models: Minimum 3 years of experience required.",
      "required_years": 3,
      "candidate_years": 4
    }},
    {{
      "job_responsibility": "Data Processing and Analysis: Minimum 2 years of experience required.",
      "required_years": 2,
      "candidate_years": 1
    }},
    ...
  ],
  "comment": "Summary explanation highlighting areas where the candidate meets or exceeds the required years of experience and areas where they fall short."
}}

### Important Notes:
- Focus only on the number of years of experience required for each job responsibility.
- Do not calculate any scores or percentages; only provide the years of experience comparison.
- Ensure the output is strictly in the specified JSON format.
"""