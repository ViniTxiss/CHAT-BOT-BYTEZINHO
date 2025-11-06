// Chatbot UI behavior (integrado ao backend /chat quando possível)
document.addEventListener('DOMContentLoaded', () => {
    console.log('[chatbot-ui] loaded');
    const chatbotToggler = document.getElementById('chatbot-toggler');
    const chatbotContainer = document.getElementById('chatbot-container');
    const closeBtn = document.getElementById('chatbot-close-btn');
    const chatBody = document.getElementById('chatbot-body');
    const inputField = document.getElementById('chatbot-input');
    const sendBtn = document.getElementById('chatbot-send-btn');
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    const timeElement = document.getElementById('current-time');

    function updateCurrentTime() {
        if (!timeElement) return;
        const now = new Date();
        timeElement.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    updateCurrentTime();
    setInterval(updateCurrentTime, 60 * 1000);

    // Se os elementos não existirem no momento do carregamento, usamos event delegation
    if (chatbotToggler && chatbotContainer) {
        console.log('[chatbot-ui] found elements, attaching direct listeners');
        chatbotToggler.addEventListener('click', () => {
            chatbotContainer.classList.add('active');
            chatbotContainer.setAttribute('aria-hidden', 'false');
            inputField && inputField.focus();
        });

        closeBtn && closeBtn.addEventListener('click', () => {
            chatbotContainer.classList.remove('active');
            chatbotContainer.setAttribute('aria-hidden', 'true');
        });
    } else {
        console.log('[chatbot-ui] elements not present yet — using delegated click handlers');
        // Delegation: escuta cliques no documento para abrir/fechar
        document.addEventListener('click', (e) => {
            try {
                const toggler = e.target.closest && e.target.closest('#chatbot-toggler');
                const close = e.target.closest && e.target.closest('#chatbot-close-btn');
                if (toggler) {
                    const container = document.getElementById('chatbot-container');
                    if (container) {
                        container.classList.add('active');
                        container.setAttribute('aria-hidden', 'false');
                        const input = document.getElementById('chatbot-input');
                        input && input.focus();
                        console.log('[chatbot-ui] opened via delegation');
                    } else console.warn('[chatbot-ui] container missing when trying to open');
                }
                if (close) {
                    const container = document.getElementById('chatbot-container');
                    if (container) {
                        container.classList.remove('active');
                        container.setAttribute('aria-hidden', 'true');
                        console.log('[chatbot-ui] closed via delegation');
                    }
                }
            } catch (err) {
                console.error('[chatbot-ui] delegation handler error', err);
            }
        });
    }

    function addMessage(message, isBot = false) {
        if (!chatBody) return;
        const wrapper = document.createElement('div');
        wrapper.className = `chat-message ${isBot ? 'bot' : 'user'}`;
        const now = new Date();
        const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        wrapper.innerHTML = `\n            <div class="message-content">${isBot ? '<strong>Bytezinho AI</strong>' : ''}<p>${escapeHtml(message)}</p><span class="message-time">${time}</span></div>\n        `;
        chatBody.appendChild(wrapper);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\"/g, "&quot;")
            .replace(/\'/g, "&#039;");
    }

    async function sendToServer(message) {
        // Tenta usar o endpoint /chat configurado no back-end
        try {
            const res = await fetch('/chat', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            if (!res.ok) throw new Error('Erro na resposta do servidor');
            const data = await res.json();
            return data.response || 'Desculpe, não obtive resposta.';
        } catch (err) {
            console.warn('Chatbot: erro ao chamar /chat, fallback local', err);
            return null; // sinaliza falha
        }
    }

    async function sendMessage() {
        const message = inputField.value.trim();
        if (!message) return;
        addMessage(message, false);
        inputField.value = '';

        // Mostrar um indicador simples de "digitando"
        const typing = document.createElement('div');
        typing.className = 'chat-message bot typing';
        typing.innerHTML = `<div class="message-content">...<\/div>`;
        chatBody.appendChild(typing);
        chatBody.scrollTop = chatBody.scrollHeight;

        const serverResp = await sendToServer(message);
        typing.remove();

        if (serverResp) {
            addMessage(serverResp, true);
        } else {
            // fallback simulado
            addMessage('Desculpe, ainda estou aprendendo a responder essa pergunta. (modo offline)', true);
        }
    }

    sendBtn && sendBtn.addEventListener('click', sendMessage);
    inputField && inputField.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const message = btn.getAttribute('data-message');
            if (!message) return;
            // Preenche o input e envia a mensagem automaticamente
            if (inputField) {
                inputField.value = message;
                inputField.focus();
            }
            console.log('[chatbot-ui] suggestion clicked, sending:', message);
            await sendMessage();
        });
    });

    // Permite clicar na bolha da mensagem para colapsá-la/ocultá-la
    if (chatBody) {
        chatBody.addEventListener('click', (e) => {
            try {
                const mc = e.target.closest && e.target.closest('.message-content');
                if (!mc) return;
                mc.classList.toggle('collapsed');
                console.log('[chatbot-ui] message toggled collapsed');
            } catch (err) {
                console.error('[chatbot-ui] error toggling message collapse', err);
            }
        });
    }

});
