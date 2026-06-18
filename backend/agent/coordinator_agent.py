from agent.resume_agent import ResumeAgent
from agent.job_agent import JobAgent
from agent.learning_agent import LearningAgent
from agent.skill_gap_agent import SkillGapAgent


class CoordinatorAgent:

    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.job_agent = JobAgent()
        self.learning_agent = LearningAgent()
        self.skill_gap_agent = SkillGapAgent()

    def run(self, data):

        return {
            "resume": self.resume_agent.run(
                data["skills"]
            ),
            "jobs": self.job_agent.run(
                data["jobs"]
            ),
            "learning": self.learning_agent.run(
                data["roadmap"],
                data["resources"]
            ),
            "gap": self.skill_gap_agent.run(
                data["missing_skills"]
            )
        }