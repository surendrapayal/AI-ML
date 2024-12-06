from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from ...model.model_classes import JiraModel
from ...tools.custom_tool import custom_jira_tool
# from langchain_openai import ChatOpenAI

# llm=ChatOpenAI(
#     model_name="ollama/llama3.1:latest",
#     api_key="your-api-key",
#     base_url= "http://localhost:11434/v1",
#     temperature=0
# )

@CrewBase
class JiraCreationCrew():
    """Jira Creation Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def jira_creation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['jira_creation_agent'],
            # llm=llm,
            max_iter=1,
        )

    @task
    def jira_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['jira_creation_task'],
            output_pydantic = JiraModel,
            tools=[custom_jira_tool],
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