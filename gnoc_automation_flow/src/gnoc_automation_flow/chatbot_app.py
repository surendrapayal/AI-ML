import base64
import os

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

image_path = f"{os.getcwd()}/gp.png"

# Streamlit app title
# st.title("Global Payments Chatbot")
st.markdown(
    f"""
    <h1 style="display: flex; align-items: center;">
        <img src="data:image/png;base64, {base64.b64encode(open(image_path, "rb").read()).decode()}" alt="Logo" style="width:50px; margin-right: 10px;">
        GNOC Personal Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

# Initialize session state for chatbot history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Add session state for user input (text_area)
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Display predefined operations in the chat interface
# operations = ["Report Incident", "Internet Search"]
# operation = st.selectbox("Choose an operation:", operations)

# Input box for user text
user_text = st.text_area("Enter your text:", key="user_input")

# If the user provides input and selects an operation, simulate chat
if st.button("Send"):
    # if operation and user_text:
    if user_text:
        # Fetch response from GNOC crews and append bot response
        # user_message = f"Operation Selected: {operation}\n\n"
        # user_message = user_message + f"Issue Reported: {user_text}\n\n"
        user_message = f"Issue Reported: {user_text}\n\n"
        st.session_state.messages.insert(0, {"role": "user", "content": user_message})
        # st.session_state.messages.append({"role": "user", "content": user_message})
        result = main.kickoff(user_text)

        # Append bot message
        # bot_response = f"**Operation Selected:** {operation}\n\n"
        # bot_response = bot_response + f"**Issue Reported:** {user_text}\n\n"
        # bot_response = f"<b>Issue Reported:</b> {user_text}\n\n"
        bot_response = ""

        if result["data"]["issue_description"].lower() == "This issue does not appear to be related to any GP products, and unfortunately, I am unable to proceed with further action. Thank you for your understanding.".lower():
            bot_response = bot_response + f"<b>Issue Description:</b> <span style='color:red;'>{result["data"]["issue_description"]}</span>"
            # bot_response = f"<p style='color:red;'>{bot_response}</p>"
        else:
            # bot_response = bot_response + f"**Issue Summary:** {result["data"]["issue_summary"]}\n\n"
            # bot_response = bot_response + f"**Issue Description:** {result["data"]["issue_description"]}\n\n"
            # bot_response = bot_response + f"**Issue Priority:** {result["data"]["issue_priority"]}\n\n"
            # bot_response = bot_response + f"**Issue Segment:** {result["data"]["issue_segment"]}\n\n"
            # bot_response = bot_response + f"**Issue Product:** {result["data"]["issue_product"]}\n\n"
            # bot_response = bot_response + f"**Jira Information:** [{result["data"]["jira_information"]}]({result["data"]["jira_link"]})\n\n"
            # bot_response = bot_response + f"**Status IO Page Information:** [Status IO Page]({result["data"]["status_io_page_link"]})\n\n"
            # bot_response = bot_response + f"**White Board Information:** [White Board]({result["data"]["white_board_information"]})\n\n"

            bot_response = bot_response + f"<b>Issue Summary:</b> {result["data"]["issue_summary"]}\n\n"
            bot_response = bot_response + f"<b>Issue Description:</b> {result["data"]["issue_description"]}\n\n"
            bot_response = bot_response + f"<b>Issue Priority:</b> {result["data"]["issue_priority"]}\n\n"
            bot_response = bot_response + f"<b>Issue Segment:</b> {result["data"]["issue_segment"]}\n\n"
            bot_response = bot_response + f"<b>Issue Product:</b> {result["data"]["issue_product"]}\n\n"
            bot_response = bot_response + f"<b>Jira Information:</b> <a href='{result["data"]["jira_link"]}'>{result["data"]["jira_information"]}</a>\n\n"
            bot_response = bot_response + f"<b>Status IO Page Information:</b> <a href='{result["data"]["status_io_page_link"]}'>Status IO Page</a>\n\n"
            bot_response = bot_response + f"<b>White Board Information:</b> <a href='{result["data"]["white_board_information"]}'>White Board</a>\n\n"


        st.session_state.messages.insert(1, {"role": "bot", "content": bot_response})
        # st.session_state.messages.append({"role": "bot", "content": bot_response})

        # bot_response = fetch_from_gemini(operation, user_text)
        # st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        message(msg["content"], is_user=True, allow_html=True)
    else:
        message(msg["content"], is_user=False, allow_html=True)
        # st.markdown(msg["content"], unsafe_allow_html=True)


# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
