import json

def calculate_matching_tool(
    state: AgentGraphState,
    matching_response = None,
    job_description_component_skill = None
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
        print("-------------calculate_matching_tool-------------")
        matcher_data = matching_response() if callable(matching_response) else matching_response
        matcher_json_data = json.loads(matcher_data.content)
        print(type(matcher_json_data))
        if len(matcher_json_data["matching_skills"]) == 0:
            state["matching_score_response"] = "0.0"
            return state

        # Tính toán điểm tương đồng
        matching_score = min((len(matcher_json_data["matching_skills"]) / len(job_description_component_skill)) * 100 , 100)
        # Cập nhật trạng thái với kết quả
        matcher_json_data["assign_score_final"] = str(matching_score)
        state["matching_response"] = json.dumps(matcher_json_data)
        state["scoring_response"] = json.dumps(matching_score)
        return state

    except Exception as e:
        # Xử lý lỗi và cập nhật trạng thái
        state["scoring_response"] = f"error occurred: {str(e)}"
        return state