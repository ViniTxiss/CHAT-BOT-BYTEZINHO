document.addEventListener("DOMContentLoaded", () => {
    const chatbotButton = document.getElementById("chatbot-button");
    const chatbotWindow = document.getElementById("chatbot-window");

    if (chatbotButton && chatbotWindow) {
        chatbotButton.addEventListener("click", () => {
            // Simplesmente abre/fecha a janela do chat
            chatbotWindow.classList.toggle("hidden");
        });
    }
});
