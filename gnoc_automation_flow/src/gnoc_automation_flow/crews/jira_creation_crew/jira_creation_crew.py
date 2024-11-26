from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from gnoc_automation_flow.src.gnoc_automation_flow.tools.custom_tool import JiraTool

# from gnoc_automation_flow.JiraTool import jira_tool

# from gnoc_automation_flow.tools.custom_tool import jira_tool

llm=ChatOpenAI(
    model_name="ollama/llama3.1:latest",
    api_key="your-api-key",
    base_url= "http://localhost:11434/v1",
    # temperature=0.5
)

@CrewBase
class JiraCreationCrew():
    """Jira Creation Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def jira_creation_agent(self) -> Agent:
        # j_tool = JiraTool.jira_tool()
        return Agent(
            config=self.agents_config['jira_creation_agent'],
            llm=llm,
            tools=[JiraTool.jira_tool]
        # tools = [jira_tool()]
        )

    @task
    def jira_creation_task(self) -> Task:
        # j_tool = JiraTool.jira_tool()
        return Task(
            config=self.tasks_config['jira_creation_task'],
            # output_pydantic = JiraModel
            # tools=[jira_tool]
            tools=[JiraTool.jira_tool]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )