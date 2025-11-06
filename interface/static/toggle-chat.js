document.addEventListener("DOMContentLoaded", () => {
    const chatbotButton = document.getElementById("chatbot-button");
    const chatContainer = document.getElementById("chat-container");

    // Segurança: se os elementos não existirem (novo UI), não faz nada.
    if (!chatbotButton || !chatContainer) return;

    chatbotButton.addEventListener("click", () => {
        chatContainer.classList.toggle("hidden");
    });
});