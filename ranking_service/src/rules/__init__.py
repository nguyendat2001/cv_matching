

job_requirement_score = {
    "university":[
        {
            "code":"HCMUS",
            "name":"Đại học khoa học tự nhiên",
            "score":80,
        },
        {
            "code":"RMIT",
            "name":"Đại học RMIT",
            "score":70,
        },
        {
            "code":"CTU",
            "name":"đại học cần thơ",
            "score":60,
        },
        {
            "code":"UNKNOWN",
            "name":"các trường đại học khác",
            "score":30,
        },
    ],
    "degree":[{"name":"bachelor degree","score":65},
              {"name":"master degree","score":75},
              {"name":"PHD degree","score":85}],
    "certificate":[{"name":"AWS certificate","score":60},
              {"name":"product managerment Certified","score":50},
              {"name":"các chứng chỉ khác, không xác định","score":10}],
    "english_level":[{"level":"proficent","description":" Ielts score >= 7.5 / Toiec score >= 800","score":100},
                    {"level":"intermediate", "description":"7.5 > Ielts score and Ielts score >= 6.0 / 800 > Toiec score and Toiec score >= 600","score":60},
                    {"level":"basc","description":"6.5 > Ielts score and Ielts score >= 4.5 /  600 > Toiec score and toiec score >= 450","score":30},
                    {"level":"None","description":"None","score":0}],
}

weights = {
    "degree": 0.05,  # The importance of the candidate's degree
    "university": 0.05,
    "english_level": 0.1,
    "year_experience": 0.1,  # The importance of the candidate's work experience
    "technical_skill": 0.25,  # Weight for technical skills and qualifications
    "responsibility": 0.35,  # How well the candidate's past responsibilities align with the job
    "certificate": 0.05,  # The significance of relevant certifications
    "soft_skill": 0.05,  # Importance of soft skills like communication, teamwork, etc.
}