from typing import TypedDict, List, Any, Annotated
from langgraph.graph.message import add_messages

class QAAgentGraphState(TypedDict):
    user_answer: str
    correct_answer: str
    user_answer_filter_response: Annotated[List[Any], add_messages]
    correct_answer_filter_response: Annotated[List[Any], add_messages]
    matcher_response: Annotated[List[Any], add_messages]
    matching_score_response: Annotated[List[Any], add_messages]
    final_reports: Annotated[List[Any], add_messages]
    end_chain: Annotated[List[Any], add_messages]

def get_agent_graph_state(state: QAAgentGraphState, state_key: str):
    """
    Trích xuất dữ liệu từ state dựa trên state_key.

    Args:
        state (AgentGraphState): Đối tượng state chứa dữ liệu.
        state_key (str): Tên khóa cần truy xuất, gồm các tùy chọn:
            - "{category}_all": Trả về toàn bộ danh sách của một loại phản hồi.
            - "{category}_latest": Trả về phần tử mới nhất trong danh sách của loại phản hồi.

    Returns:
        Any: Dữ liệu phù hợp với state_key, hoặc None nếu không hợp lệ.
    """
    if not isinstance(state, dict):
        raise ValueError("State must be a dictionary conforming to AgentGraphState.")

    if state_key.endswith("_all"):
        category = state_key.replace("_all", "")
        return state.get(f"{category}_response", [])

    if state_key.endswith("_latest"):
        category = state_key.replace("_latest", "")
        responses = state.get(f"{category}_response", [])
        return responses[-1] if responses else None

    # Trường hợp state_key không hợp lệ
    return None



# Define the initial state for the agent graph
qa_state: QAAgentGraphState = {
    "user_answer": "",
    "correct_answer": "",
    "user_answer_filter_response": [],
    "correct_answer_filter_response": [],
    "matcher_response": [],
    "matching_score_response": [],
    "final_reports": [],
    "end_chain": []
}
