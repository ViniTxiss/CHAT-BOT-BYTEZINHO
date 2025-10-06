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