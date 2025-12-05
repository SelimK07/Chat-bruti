const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const resetBtn = document.getElementById('reset-btn');

const conversationId = 'conv_' + Date.now();

function addMessage(content, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<span></span><span></span><span></span>';
    
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

async function sendMessage(message) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });
        
        const data = await response.json();
        
        removeTypingIndicator();
        
        if (data.success) {
            addMessage(data.message, false);
        } else {
            addMessage('Oups ! Une erreur s\'est produite: ' + data.error, false);
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage('Erreur de connexion au serveur. Veuillez réessayer.', false);
    }
}

async function resetConversation() {
    try {
        await fetch('/api/reset', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                conversation_id: conversationId
            })
        });
        
        chatMessages.innerHTML = '';
        addMessage('Salut ! Je suis un chatbot complètement déjanté. Pose-moi une question, mais ne t\'attends pas à une réponse normale...', false);
    } catch (error) {
        addMessage('Erreur lors de la réinitialisation.', false);
    }
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    messageInput.value = '';
    
    sendBtn.disabled = true;
    showTypingIndicator();
    
    await sendMessage(message);
    
    sendBtn.disabled = false;
    messageInput.focus();
});

resetBtn.addEventListener('click', resetConversation);

messageInput.focus();
