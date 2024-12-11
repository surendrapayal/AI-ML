from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ...model.model_classes import PriorityModel
from ...tools.custom_tool import pdf_reader
# from langchain_openai import ChatOpenAI

# llm=ChatOpenAI(
#     model_name="ollama/llama3.1:latest",
#     api_key="your-api-key",
#     base_url= "http://localhost:11434/v1",
#     temperature=0.5
# )

@CrewBase
class PriorityIdentificationCrew():
    """Priority Identification Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def priority_identification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["priority_identification_agent"],
            # llm=llm,
            tools=[pdf_reader],
        )

    @task
    def priority_identification_task(self) -> Task:
        return Task(
            config=self.tasks_config["priority_identification_task"],
            output_pydantic = PriorityModel,
            # human_input=True
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            cache=False
        )