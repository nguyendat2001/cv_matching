from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.team_agents.skill_matching_agent.prompts.matching import *
import json
from ranking_service.src.utils.util import check_for_content, get_current_utc_datetime
from ranking_service.src.utils import *
from termcolor import colored

class MatchingAgent(Agent):
    def invoke(self, user_component_skills, job_description_component_skills, prompt=matching_prompt_template, feedback=None):
        # Xử lý feedback nếu có
        print("---------------MatcherAgent-----------")
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        # user_skills_value = user_technique_skills() if callable(user_technique_skills) else user_technique_skills
        # user_skills_response = check_for_content(user_skills_value)

        # job_skills_value = job_description_skills() if callable(job_description_skills) else job_description_skills
        # job_skills_response = check_for_content(job_skills_value)

        # Tạo prompt với dữ liệu truyền vào
        matcher_prompt = prompt.format(
            user_component_skills="\n".join(user_component_skills),
            job_description_component_skills="\n".join(job_description_component_skills),
            datetime=get_current_utc_datetime()
        )

        # Tạo thông điệp
        messages = [
            {"role": "system", "content": matcher_prompt}
        ]

        # Gọi LLM để lấy kết quả so sánh
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = check_for_content(ai_msg)

        # In kết quả
        print(colored(f"Matcher Agent 🧑🏼‍💻: {response}", 'blue'))

        # Cập nhật trạng thái và trả về kết quả
        self.update_state("matching_response", response)
        return self.state