from typing import Any, Dict, List, Optional, Mapping, Sequence
from langchain.llms.base import BaseLLM
# No need to import CallbackManagerForLLM
from langchain_ollama.llms import OllamaLLM
from langchain.tools import BaseTool
from langchain.callbacks.base import BaseCallbackManager

class CustomOllamaLLM(OllamaLLM):  # Inherit from OllamaLLM
    """Custom LangChain LLM wrapper for Ollama to enable tool calling."""

    # tools: Sequence[BaseTool]

    def __init__(self,
                 model: str = "llama3.2",
                 ollama_kwargs: Optional[Dict] = None,
                 callback_manager: Optional[BaseCallbackManager] = None,
                 tools: Optional[Sequence[BaseTool]] = None,
                 **kwargs: Any) -> None:
        """Initialize the CustomOllamaLLM."""
        # Set ollama_kwargs to an empty dictionary if it's None
        if ollama_kwargs is None:
            ollama_kwargs = {}
        # Pass tools to super().__init__
        super().__init__(model=model,
                         callback_manager=callback_manager,
                         tools=tools or [],  # Pass tools here
                         **ollama_kwargs, **kwargs)
        # self.tools = tools or []

    @property
    def _llm_type(self) -> str:
        return "custom_ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the Ollama model and return JSON response."""
        # The Ollama client's `generate` method doesn't support an `output_format` parameter.
        # It returns text by default. To get JSON output, we'll need to parse the text response.
        response = super().__call__(prompt, stop=stop)

        # Attempt to parse the response as JSON. If it fails, assume it's plain text.
        try:
            parsed_response = json.loads(response)
        except json.JSONDecodeError:
            parsed_response = response # If it's not JSON, keep it as text

        return parsed_response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {**super()._identifying_params, **{"custom": True}}

    def bind_tools(self, tools: Sequence[BaseTool]) -> "CustomOllamaLLM":
        """Bind tools to the LLM.

        Args:
            tools: A sequence of tools to bind.

        Returns:
            The LLM instance with the tools bound.
        """
        self.tools = tools
        return self