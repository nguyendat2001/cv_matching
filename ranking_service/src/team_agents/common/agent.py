from langchain_ollama.llms import OllamaLLM

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
