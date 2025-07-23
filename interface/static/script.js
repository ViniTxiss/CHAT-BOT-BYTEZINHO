document.addEventListener('DOMContentLoaded', () => {
    // Elementos do Widget
    const chatContainer = document.getElementById('chat-container');
    const toggleButton = document.getElementById('chat-toggle-button');
    const closeButton = document.getElementById('close-chat-btn');

    // Elementos do Chat
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    // Função para abrir/fechar o chat
    function toggleChat() {
        chatContainer.classList.toggle('open');
        // Foca no input quando o chat é aberto
        if (chatContainer.classList.contains('open')) {
            userInput.focus();
        }
    }

    // Event Listeners para abrir e fechar
    toggleButton.addEventListener('click', toggleChat);
    closeButton.addEventListener('click', toggleChat);

    // Lógica de envio de mensagem
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userMessage = userInput.value.trim();

        if (userMessage === '') return;

        addMessage(userMessage, 'user-message');
        userInput.value = '';

        // Adiciona um indicador de "digitando..."
        addTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            const botMessage = data.response;

            // Remove o indicador e adiciona a resposta do bot
            removeTypingIndicator();
            addMessage(botMessage, 'bot-message');

        } catch (error) {
            console.error('Erro ao comunicar com o chatbot:', error);
            removeTypingIndicator();
            addMessage('Desculpe, ocorreu um erro. Tente novamente mais tarde.', 'bot-message');
        }
    });

    function addMessage(text, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', className);
        const p = document.createElement('p');
        // Gemini pode retornar markdown, então usamos innerHTML para renderizar negrito, etc.
        // Uma biblioteca como 'marked' seria mais segura para markdown completo.
        p.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        messageElement.appendChild(p);
        chatBox.appendChild(messageElement);
        scrollToBottom();
    }

    function addTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('message', 'bot-message', 'typing-indicator');
        typingIndicator.innerHTML = `
            <p>
                <span></span><span></span><span></span>
            </p>
        `;
        chatBox.appendChild(typingIndicator);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});