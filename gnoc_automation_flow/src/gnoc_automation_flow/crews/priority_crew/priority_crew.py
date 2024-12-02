import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai_tools.tools.file_read_tool.file_read_tool import FileReadTool
# from crewai_tools.tools.pdf_search_tool.pdf_search_tool import PDFSearchTool
from langchain_openai import ChatOpenAI
# from qdrant_client.http import model

# from demo_flow.tools.custom_tool import my_custom_email_tool_new
# from ...tools.custom_tool import text_reader
from ...tools.custom_tool import pdf_reader

# from langchain.llms import GoogleGemini

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "AIzaSyA7gyXPuz5b0AyyPERLcaanX6f2-NE_iWE"
#
# llm = GoogleGemini(model="gemini-pro")


# llm=ChatOpenAI(
#     model_name="ollama/llama3.1:latest",
#     api_key="your-api-key",
#     base_url= "http://localhost:11434/v1",
#     temperature=0.8,
#
# )

@CrewBase
class PriorityCrew():
	"""Priority Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def priority_analyzer(self) -> Agent:
		return Agent(
			config=self.agents_config['priority_analyzer'],
			# llm=llm,
			max_iter=1,
			# tools=[PDFSearchTool(file_path="C:\\MyData\\ai_ml_personal_project\\demo_flow\\IT Service Management Priority Definitions v1.pdf")]
			tools=[pdf_reader]
			# allow_delegation=True,
			# verbose=True
		)

	@task
	def priority_analyzer_task(self) -> Task:
		return Task(
			config=self.tasks_config['priority_analyzer_task'],
		)

	@agent
	def priority_identification(self) -> Agent:
		return Agent(
			config=self.agents_config['priority_identification'],
			# llm=llm,
			max_iter=1,
			# tools=[text_reader]
			# allow_delegation=True,
			# verbose=True
		)

	@task
	def priority_identification_task(self) -> Task:
		return Task(
			config=self.tasks_config['priority_identification_task'],
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
			# manager_llm=llm
		)
