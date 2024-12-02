from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from langchain_openai import ChatOpenAI
# from demo_flow.tools.custom_tool import my_custom_email_tool_new

# from demo_flow.types import EmailTemplate
from ...types import EmailTemplate

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
			max_iter=1
			# allow_delegation=True,
			# verbose=True
		)

	@task
	def write_email(self) -> Task:
		return Task(
			config=self.tasks_config['write_email'],
			output_pydantic=EmailTemplate
		)

	# @agent
	# def email_send(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['email_send'],
	# 		llm=llm,
	# 		tools=[my_custom_email_tool_new],
	# 	)
	#
	# @task
	# def send_email(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['send_email'],
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# memory=False,
			# manager_llm=llm
		)
