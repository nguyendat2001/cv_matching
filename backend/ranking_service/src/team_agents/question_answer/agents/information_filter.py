from ranking_service.src.team_agents.common.agent import Agent
from ranking_service.src.team_agents.question_answer.prompts.information_filter import *
from ranking_service.src.utils import *

class UserAnswerFilterAgent(Agent):
    def invoke(self, context, prompt=information_filter_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback

        information_filter_prompt = prompt.format(
            feedback=feedback_value,
            # context=context,
            datetime=get_current_utc_datetime()
        )

        messages = [
            {"role": "system", "content": information_filter_prompt},
            {"role": "user", "content": f"context: {context}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = check_for_content(ai_msg)

        print(colored(f"user answer filter 🧑🏼‍💻: {response}", 'green'))
        self.update_state("user_answer_filter_response", response)
        return self.state

class CorrectAnswerFilterAgent(Agent):
    def invoke(self, context, prompt=information_filter_prompt_template, feedback=None):
        feedback_value = feedback() if callable(feedback) else feedback

        information_filter_prompt = prompt.format(
            feedback=feedback_value,
            # context=context,
            datetime=get_current_utc_datetime()
        )

        messages = [
            {"role": "system", "content": information_filter_prompt},
            {"role": "user", "content": f"context: {context}"}
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = check_for_content(ai_msg)

        print(colored(f"correct answer filter 🧑🏼‍💻: {response}", 'green'))
        self.update_state("correct_answer_filter_response", response)
        return self.state