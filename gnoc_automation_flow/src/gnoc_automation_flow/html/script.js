const chatBody = document.getElementById("chatBody");
const userInput = document.getElementById("userInput");

// Append a message to the chat
function appendMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Send a message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Append user message
    appendMessage(message, "user");
    userInput.value = "";

    // Simulate bot typing
    appendMessage("Typing...", "bot");
    const botMessages = document.querySelectorAll(".message.bot");
    const typingIndicator = botMessages[botMessages.length - 1];

    try {
        // Call Crewai agent API
        const response = await callCrewaiAgent(message);

        // Replace typing indicator with response
        typingIndicator.textContent = response;
    } catch (error) {
        typingIndicator.textContent = "An error occurred. Please try again.";
    }
}

// Mock Crewai agent API call
async function callCrewaiAgent(userMessage) {
    const apiUrl = "https://your-crew-ai-endpoint.com/agent"; // Replace with your Crewai agent endpoint
    const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    });

    if (!response.ok) {
        throw new Error("Failed to communicate with Crewai agent");
    }

    const data = await response.json();
    return data.reply; // Adjust this according to your API's response structure
}
