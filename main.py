import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys
from typing import Optional

# --- Constantes ---
KNOWLEDGE_BASE_FILE = "dados.txt"
GEMINI_MODEL_NAME = "gemini-2.5-pro"
PROMPT_TEMPLATE = """
Use o conteúdo abaixo como base para responder a pergunta de forma direta, sem inventar nada que não esteja no texto.

=== BASE DE CONHECIMENTO ===
{base_conhecimento}

=== PERGUNTA ===
{pergunta_usuario}

Responda com base apenas no conteúdo da base acima.
"""

# Carrega as variáveis do .env
load_dotenv()

def carregar_conhecimento(caminho: str = KNOWLEDGE_BASE_FILE) -> Optional[str]:
    """
    Carrega a base de conhecimento de um arquivo de texto.

    Args:
        caminho: O caminho para o arquivo de dados.

    Returns:
        O conteúdo do arquivo como uma string, ou None se o arquivo não for encontrado.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ ERRO: Arquivo da base de conhecimento não encontrado em '{caminho}'.")
        return None

def iniciar_gemini() -> Optional[genai.ChatSession]:
    """
    Configura e inicia uma sessão de chat com a API do Google Gemini.

    Returns:
        Um objeto de sessão de chat, ou None se a API Key não for encontrada.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERRO: API KEY da Gemini não encontrada. Verifique seu arquivo .env.")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
        return model.start_chat()
    except Exception as e:
        print(f"❌ ERRO: Falha ao iniciar o modelo Gemini: {e}")
        return None

def responder_com_gemini(chat: genai.ChatSession, base_conhecimento: str, pergunta_usuario: str) -> str:
    """
    Envia uma pergunta para o Gemini e retorna a resposta formatada.

    Args:
        chat: A sessão de chat ativa.
        base_conhecimento: O texto com o contexto para a resposta.
        pergunta_usuario: A pergunta feita pelo usuário.

    Returns:
        A resposta gerada pelo modelo.
    """
    prompt = PROMPT_TEMPLATE.format(base_conhecimento=base_conhecimento, pergunta_usuario=pergunta_usuario)
    resposta = chat.send_message(prompt)
    return resposta.text.strip()

def iniciar_chatbot():
    """Inicia a interface de linha de comando para o chatbot."""
    chat = iniciar_gemini()
    base_conhecimento = carregar_conhecimento()

    if not chat or not base_conhecimento:
        print(" encerrando a aplicação.") # A mensagem de erro específica já foi impressa antes.
        sys.exit(1)

    print("🤖 Chatbot PJP (LLM Gemini) iniciado! Digite 'sair' para encerrar.")
    while True:
        pergunta = input("👤 Você: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("🤖 Até mais!")
            break
        resposta = responder_com_gemini(chat, base_conhecimento, pergunta) # type: ignore
        print(f"\n🤖 {resposta}\n")

if __name__ == "__main__":
    iniciar_chatbot()
