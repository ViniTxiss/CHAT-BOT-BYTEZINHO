from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys
import logging

# Adiciona o diretório raiz ao path para encontrar o main.py e outros módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa as funções do seu arquivo main.py
from main import carregar_conhecimento, iniciar_gemini, responder_com_gemini

# Configura o logging para exibir informações úteis no console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- INICIALIZAÇÃO DO CHATBOT ---
# Carrega as variáveis de ambiente do arquivo .env na raiz do projeto
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

base_conhecimento = None
chat_session = None

try:
    logging.info("Iniciando o chatbot...")
    # Define o caminho para o arquivo de dados
    caminho_dados = os.path.join(os.path.dirname(__file__), '..', 'dados.txt')
    
    # Carrega a base de conhecimento e inicia o modelo Gemini
    base_conhecimento = carregar_conhecimento(caminho_dados)
    chat_session = iniciar_gemini()
    
    if not chat_session:
        raise ConnectionError("A sessão com o Gemini não pôde ser estabelecida.")

    logging.info("✅ Chatbot Gemini inicializado com sucesso!")

except Exception as e:
    # Não encerraremos a aplicação: permitimos que o servidor rode mesmo sem o modelo
    logging.error(f"❌ Erro ao inicializar o chatbot (modo degradado): {e}", exc_info=True)
    print("[Aviso] O chatbot não pôde ser inicializado. O servidor continuará rodando em modo degradado.")
    # base_conhecimento e chat_session permanecem None — a rota /chat irá responder com erro apropriado
# ------------------------------------

app = FastAPI()

# Configura os caminhos dos diretórios absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Configura os templates primeiro
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Configura os arquivos estáticos com nome explícito
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static_files")

# Define o modelo de dados para a requisição do chat
class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve a página principal do chat."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat-page", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Serve a página do iframe do chat."""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    """Recebe a mensagem do usuário e retorna a resposta do bot."""
    if not chat_session:
        raise HTTPException(status_code=500, detail="Desculpe, o chatbot não está disponível no momento.")

    user_message = chat_request.message
    if not user_message:
        raise HTTPException(status_code=400, detail="A mensagem não pode ser vazia.")

    bot_response = responder_com_gemini(chat_session, base_conhecimento, user_message)
    return JSONResponse(content={'response': bot_response})

if __name__ == "__main__":
    import uvicorn
    # Roda o servidor Uvicorn. O reload=True é ótimo para desenvolvimento.
    # Usamos reload=False aqui para evitar problemas com reloader em alguns ambientes
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=False)
