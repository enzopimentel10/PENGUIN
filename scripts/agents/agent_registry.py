from typing import List, Dict, Any, Optional

class Agent:
    def __init__(self, agent_name: str, description: str, competencies: List[str], supported_skills: List[str], instructions: str = ""):
        self.agent_name = agent_name
        self.description = description
        self.competencies = competencies
        self.supported_skills = supported_skills
        self.instructions = instructions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "description": self.description,
            "competencies": self.competencies,
            "supported_skills": self.supported_skills,
            "instructions": self.instructions
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Agent':
        return cls(
            agent_name=data.get("agent_name", ""),
            description=data.get("description", ""),
            competencies=data.get("competencies", []),
            supported_skills=data.get("supported_skills", []),
            instructions=data.get("instructions", "")
        )

class AgentRegistry:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    def register_agent(self, agent: Agent):
        self.agents[agent.agent_name] = agent
        print(f"[AgentRegistry] Registered agent: {agent.agent_name}")

    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        return self.agents.get(name)

    def find_agents_by_competency(self, competency: str) -> List[Agent]:
        return [
            agent for agent in self.agents.values()
            if competency.lower() in [c.lower() for c in agent.competencies]
        ]

    def list_all_agents(self) -> List[str]:
        return list(self.agents.keys())
