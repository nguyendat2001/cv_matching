from ranking_service.src.utils.util import check_for_content, get_current_utc_datetime
from ranking_service.src.utils import *
from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.team_agents.skill_matching_agent.prompts.scoring_with_board import *
from termcolor import colored

class ScoringWithBoardAgent(Agent):
    def invoke(self, scoring_board, user_component_skills, prompt=scoring_with_board_prompt_template, feedback=None):
        # Xử lý feedback nếu có
        print("---------------ScoringWithBoardAgent-----------")
        feedback_value = feedback() if callable(feedback) else feedback
        feedback_value = check_for_content(feedback_value)

        # scoring_board_value = scoring_board() if callable(scoring_board) else scoring_board

        # Tạo prompt với scoring board
        scorer_prompt = prompt.format(
            scoring_board=str(scoring_board),
            datetime=get_current_utc_datetime()
        )

        # Tạo thông điệp
        messages = [
            {"role": "system", "content": scorer_prompt},
            {"role": "user", "content": f"candidate skills: {', '.join(user_component_skills)}"}
        ]

        # Gọi LLM để lấy kết quả so sánh
        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = check_for_content(ai_msg)
        json_response = json.loads(response)
        print("json_response: ", json_response)
        # max_score = max(json_response["assign_score"])
        max_score = max((float(x['score']) for x in json_response["assign_score"] if not isinstance(x, str) and not isinstance(x, int) and not isinstance(x, float)), default=0)
        # 2. Calculate the sum of the rest of the values * 0.1
        rest_sum = sum(float(x["score"]) for x in json_response["assign_score"] if not isinstance(x, str) and not isinstance(x, int) and not isinstance(x, float) and x["score"] != max_score) * 0.1

        # 3. Update the assign_score
        json_response["assign_score_final"] = min(max_score + rest_sum,100)

        # In kết quả
        print(colored(f"ScoringWithBoardAgent 🧑🏼‍💻: {json_response}", 'blue'))

        # Cập nhật trạng thái và trả về kết quả
        self.update_state("scoring_with_board_response", json.dumps(json_response))
        return self.state
