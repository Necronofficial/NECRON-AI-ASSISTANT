// Element references
const micToggle = document.getElementById('micToggle');
const speakerToggle = document.getElementById('speakerToggle');
const sendIcon = document.querySelector('img[alt="Send"]');
const inputBox = document.querySelector('.chat-box input');
const chatContainer = document.querySelector('.main');

let micOn = true;
let speakerOn = false;

// Toggle Mic
micToggle.addEventListener('click', () => {
  micOn = !micOn;
  micToggle.src = micOn ? 'micon-icon.png' : 'micoff-icon.png';
});

// Toggle Speaker
speakerToggle.addEventListener('click', () => {
  speakerOn = !speakerOn;
  speakerToggle.src = speakerOn ? 'speakeron-icon.png' : 'speakeroff-icon.png';
});

// Send Message
sendIcon.addEventListener('click', sendMessage);

// Press Enter to Send
inputBox.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
  const msg = inputBox.value.trim();
  if (!msg) return;

  addMessage('user', msg);
  inputBox.value = '';

  // Simulate AI Response (Replace this with your backend call)
  setTimeout(() => {
    addMessage('ai', 'Sure, I can help with that.');
    if (speakerOn) {
      speak('Sure, I can help with that.');
    }
  }, 1000);
}

function addMessage(sender, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'message';
  msgDiv.style.margin = '10px 0';
  msgDiv.style.textAlign = sender === 'user' ? 'right' : 'left';
  msgDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'FRIDAY'}:</strong> ${text}`;
  chatContainer.appendChild(msgDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Text-to-Speech
function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}
