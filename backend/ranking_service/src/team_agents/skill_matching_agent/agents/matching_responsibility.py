from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.team_agents.skill_matching_agent.prompts.matching_responsibility import *
from ranking_service.src.utils import *

class MatchingResponsibilityAgent(Agent):
    def invoke(self, candidate_responsibilities, job_responsibilities, prompt=matching_responsibility_prompt_template, feedback=None):
        # Xử lý feedback nếu có
        print("---------------MatchingResponsibilityAgent-----------")
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        # Tạo prompt với job và candidate responsibilities
        scorer_prompt = prompt.format(
            job_responsibilities="\n".join(job_responsibilities),
            # candidate_responsibilities=json.dumps(candidate_responsibility),
            datetime=get_current_utc_datetime()
        )

        # Tạo thông điệp
        messages = [
            {"role": "system", "content": scorer_prompt},
            {"role": "user", "content": f"### Candidate's Responsibilities: {str(candidate_responsibilities)}"}
        ]

        # Gọi LLM để lấy kết quả so sánh
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = check_for_content(ai_msg)

        # In kết quả
        print(colored(f"MatchingResponsibilityAgent 🧑🏼‍💻: {response}", 'blue'))

        # Cập nhật trạng thái và trả về kết quả
        return response