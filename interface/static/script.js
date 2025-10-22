document.addEventListener("DOMContentLoaded", () => {
    // --- Lógica para a página principal (index.html) ---
    // Este script agora controla apenas o botão e a janela (iframe) na página principal.
    const chatbotButton = document.getElementById("chatbot-button");
    const chatbotWindow = document.getElementById("chatbot-window");

    if (chatbotButton && chatbotWindow) {
        chatbotButton.addEventListener("click", () => {
            chatbotWindow.classList.toggle("hidden");
        });
    }
});

try {
    // enviar a pergunta para a api do backend
    const response = await fetch('http://127.0.0.1:5000/perguntar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pergunta: perguntaUsuario }),
    });

    if (!response.ok) {
        throw new Error('a resposta da API não foi ok');    
    
    }

    const data = await response.json();
    const respostaBot = data.resposta;
}

    adicionarMensagemAoChat(respostaBot, 'bot');

