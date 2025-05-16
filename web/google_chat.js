// Suggested code may be subject to a license. Learn more: ~LicenseLog:3105838612.
// Suggested code may be subject to a license. Learn more: ~LicenseLog:3709306068.
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatBox = document.getElementById('chat-box');
    const typingIndicator = document.getElementById('typing-indicator'); // Get the element here
    // console.log('Typing Indicator Element:', typingIndicator); // Add this line

    // Initialize markdown-it
    const md = new markdownit();
    
    
    // Function to display messages
    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender === 'user' ? 'sent' : 'received', 'responsive');
        const renderedMessage = md.render(message); // Render markdown to HTML
        messageElement.innerHTML = `<div class="message-bubble">${renderedMessage}</div>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
    }

    // Function to send a message
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') {
            return; // Don't send empty messages
        }

        displayMessage(message, 'user'); // Display user's message

        messageInput.value = ''; // Clear the input field

        typingIndicator.style.display = 'flex'; // Show typing indicator

        try {
            const response = await fetch('/google_chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Response:', data[0].content.parts[0].text);
            displayMessage(data[0].content.parts[0].text, 'bot'); // Display bot's reply
        } catch (error) {
            displayMessage('Error: Could not send message.', 'bot'); // Display error message
        } finally {
            typingIndicator.style.display = 'none'; // Hide typing indicator
        }
    }

    // Event listener for send button click
    sendButton.addEventListener('click', sendMessage);

    // Event listener for pressing Enter in the input field
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default form submission
            sendMessage();
        }
    });
});
