from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.team_agents.question_answer.prompts.matcher import *
from ranking_service.src.utils import *
from termcolor import colored

class MatcherAgent(Agent):
    def invoke(self, user_answer_key_points=None, correct_answer_key_points=None, prompt=matcher_prompt_template, feedback=None):
        # Xử lý feedback nếu có
        print("---------------MatcherAgent-----------")
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        user_answer_key_points_value = user_answer_key_points() if callable(user_answer_key_points) else user_answer_key_points
        user_answer_response = check_for_content(user_answer_key_points_value)

        correct_answer_key_points_value = correct_answer_key_points() if callable(correct_answer_key_points) else correct_answer_key_points
        correct_answer_response = check_for_content(correct_answer_key_points_value)
        print("user_answer_key_points_value: " + str(json.loads(user_answer_response[0].content)["response"]))
        print("correct_answer_key_points_value: " + str(json.loads(correct_answer_response[0].content)["response"]))
        # Tạo prompt với dữ liệu truyền vào
        matcher_prompt = prompt.format(
            user_answer_key_points="\n".join(json.loads(user_answer_response[0].content)["response"]),
            correct_answer_key_points="\n".join(json.loads(correct_answer_response[0].content)["response"]),
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
        self.update_state("matcher_response", response)
        return self.state