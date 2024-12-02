#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start

from .crews.priority_crew.priority_crew import PriorityCrew
# from .crews.read_file_crew.read_file_crew import ReadFileCrew
# from .crews.send_google_crew.send_google_crew import GoogleSendCrew
# from .crews.poem_crew.poem_crew import PoemCrew
# from .crews.google_crew.google_crew import GoogleCrew
# from .crews.read_txt_file_crew.read_txt_file_crew import ReadTextFileCrew


class PoemState(BaseModel):
    priority: str = ""
    description: str = ""
    issue_reported: str = ""
    jira_id: str = "Jira-12345"
    email: str = ""
    subject: str = ""
    body: str = ""
    summary: str = ""

class PoemFlow(Flow[PoemState]):

    @start()
    def generate_issue_reported_user(self):
        print("Generating issue reported by user")
        # self.state.issue_reported = "As a consumer I am not able to perform the transaction from the last 15 minutes and due to this over 500K transactions have declined that result in the revenue loss of more than 150K US dollar. Please look into this issue on urgent basis."
        self.state.issue_reported = "We are getting issue in the merchant segment. As a customer I am getting intermittent issue and some of the transaction are getting declined. AS of now only 1 customer is impacted and around 10 transaction have declined from last 6 hours. Please prioritize this issue."
        self.state.jira_id = "JIRA-12345"
        self.state.priority = "High"
        self.state.description = "The user is unable to perform transactions for the last 15 minutes, resulting in over 500K declined transactions with revenue loss of more than $150K US dollar."
        self.state.summary = "User unable to perform transactions, 500K+ declined, $150K+ revenue loss in last 15 minutes."
        # self.state.issue_reported = "As a user I am not able to perform the transaction from the last 5 minutes and due to this around 100 transactions have declined that result in the revenue loss of around 1000 US dollar. Please look into this issue and provide resolution."

    # @listen(generate_issue_reported_user)
    # def create_email_template(self):
    #     print("Creating email template")
    #     self.state.description = self.state.issue_reported
    #     result = (
    #         GoogleCrew()
    #         .crew()
    #         .kickoff(inputs={"jira_id": self.state.jira_id, "priority": self.state.priority, "description": self.state.description,
    #                          "project": "GNOC"})
    #     )
    #
    #     print("result.raw Email template created", result.raw)
    #     print("Email subject", result["subject"])
    #     print("Email body", result["body"])
    #     self.state.subject = result["subject"]
    #     self.state.body = result["body"]


    # @listen(create_email_template)
    # def send_email_gmail(self):
    #     print("Send email and calendar invite")
    #     subject_str = f"{self.state.jira_id} - {self.state.summary}"
    #     result = (
    #         GoogleSendCrew()
    #         .crew()
    #         .kickoff(inputs={"subject": subject_str, "body": self.state.body})
    #     )
    #
    #     print("Email template created", result.raw)

    # @listen(generate_issue_reported_user)
    # def identify_priority_of_issue(self):
    #     print("Identifying the priority of the issue reported by user.")
    #     result = (
    #         ReadTextFileCrew()
    #         .crew()
    #         .kickoff(inputs={"issue_reported": self.state.issue_reported})
    #     )

    # @listen(save_email_template)
    # def send_email_gmail(self):
    #     print("Send email")
    #     # self.state.description = self.state.issue_reported
    #     result = (
    #         GoogleSendCrew()
    #         .crew()
    #         # .kickoff(inputs={"to": "; ".join(self.state.to), "subject": self.state.subject, "body": self.state.body})
    #         .kickoff(inputs={"to": self.state.to, "subject": self.state.subject, "body": self.state.body})
    #     )
    #
    #     print("Email template created", result.raw)
    #     self.state.email = result.raw

    @listen(generate_issue_reported_user)
    def identify_priority_of_issue(self):
        print("Identifying the priority of the issue reported by user.")
        result = (
            PriorityCrew()
            .crew()
            .kickoff(inputs={"issue_reported": self.state.issue_reported})
        )

def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
