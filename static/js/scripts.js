function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;

  appendMessage('user', message);
  input.value = '';

  fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message})
  })
  .then(res => res.json())
  .then(data => appendMessage('bot', data.reply))
  .catch(err => appendMessage('bot', 'Sorry, something went wrong.'));
}

function appendMessage(sender, text) {
  const chatBox = document.getElementById('chat-box');
  const msgDiv = document.createElement('div');
  msgDiv.className = `message ${sender}`;

  let formattedText = text;

  if (sender === 'bot') {
    const isItinerary = /🗓️ Day \d:/g.test(text);

    if (isItinerary) {
      // Format day headings and each activity with spacing
      formattedText = text
        .replace(/🗓️ Day \d:/g, match => `<h4>${match}</h4>`)
        .replace(/\n{2,}/g, '<br>')
        .replace(/\n/g, '</div><div style="margin-bottom: 8px;">')
        .replace(/^/, '<div style="margin-bottom: 8px;">')
        .concat('</div>');
    } else {
      // For general responses, preserve line breaks and bullets
      formattedText = text.replace(/\n/g, '<br>');
    }
  }

  msgDiv.innerHTML = `
    <img class="avatar" src="/static/${sender}.png">
    <div class="text">${formattedText}</div>`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}