import { streamGemini } from './gemini-api.js';

let form = document.querySelector('form');
let promptInput = document.querySelector('input[name="prompt"]');
let chatbotButton = document.getElementById('chatbotButton');

let chatForm = document.getElementById('chat-form'); // Select the form with id "chat-form"

async function sendMessage() {
  const messageInput = document.getElementById('user-input'); // Get the input field
  const message = messageInput.value.trim();
  if (!message) return;

  displayMessage('user', message);
  messageInput.value = '';

  try {
    const response = await fetch('/chatbot', { // Assuming you have a '/chat' endpoint in your backend
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    displayMessage('bot', data.response);
  } catch (error) {
    console.error('Error sending message:', error);
    displayMessage('bot', 'Sorry, something went wrong.');
  }
}

if (chatbotButton) {
  chatbotButton.addEventListener('click', () => {
    window.location.href = 'chatbot.html';
  });
}

// Add event listener to the form's submit event
if (chatForm) {
  chatForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    sendMessage();
  });
}

// Assuming you have a div with id 'chat-box' in chatbot.html for displaying messages
function displayMessage(sender, message) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', `${sender}-message`);
  messageElement.textContent = message;
  chatArea.appendChild(messageElement);
  chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll to the latest message
}
let chatArea = document.getElementById('chat-box'); // Select the chat area div
