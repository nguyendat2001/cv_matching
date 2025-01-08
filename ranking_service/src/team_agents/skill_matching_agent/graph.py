import json
import ast
from termcolor import colored
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage

from ranking_service.src.team_agents.skill_matching_agent.utils import *
from ranking_service.src.team_agents.skill_matching_agent.agents import *
from ranking_service.src.team_agents.skill_matching_agent.json_guide import *
from ranking_service.src.team_agents.skill_matching_agent.prompts import *
from ranking_service.src.team_agents.skill_matching_agent.tools import *

def create_graph(server=None, model=None, stop=None, model_endpoint=None, temperature=0):
    graph = StateGraph(AgentGraphState)

    def initialized(state: AgentGraphState):
      """
      Checks if the scoring board is initialized and updates the state accordingly.
      Args:
          state (AgentGraphState): The state dictionary.
      Returns:
          AgentGraphState: The updated state dictionary.
      """
      print("---------------------initialized----------------------")
      state['initialized'] = state.get('scoring_board') is None or 'scoring_board' not in state

      # Add 'user_component_skills' and 'job_description_skills' to the state
      # if they exist in the input
      state['user_component_skills'] = state.get('user_component_skills', None)
      state['job_description_skills'] = state.get('job_description_skills', None)
      return state

    graph.add_node(
        "initialize_agent",
        lambda state: initialized(state=state)
    )

    graph.add_node(
        "matching_agent",
        lambda state: MatchingAgent(
            state=state,
            model=model,
            server=server,
            guided_json=matching_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            user_component_skills = state["user_component_skills"],
            job_description_component_skills = state["job_description_component_skills"],
            prompt=matching_prompt_template,
        )
    )

    graph.add_node(
        "scoring_with_board_agent",
        lambda state: ScoringWithBoardAgent(
            state=state,
            model=model,
            server=server,
            guided_json=scoring_with_board_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            scoring_board = state["scoring_board"],
            user_component_skills = state["user_component_skills"],
            # feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
            prompt=scoring_with_board_prompt_template
        )
    )

    graph.add_node(
          "calculate_matching_tool",
          lambda state: calculate_matching_tool(
              state=state,
              matching_response = lambda: get_agent_graph_state(state=state, state_key="matching_latest"),
              job_description_component_skill = state["job_description_component_skills"],
          )
      )

    graph.add_node(
        "final_report",
        lambda state: FinalReportAgent(
            state=state
        ).invoke(
            matching_response=lambda: get_agent_graph_state(state=state, state_key="matching_latest"),
            scoring_response=lambda: get_agent_graph_state(state=state, state_key="scoring_latest"),
            scoring_with_board_response=lambda: get_agent_graph_state(state=state, state_key="scoring_with_board_latest"),
        )
    )

    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    def cv_matching_router(state: AgentGraphState):
        """
        Routes the workflow based on the initialization status.

        Args:
            state (AgentGraphState): The current state of the workflow.

        Returns:
            str: The name of the next agent to execute.
        """

        # Check if the 'initialized' flag is True in the state dictionary
        if state.get('initialized', False):
            return "matching_agent"  # If initialized, proceed to the matching agent
        else:
            return "scoring_with_board_agent"  # If not initialized, start with the scoring agent

    graph.add_conditional_edges('initialize_agent', cv_matching_router, {
        'scoring_with_board_agent': 'scoring_with_board_agent',
        'matching_agent': "matching_agent"
    })


    # Add edges to the graph
    graph.set_entry_point("initialize_agent")
    graph.set_finish_point("end")
    graph.add_edge("matching_agent", "calculate_matching_tool")
    graph.add_edge("calculate_matching_tool", "final_report")
    graph.add_edge("scoring_with_board_agent", "final_report")
    graph.add_edge("final_report", "end")

    return graph