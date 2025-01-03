import base64
import os
import streamlit as st
from streamlit_chat import message
import priority_main
import main
from typing import cast, List, Dict

i = 0
feedback_index = 0
image_path = f"{os.getcwd()}/gp.png"

def display_message():
    pass

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

if "feedback" not in st.session_state:
    st.session_state["feedback"] = {}  # Feedback for bot messages

# Add session state for user input (text_area)
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Input box for user text
user_text = st.text_area("Enter your text:", key="user_input_text_area")

# If the user provides input and selects an operation, simulate chat
if st.button("Send", key="send_button"):
    # if operation and user_text:
    if user_text:
        # Fetch response from GNOC crews and append bot response
        user_message = f"Issue Reported: {user_text}\n\n"
        st.session_state.messages.append({"role": "user", "content": user_message})
        result = priority_main.kickoff(user_text)

        # Append bot message
        bot_response = ""

        if result["data"]["issue_description"].lower() == "This issue does not appear to be related to any GP products, and unfortunately, I am unable to proceed with further action. Thank you for your understanding.".lower():
            bot_response = bot_response + f"<b>Issue Description:</b> <span style='color:red;'>{result["data"]["issue_description"]}</span>"
        else:
            bot_response = bot_response + f"<b>Issue Summary:</b> {result["data"]["issue_summary"]}\n\n"
            bot_response = bot_response + f"<b>Issue Description:</b> {result["data"]["issue_description"]}\n\n"
            bot_response = bot_response + f"<b>Issue Priority:</b> {result["data"]["issue_priority"]}\n\n"
            bot_response = bot_response + f"<b>Issue Segment:</b> {result["data"]["issue_segment"]}\n\n"
            bot_response = bot_response + f"<b>Issue Product:</b> {result["data"]["issue_product"]}\n\n"
            bot_response = bot_response + f"<b>Issue Impact:</b> {result["data"]["issue_impact"]}\n\n"
            bot_response = bot_response + f"<b>Issue Urgency:</b> {result["data"]["issue_urgency"]}\n\n"
            # bot_response = bot_response + f"<b>Jira Information:</b> <a href='{result["data"]["jira_link"]}'>{result["data"]["jira_information"]}</a>\n\n"
            # bot_response = bot_response + f"<b>Status IO Page Information:</b> <a href='{result["data"]["status_io_page_link"]}'>Status IO Page</a>\n\n"
            # bot_response = bot_response + f"<b>White Board Information:</b> <a href='{result["data"]["white_board_information"]}'>White Board</a>\n\n"

        messages = cast(List[Dict[str, str]], st.session_state["messages"])
        st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display chat messages
# for msg in reversed(st.session_state.messages):
# for idx, msg in enumerate(reversed(st.session_state.messages)):
for idx, msg in enumerate(st.session_state.messages):
    print(f"idx inside enumerate value:- {idx}")
    i += 1
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"role_user_{i}", allow_html=True)
    else:
        message(msg["content"], is_user=False, key=f"role_other_{i}", allow_html=True)

        if "Jira Information" not in msg["content"]:
            # Add thumbs-up and thumbs-down buttons for bot messages
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("👍", key=f"thumbs_up_{i}"):
                    feedback_index = idx
                    st.session_state.feedback[idx] = "up"
                    # Display specific feedback immediately
                    st.write("👍 Thumbs Up")
                    # bot_message = st.session_state["messages"][(idx + 1)]["content"]
                    bot_message = msg["content"]
                    print(f"#########bot_message:- {bot_message}")
                    if "This issue does not appear to be related to any GP products, and unfortunately, I am unable to proceed with further action. Thank you for your understanding.".lower() not in bot_message.lower():
                        bot_messages = bot_message.split("\n\n")
                        print(f"bot_messages:- {bot_messages}")
                        summary = bot_messages[0].split("</b>")[1].strip()
                        description = bot_messages[1].split("</b>")[1].strip()
                        priority = bot_messages[2].split("</b>")[1].strip()
                        segment = bot_messages[3].split("</b>")[1].strip()
                        product = bot_messages[4].split("</b>")[1].strip()
                        impact = bot_messages[5].split("</b>")[1].strip()
                        urgency = bot_messages[6].split("</b>")[1].strip()
                        print(f"Issue Summary:- {bot_messages[0].split("</b>")[1].strip()}")
                        print(f"Issue Description:- {bot_messages[1].split("</b>")[1].strip()}")
                        print(f"Issue Priority:- {bot_messages[2].split("</b>")[1].strip()}")
                        print(f"Issue Segment:- {bot_messages[3].split("</b>")[1].strip()}")
                        print(f"Issue Product:- {bot_messages[4].split("</b>")[1].strip()}")
                        print(f"Issue Impact:- {bot_messages[5].split("</b>")[1].strip()}")
                        print(f"Issue Urgency:- {bot_messages[6].split("</b>")[1].strip()}")
                        bot_response = ""
                        result = main.kickoff(summary, description, priority, segment, product, impact, urgency)
                        print(f"!!!!!!!!!!!!!!! result:- {result}")
                        bot_response = bot_response + f"<b>Jira Information:</b> <a href='{result["data"]["jira_link"]}'>{result["data"]["jira_information"]}</a>\n\n"
                        bot_response = bot_response + f"<b>Status IO Page Information:</b> <a href='{result["data"]["status_io_page_link"]}'>Status IO Page</a>\n\n"
                        bot_response = bot_response + f"<b>White Board Information:</b> <a href='{result["data"]["white_board_information"]}'>White Board</a>\n\n"
                        # bot_response = bot_response + f"<b>Jira Information:</b> JIRA-123\n\n"
                        # bot_response = bot_response + f"<b>Status IO Page Information:</b> STATUS-IO-54321\n\n"
                        messages = cast(List[Dict[str, str]], st.session_state["messages"])
                        st.session_state.messages.append({"role": "bot", "content": bot_response})
                        continue
            with col2:
                if st.button("👎", key=f"thumbs_down_{i}"):
                    feedback_index = idx
                    st.session_state.feedback[idx] = "down"
                    # Display specific feedback immediately
                    # bot_message = st.session_state["messages"][-(idx + 1)]["content"]
                    # st.write(f"Feedback for this message ({idx}): {bot_message}")
                    st.write("👎 Thumbs Down")
                    st.write("Please provide more details so that the system can process your request.")

# Clear chat button
if st.button("Clear Chat", key="clear_chat_button"):
    st.session_state.messages = []
    st.session_state.feedback = {}

# Debugging: Display feedback
# if st.session_state["feedback"]:
#     st.write("Feedback collected:", st.session_state["feedback"])

# Debugging: Display feedback with bot message content
# if st.session_state["feedback"]:
#     st.write("Feedback collected:")
#     for idx, feedback in st.session_state["feedback"].items():
#         print(f"idx value:- {idx}")
#         print(f"i value:- {i}")
#         # Retrieve the corresponding bot message
#         bot_message = st.session_state["messages"][-(idx + 1)]["content"]
#         st.write(f"Message {idx}:")
#         st.write(bot_message)
#         st.write(f"Feedback: {feedback}")