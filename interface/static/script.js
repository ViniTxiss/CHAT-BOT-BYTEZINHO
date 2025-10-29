document.addEventListener("DOMContentLoaded", () => {
    const chatbotButton = document.getElementById("chatbot-button");
    const chatbotWindow = document.getElementById("chatbot-window");

    if (chatbotButton && chatbotWindow) {
        chatbotButton.addEventListener("click", () => {
            // Inverte a direção da timeline e a executa
            fabTimeline.reverse();
            fabTimeline.play();
            isFabOpen = !isFabOpen;

            // Abre a janela do chat apenas se o FAB não estiver sendo aberto
            if (!isFabOpen) {
                chatbotWindow.classList.toggle("hidden");
            }
        });
    }
});
