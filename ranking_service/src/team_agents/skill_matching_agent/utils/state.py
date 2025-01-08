from typing import TypedDict, List, Any
from langgraph.graph.message import add_messages

# Define the state object for the agent graph
class AgentGraphState(TypedDict):
    user_component_skills: List[Any]
    job_description_component_skills: List[Any]
    scoring_board: List[Any]
    initialized: bool
    matching_response: Annotated[List[Any], add_messages]
    scoring_response: Annotated[List[Any], add_messages]
    scoring_with_board_response: Annotated[List[Any], add_messages]
    final_reports: Annotated[List[Any], add_messages]
    end_chain: Annotated[List[Any], add_messages]

def get_agent_graph_state(state: AgentGraphState, state_key: str):
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
state: AgentGraphState = {
    "user_component_skills": [],
    "job_description_component_skills": [],
    "scoring_board": [],
    "initialized": None,
    "matching_response": [],
    "scoring_response": [],
    "scoring_with_board_response": [],
    "final_reports": [],
    "end_chain": []
}
