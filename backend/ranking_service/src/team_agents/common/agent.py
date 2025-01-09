from langchain_ollama.llms import OllamaLLM
from typing import TypedDict, List, Any, Annotated
from langgraph.graph.message import add_messages

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

class Agent:
    def __init__(self, state: AgentGraphState, model=None, server=None, temperature=0, model_endpoint=None, stop=None, guided_json=None):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.guided_json = guided_json

    def get_llm(self, json_model=True):

        if self.server == 'ollama':
            # return OllamaJSONModel(model=self.model, temperature=self.temperature) if json_model else OllamaModel(model=self.model, temperature=self.temperature)
            # return CustomOllamaLLM(model="llama3.2")
            return OllamaLLM(model=self.model, format="json")


    def update_state(self, key, value):
        self.state = {**self.state, key: value}
