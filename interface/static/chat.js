document.addEventListener("DOMContentLoaded", () => {
    // --- Lógica para a página do chat (chat.html) ---
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.getElementById("send-btn");
    const chatbox = document.querySelector(".chatbox");
    const initialView = document.getElementById("initial-view");
    const predefinedQuestions = document.querySelectorAll(".predefined-questions a");

    // Se não encontrar os elementos do chat, interrompe a execução
    if (!chatInput || !sendChatBtn || !chatbox) return;

    let userMessage;

    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat-message", className);
        // Adiciona o ícone do bot apenas para as mensagens do bot
        let chatContent = className === "bot-message" 
            ? `<span class="material-symbols-outlined">smart_toy</span><p></p>` 
            : `<p></p>`;
        chatLi.innerHTML = chatContent;
        // Adiciona a mensagem de texto ao parágrafo
        if (message) {
            chatLi.querySelector("p").textContent = message;
        }
        return chatLi;
    }

    const generateResponse = (incomingChatLi) => {
        const API_URL = "/chat";
        const messageElement = incomingChatLi.querySelector("p");

        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: userMessage
            })
        }

        fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
            messageElement.textContent = data.response;
        }).catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Algo deu errado. Por favor, tente novamente.";
        }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
    }

    const handleChat = (message) => {
        userMessage = message.trim();
        if (!userMessage) return;

        // Esconde a visão inicial e limpa o input
        if (initialView) initialView.style.display = "none";
        chatInput.value = "";

        chatbox.appendChild(createChatLi(userMessage, "user-message"));
        chatbox.scrollTo(0, chatbox.scrollHeight);

        setTimeout(() => {
            // Cria um balão de "Digitando..."
            const incomingChatLi = createChatLi(null, "bot-message");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            generateResponse(incomingChatLi);
        }, 600);
    }

    predefinedQuestions.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            handleChat(link.dataset.question);
        });
    });

    sendChatBtn.addEventListener("click", () => handleChat(chatInput.value));
    
    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleChat(chatInput.value);
        }
    });
});