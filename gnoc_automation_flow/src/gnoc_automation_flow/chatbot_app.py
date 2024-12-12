import streamlit as st
from streamlit_chat import message
import requests
import main
import time

# Define a function to interact with Gemini API
def fetch_from_gemini(operation, text):
    url = "https://api.gemini.example/perform"  # Replace with the actual Gemini API endpoint
    payload = {"operation": operation, "text": text}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "No response received from Gemini.")
    except requests.exceptions.RequestException as e:
        return f"Error fetching response from Gemini: {e}"


# Streamlit app title
st.title("Global Payments Chatbot")

# Initialize session state for chatbot history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Add session state for user input (text_area)
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Display predefined operations in the chat interface
operations = ["Report Incident", "Internet Search"]
operation = st.selectbox("Choose an operation:", operations)

# Input box for user text
user_text = st.text_area("Enter your text:", key="user_input")

# If the user provides input and selects an operation, simulate chat
if st.button("Send"):
    if operation and user_text:
        # Fetch response from GNOC crews and append bot response
        user_message = f"Operation Selected: {operation}\n\n"
        user_message = user_message + f"Issue Reported: {user_text}\n\n"
        # st.session_state.messages.insert(0, {"role": "user", "content": user_message})
        st.session_state.messages.append({"role": "user", "content": user_message})
        result = main.kickoff(user_text)
        # Append user message
        bot_response = f"**Operation Selected:** {operation}\n\n"
        bot_response = bot_response + f"**Issue Reported:** {user_text}\n\n"
        bot_response = bot_response + f"**Issue Summary:** {result["data"]["issue_summary"]}\n\n"
        bot_response = bot_response + f"**Issue Description:** {result["data"]["issue_description"]}\n\n"
        bot_response = bot_response + f"**Issue Priority:** {result["data"]["issue_priority"]}\n\n"
        bot_response = bot_response + f"**Issue Segment:** {result["data"]["issue_segment"]}\n\n"
        bot_response = bot_response + f"**Issue Product:** {result["data"]["issue_product"]}\n\n"
        bot_response = bot_response + f"**Jira Information:** [{result["data"]["jira_information"]}]({result["data"]["jira_link"]})\n\n"
        bot_response = bot_response + f"**Status IO Page Information:** [Status IO Page]({result["data"]["status_io_page_link"]})\n\n"
        bot_response = bot_response + f"**White Board Information:** [White Board]({result["data"]["white_board_information"]})\n\n"


        # st.session_state.messages.insert(0, {"role": "bot", "content": bot_response})
        st.session_state.messages.append({"role": "bot", "content": bot_response})

        # bot_response = fetch_from_gemini(operation, user_text)
        # st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True)
    else:
        message(msg["content"], is_user=False)


# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
