from ranking_service.src.team_agents.common.agent import Agent

class EndNodeAgent(Agent):
    def invoke(self):
        self.update_state("end_chain", "end_chain")
        return self.state