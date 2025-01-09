from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.utils import *

class FinalReportAgent(Agent):
    def invoke(self, scoring_response=None, matching_response=None, scoring_with_board_response=None):
        print("-"*15 + "Final Report" + "-"*15)
        tool_value = scoring_response() if callable(scoring_response) else scoring_response
        tool_value_response = check_for_content(tool_value)

        matcher_value = matching_response() if callable(matching_response) else matching_response
        matcher_value_response = check_for_content(matcher_value)

        if tool_value_response is not None and matcher_value_response is not None:
            matcher_value_response = json.loads(matcher_value_response)
            matcher_value_response["assign_score_final"] = tool_value_response

        scoring_with_board_value = scoring_with_board_response() if callable(scoring_with_board_response) else scoring_with_board_response
        scoring_with_board = check_for_content(scoring_with_board_value)


        final_reports = {
            # "tool_value": tool_value_response,
            "matcher_value_response": matcher_value_response,
            "scoring_with_board": scoring_with_board
        }
        print(colored(f"final_reports: {final_reports}", 'blue'))
        self.update_state("final_reports", json.dumps(final_reports))
        return self.state