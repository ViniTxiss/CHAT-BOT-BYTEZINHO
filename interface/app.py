from flask import Flask, render_template, request, jsonify
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
    logging.error(f"❌ Erro fatal ao inicializar o chatbot: {e}", exc_info=True)
    print("\n--- ERRO CRÍTICO: APLICAÇÃO NÃO PODE INICIAR ---")
    print("Ocorreu um erro durante a inicialização do chatbot, e a aplicação será encerrada.")
    print("Verifique o log de erro detalhado acima. Causas comuns incluem:\n  1. Chave de API (GOOGLE_API_KEY) ausente ou inválida no arquivo '.env'.\n  2. Arquivo 'dados.txt' não encontrado ou com formato incorreto.\n  3. Problemas de conexão com a internet.\n  4. Biblioteca 'google-generativeai' não instalada corretamente.")
    sys.exit(1) # Encerra a aplicação se o chatbot não puder ser inicializado
# ------------------------------------

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

# Rota para servir a cópia local do site para demonstração
@app.route('/site-local')
def site_local():
    return render_template('jovem_programador_sobre.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not chat_session:
        return jsonify({'response': 'Desculpe, o chatbot não está disponível no momento.'}), 500

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Mensagem não pode ser vazia.'}), 400

    bot_response = responder_com_gemini(chat_session, base_conhecimento, user_message)
    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)
