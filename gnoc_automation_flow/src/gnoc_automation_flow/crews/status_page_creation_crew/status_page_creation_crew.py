from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from model.model_classes import JiraModel
from tools.custom_tool import create_status_page_tool

# from langchain_openai import ChatOpenAI
# llm=ChatOpenAI(
#     model_name="ollama/llama3.1:latest",
#     api_key="your-api-key",
#     base_url= "http://localhost:11434/v1",
#     temperature=0
# )

@CrewBase
class StatusPageCreationCrew():
    """Jira Creation Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def status_page_creation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['status_page_creation_agent'],
            # llm=llm,
            # output_pydantic=JiraModel,
            # temperature=0,
            # cache=False

        )

    @task
    def status_page_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['status_page_creation_task'],
            tools=[create_status_page_tool],
            output_pydantic = JiraModel
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