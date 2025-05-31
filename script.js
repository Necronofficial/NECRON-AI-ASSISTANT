const micBtn = document.getElementById('micToggle');
const speakerBtn = document.getElementById('speakerToggle');
const sendBtn = document.querySelector('.chat-box img[alt="Send"]');
const input = document.querySelector('.chat-box input');
const chatHistory = document.getElementById('chat');

let micOn = true;
let speakerOn = true;

// Toggle Mic
micBtn.addEventListener('click', () => {
  micOn = !micOn;
  micBtn.src = micOn ? 'micon-icon.png' : 'micoff-icon.png';
  fetch('/toggle_mic', { method: 'POST', body: JSON.stringify({ mic: micOn }), headers: { 'Content-Type': 'application/json' } });
});

// Toggle Speaker
speakerBtn.addEventListener('click', () => {
  speakerOn = !speakerOn;
  speakerBtn.src = speakerOn ? 'speakeron-icon.png' : 'speakeroff-icon.png';
  fetch('/toggle_speaker', { method: 'POST', body: JSON.stringify({ speaker: speakerOn }), headers: { 'Content-Type': 'application/json' } });
});

// Send Message
sendBtn.addEventListener('click', async () => {
  const message = input.value.trim();
  if (!message) return;
  addMessage('user', message);
  input.value = '';

  const res = await fetch('/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
    headers: { 'Content-Type': 'application/json' }
  });

  const data = await res.json();
  addMessage('ai', data.reply || 'Sorry, no response.');
});

function addMessage(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.classList.add('message', sender);
  msgDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'FRIDAY'}:</strong> ${text}`;
  chatHistory.appendChild(msgDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}
