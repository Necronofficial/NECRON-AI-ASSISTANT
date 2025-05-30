const micBtn = document.getElementById('micBtn');
const speakerBtn = document.getElementById('speakerBtn');
const sendBtn = document.getElementById('sendBtn');
const aiLogoContainer = document.querySelector('.ai-logo-container');

let micOn = false;
let speakerOn = true;

// Toggle Mic
micBtn.addEventListener('click', () => {
  micOn = !micOn;
  micBtn.classList.toggle('active', micOn);
  if (micOn) {
    aiLogoContainer.classList.add('listening');
  } else {
    aiLogoContainer.classList.remove('listening');
  }
});

// Toggle Speaker
speakerBtn.addEventListener('click', () => {
  speakerOn = !speakerOn;
  speakerBtn.classList.toggle('active', speakerOn);
});

// Send Message
sendBtn.addEventListener('click', () => {
  const input = document.getElementById('userInput');
  const message = input.value.trim();
  if (message) {
    addMessage('user', message);
    input.value = '';
    // Simulate AI response
    setTimeout(() => addMessage('ai', 'Sure, I can do that.'), 1000);
  }
});

function addMessage(sender, text) {
  const chatHistory = document.querySelector('.chat-history');
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);
  messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'FRIDAY'}:</strong> ${text}`;
  chatHistory.appendChild(messageDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}
