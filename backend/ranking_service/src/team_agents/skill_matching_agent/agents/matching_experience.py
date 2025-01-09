from ranking_service.src.utils.util import check_for_content, get_current_utc_datetime
from ranking_service.src.utils import *
from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.team_agents.skill_matching_agent.prompts.matching_experience import *
from termcolor import colored

class MatchingExperienceAgent(Agent):
    def invoke(self, candidate_experience, job_experience, prompt_template = matching_experience_prompt_template, feedback=None):
        """
        So khớp số năm kinh nghiệm giữa yêu cầu công việc và kinh nghiệm của ứng viên.

        Args:
            candidate_experience (list): Danh sách các kinh nghiệm của ứng viên.
            job_experience (list): Danh sách các trách nhiệm công việc kèm theo số năm kinh nghiệm yêu cầu.
            prompt_template (str): Prompt mẫu để so sánh kinh nghiệm.
            feedback (callable or None): Hàm hoặc giá trị phản hồi, nếu có.

        Returns:
            dict: Kết quả JSON với so khớp kinh nghiệm.
        """
        print("---------------MatchingExperienceAgent-----------")

        # Xử lý feedback nếu có
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        # Tạo prompt với job responsibilities và candidate experience
        prompt = prompt_template.format(
            job_responsibilities="\n".join(job_experience),
            datetime=get_current_utc_datetime()
        )

        # Tạo thông điệp input cho mô hình
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"### Candidate's Experience: {str(candidate_experience)}"}
        ]

        # Gọi LLM để lấy kết quả so sánh
        llm = self.get_llm()
        ai_response = llm.invoke(messages)
        response = check_for_content(ai_response)
        json_response = json.loads(response)

        for item in json_response["experience_comparison"]:
            if item.get("required_years") is not None and item.get("candidate_years") is not None:
                item["experience_percentage"] = min((int(item["candidate_years"]) / int(item["required_years"])) * 100, 100)
            else: item["experience_percentage"] = 0
        # Tính điểm trung bình
        total_percentage = sum(item["experience_percentage"] for item in json_response["experience_comparison"])
        average_percentage = total_percentage / len(json_response["experience_comparison"])

        # Cập nhật overall_experience_percentage trong json_response
        json_response["average_experience_percentage"] = average_percentage

        # In kết quả
        print(colored(f"MatchingExperienceAgent 🧑🏼‍💻: {json_response}", 'blue'))

        # Cập nhật trạng thái và trả về kết quả
        return json_response