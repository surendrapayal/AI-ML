from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from ...types import EmailTemplate


from ...model.model_classes import EmailTemplate
from ...tools.custom_tool import custom_email_template_tool


# from langchain_openai import ChatOpenAI
# llm=ChatOpenAI(
#     model_name="ollama/llama3.1:latest",
#     api_key="your-api-key",
#     base_url= "http://localhost:11434/v1",
#     temperature=0.5
# )

@CrewBase
class GoogleCrew():
	"""Google Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def email_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['email_writer'],
			# llm=llm,
			max_iter=1,
			# cache=False
			# allow_delegation=True,
			verbose=True
		)

	@task
	def write_email(self) -> Task:
		return Task(
			config=self.tasks_config['write_email'],
			output_pydantic=EmailTemplate,
			tools=[custom_email_template_tool],
			output_file="EmailTemplate.html"
		)

	@task
	def write_email_no_data(self) -> Task:
		return Task(
			config=self.tasks_config['write_email_no_data'],
			output_pydantic=EmailTemplate,
			tools=[custom_email_template_tool],
			output_file="EmailTemplateNoData.html"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			cache=False
			# memory=False,
			# manager_llm=llm
		)
