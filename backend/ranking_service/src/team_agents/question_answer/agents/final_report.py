from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.utils.util import check_for_content, get_current_utc_datetime
from ranking_service.src.utils import *
from termcolor import colored

class FinalReportQAAgent(Agent):
    def invoke(self, tool_response=None, matcher_response=None):
        tool_value = tool_response() if callable(tool_response) else tool_response
        tool_value_response = check_for_content(tool_value)

        matcher_value = matcher_response() if callable(matcher_response) else matcher_response
        matcher_value_response = check_for_content(matcher_value)
        matcher_value_response = json.loads(matcher_value_response)
        matcher_value_response["tool_value_response"]=tool_value_response
        # Add role and content keys
        final_report = {
            "role": "assistant",  # You can adjust the role as needed
            "content": json.dumps(matcher_value_response) # Convert the entire matcher response to a string for content
        }
        print("="*50)
        print(colored(f"Final Report 📝:", 'blue'))
        print(colored(f"tool_value_response: {tool_value_response}", 'blue'))
        print(colored(f"matcher_value_response: {matcher_value_response}", 'blue'))
        # Update the state with the modified dictionary
        self.update_state("final_reports", final_report)
        return self.state