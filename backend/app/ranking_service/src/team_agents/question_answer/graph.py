import json
import ast
from termcolor import colored
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage

from ranking_service.src.team_agents.question_answer.utils import *
from ranking_service.src.team_agents.question_answer.agents import *
from ranking_service.src.team_agents.question_answer.json_guide import *
from ranking_service.src.team_agents.question_answer.prompts import *
from ranking_service.src.team_agents.question_answer.tools import *

def create_graph_matching_QA(server=None, model=None, stop=None, model_endpoint=None, temperature=0, state=qa_state):
    graph = StateGraph(QAAgentGraphState)

    graph.add_node(
        "correct_answer_filter",
        lambda state: CorrectAnswerFilterAgent(
            state=state,
            model=model,
            server=server,
            guided_json=information_filter_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            context=state["correct_answer"],
            prompt=information_filter_prompt_template,
        )
    )

    graph.add_node(
        "user_answer_filter",
        lambda state: UserAnswerFilterAgent(
            state=state,
            model=model,
            server=server,
            guided_json=information_filter_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            context=state["user_answer"],
            prompt=information_filter_prompt_template,
        )
    )

    graph.add_node(
        "matcher",
        lambda state: MatcherAgent(
            state=state,
            model=model,
            server=server,
            guided_json=matcher_guided_json,
            stop=stop,
            model_endpoint=model_endpoint,
            temperature=temperature
        ).invoke(
            user_answer_key_points=lambda: get_agent_graph_state(state=state, state_key="user_answer_filter_all"),
            correct_answer_key_points=lambda: get_agent_graph_state(state=state, state_key="correct_answer_filter_all"),
            feedback=lambda: get_agent_graph_state(state=state, state_key="reviewer_latest"),
            prompt=matcher_prompt_template
        )
    )

    graph.add_node(
          "calculate_matching_tool",
          lambda state: calculate_matching_qa_tool(
              state=state,
              matcher_response = lambda: get_agent_graph_state(state=state, state_key="matcher_latest"),
              correct_answer_filter_response = lambda: get_agent_graph_state(state=state, state_key="correct_answer_filter_latest")
          )
      )

    graph.add_node(
        "final_report",
        lambda state: FinalReportQAAgent(
            state=state
        ).invoke(
            matcher_response=lambda: get_agent_graph_state(state=state, state_key="matcher_latest"),
            tool_response=lambda: get_agent_graph_state(state=state, state_key="matching_score_latest")
        )
    )

    graph.add_node("end", lambda state: EndNodeAgent(state).invoke())

    # Add edges to the graph
    graph.set_entry_point("correct_answer_filter")
    graph.set_finish_point("end")
    graph.add_edge("correct_answer_filter", "user_answer_filter")
    graph.add_edge("user_answer_filter", "matcher")
    graph.add_edge("matcher", "calculate_matching_tool")
    graph.add_edge("calculate_matching_tool", "final_report")
    graph.add_edge("final_report", "end")

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow