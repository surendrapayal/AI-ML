import os
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from crews.priority_identification_crew.priority_identification_crew import PriorityIdentificationCrew

class GNOCPriorityModel(BaseModel):
    description: str = ""
    summary: str = ""
    segment: str = ""
    product: str = ""
    priority: str = ""
    impact: str = ""
    urgency: str = ""
    priority_identification_response: str = ""
    issue_reported: str = ""
    # jira_id: str = ""
    # status_io_id: str = ""
    # white_board_id: str = ""
    # white_board_link: str = ""
    # subject: str = ""
    # to: list = None
    # body: str = ""
    # subject1: str = ""
    # subject2: str = ""
    # body1: str = ""
    # body2: str = ""


class GNOCPriorityFlow(Flow[GNOCPriorityModel]):

    @start()
    def generate_issue_reported_user(self):
        print(f"Generating issue reported by user-  {self.state.issue_reported}")
        # self.state.issue_reported = "We are experiencing a critical issue in the merchant segment impacting our Transit product. Customers have been unable to perform Mastercard card transactions for the past 15 minutes, resulting in significant disruption. Approximately 10,000 transactions have been declined during this time, leading to a revenue loss of $50,000. This issue is affecting multiple merchants and requires immediate attention. The root cause appears to be related to the processing system for Mastercard transactions on the Transit product. Please prioritize this issue, as it has a high financial impact and is negatively affecting customer experience."
        #self.state.issue_reported = "We are facing a critical issue in the issuing segment, specifically impacting our INTL Citi Bank product. The problem has resulted in Visa and Mastercard transactions failing across multiple channels. The issue has led to more than 100,000 transaction failures, causing significant disruption to the client’s operations. The estimated revenue loss exceeds $1 million, highlighting the severity of the situation. This outage is negatively impacting customer trust and requires immediate investigation to identify and resolve the root cause. Prompt action is needed to mitigate further losses and restore normal transaction processing for the INTL Citi Bank product."
        return {"data": {}}

    @listen(generate_issue_reported_user)
    def identify_priority_of_issue(self, context):
        print("Identifying the priority of the issue reported by user.")
        result = (
            PriorityIdentificationCrew()
            .crew()
            .kickoff(inputs={"issue_reported": self.state.issue_reported})
        )

        self.state.description = result["description"]
        self.state.summary = result["summary"]
        self.state.segment = result["segment"]
        self.state.product = result["product"]
        self.state.priority = result["priority"]
        self.state.impact = result["impact"]
        self.state.urgency = result["urgency"]
        self.state.priority_identification_response = result.raw
        print("\n################################")
        print(f"identify_priority_of_issue :: Raw result:- {result.raw}")
        context["data"]["issue_summary"] = result["summary"]
        context["data"]["issue_description"] = result["description"]
        context["data"]["issue_priority"] = result["priority"]
        context["data"]["issue_impact"] = result["impact"]
        context["data"]["issue_segment"] = result["segment"]
        context["data"]["issue_product"] = result["product"]
        context["data"]["urgency"] = result["urgency"]
        return context

def kickoff(issue_reported):
    print(f"issue_reported:- {issue_reported}")
    # issue_reported = "We are experiencing a critical issue in the merchant segment impacting our Transit product. Customers have been unable to perform Mastercard card transactions for the past 15 minutes, resulting in significant disruption. Approximately 10,000 transactions have been declined during this time, leading to a revenue loss of $50,000. This issue is affecting multiple merchants and requires immediate attention. The root cause appears to be related to the processing system for Mastercard transactions on the Transit product. Please prioritize this issue, as it has a high financial impact and is negatively affecting customer experience."
    # issue_reported = "We are facing a critical issue in the issuing segment, specifically impacting our INTL Citi Bank product. The problem has resulted in Visa and Mastercard transactions failing across multiple channels. The issue has led to more than 100,000 transaction failures, causing significant disruption to the client’s operations. The estimated revenue loss exceeds $1 million, highlighting the severity of the situation. This outage is negatively impacting customer trust and requires immediate investigation to identify and resolve the root cause. Prompt action is needed to mitigate further losses and restore normal transaction processing for the INTL Citi Bank product."
    gnoc_priority_flow = GNOCPriorityFlow()
    result = gnoc_priority_flow.kickoff(inputs={"issue_reported": issue_reported})
    print("******************************************")
    for inner_key, inner_value in result["data"].items():
        print(f"  Inner key: {inner_key}, Inner value: {inner_value}")
    return result

def plot():
    gnoc_priority_flow = GNOCPriorityFlow()
    gnoc_priority_flow.plot()


if __name__ == "__main__":
    kickoff()