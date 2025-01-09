

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

job_description_requirement = {
    "degree":["bachelor degree"],
    "year_experience":["from 5 year experience with Devops","2 year experience with product management"],
    "technical_skill":["tensorflow","pytorch","llm","faskAPI", "java","devops"],
    "responsibility":[
                      "Lead and manage cross-functional project teams to deliver projects on time, within scope, and within budget. Develop detailed project plans, including timelines, milestones, and resources. Coordinate with stakeholders to ensure project objectives and expectations are aligned. Monitor project performance, track progress, and make adjustments as necessary."
                      "Building and Deploying AI/ML Models: Design, develop, and optimize machine learning (ML) or deep learning (DL) algorithms and models.Deploy AI models from research environments into production.Evaluate and improve the performance of deployed models.",
                      "Data Processing and Analysis: Collect, clean, and process data from various sources for model training. Build automated data processing pipelines (ETL pipelines).Analyze datasets to extract insights and support AI applications.",
                      "System Integration: Integrate AI models into applications or enterprise products. Develop APIs or microservices to enable other systems to use AI models. Ensure the stability and efficiency of AI systems in production",
                      "Research and Development (R&D): Stay updated on the latest trends and technologies in AI/ML. Customize existing models or develop new algorithms to solve specific business problems. Collaborate with research teams to improve AI products."],
    # "english_level":["proficient"],
    "certificate":["AWS certificate","Microsoft azure Certified","product managerment Certified"],
    "soft_skill": ["leadership skill","critical thinking skill"],
    "correct_answer_1":"Hàm ReLU được định nghĩa là:ReLU(𝑥)=max(0,𝑥) Điều này có nghĩa là nếu giá trị đầu vào là âm, ReLU trả về 0, và nếu giá trị đầu vào là dương, ReLU trả về chính giá trị đó.",
    "correct_answer_2":"The aerodynamic system operates based on the principles of fluid dynamics, focusing on the interaction between air and solid surfaces. When an object moves through the air, it generates forces due to pressure and velocity differences around its surface. These forces include lift, drag, and sometimes thrust, depending on the system design.\
          Lift is created when the airflow over the top surface of an object, such as an airplane wing, moves faster than the airflow beneath, resulting in lower pressure above and higher pressure below. Drag, on the other hand, is the resistance caused by air friction and turbulence as the object moves forward.\
          The balance and optimization of these forces are achieved through careful design of shapes, surfaces, and control systems to maximize efficiency and stability, making it a critical aspect in aviation, automotive, and wind energy applications.",
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