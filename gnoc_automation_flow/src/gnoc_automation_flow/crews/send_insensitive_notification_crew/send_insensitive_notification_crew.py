from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from langchain_openai import ChatOpenAI
# from demo_flow.types import my_custom_email_calendar_tool_new
# from ...tools.custom_tool import my_custom_email_calendar_tool_no_data
from tools.custom_tool import insensitive_notification_tool


# from demo_flow.tools.custom_tool import MyCustomEmailInput

# llm=ChatOpenAI(
#     model_name="ollama/llama3.1:latest",
#     api_key="your-api-key",
#     base_url= "http://localhost:11434/v1",
#     # temperature=0.5
# )

@CrewBase
class GoogleSendNoDataCrew():
	"""Google Email and Calendar Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# @agent
	# def email_writer(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['email_writer'],
	# 		llm=llm,
	# 		allow_delegation=True,
	# 		verbose=True
	# 	)
	#
	# @task
	# def write_email(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['write_email'],
	# 		output_pydantic=MyCustomEmailInput
	# 	)

	@agent
	def send_insensitive_notification_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['send_insensitive_notification_agent'],
			# llm=llm,
			max_iter=1,
			# cache=False
		)

	@task
	def send_insensitive_notification_task(self) -> Task:
		return Task(
			config=self.tasks_config['send_insensitive_notification_task'],
			tools=[insensitive_notification_tool],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# memory=True,
			cache=False
		)
