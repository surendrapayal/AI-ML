from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from ...types import EmailTemplate


from model.model_classes import EmailTemplate
from tools.custom_tool import draft_email_template_tool


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
	def email_writer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['email_writer_agent'],
			# llm=llm,
			max_iter=1,
			# cache=False
			# allow_delegation=True,
			verbose=True
		)

	@task
	def sensitive_email_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['sensitive_email_writer_task'],
			output_pydantic=EmailTemplate,
			tools=[draft_email_template_tool],
			output_file="SensitiveEmailTemplate.html"
		)

	@task
	def insensitive_email_writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['insensitive_email_writer_task'],
			output_pydantic=EmailTemplate,
			tools=[draft_email_template_tool],
			output_file="InsensitiveEmailTemplate.html"
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
