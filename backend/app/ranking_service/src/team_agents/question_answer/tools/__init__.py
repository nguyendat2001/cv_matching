import json
from ranking_service.src.team_agents.common.agent import *

def calculate_matching_qa_tool(
    state: AgentGraphState,
    matcher_response = None,
    correct_answer_filter_response = None,
) -> AgentGraphState:
    """
    Tính toán điểm tương đồng giữa câu trả lời đúng và câu trả lời của người dùng trên thang điểm 100
    dựa trên tỷ lệ độ dài của mảng câu trả lời của người dùng so với câu trả lời đúng.

    Args:
        state (AgentGraphState): Trạng thái hiện tại của AgentGraph.
        plan (callable): Hàm hoặc đối tượng cung cấp thông tin kế hoạch, phải có `.content`.

    Returns:
        AgentGraphState: Trạng thái đã cập nhật với kết quả matching_score.
    """
    try:
        matcher_data = matcher_response() if callable(matcher_response) else matcher_response
        print("matcher_data: == "+str(matcher_data.content))

        matcher_json_data = json.loads(matcher_data.content)

        correct_answer_filter_data = correct_answer_filter_response().content
        correct_answer_filter_json_data = json.loads(correct_answer_filter_data)
        # Kiểm tra nếu mảng correct_main_point trống để tránh chia cho 0
        if len(matcher_json_data) == 0:
            state["matching_score_response"] = "0.0"
            return state

        # Tính toán điểm tương đồng
        matching_score = min((len(matcher_json_data["matching_points"]) / len(correct_answer_filter_json_data["response"])) * 100 , 100)

        # Cập nhật trạng thái với kết quả
        state["matching_score_response"] = str(matching_score)
        return state

    except Exception as e:
        # Xử lý lỗi và cập nhật trạng thái
        state["matching_score_response"] = f"error occurred: {str(e)}"
        return state