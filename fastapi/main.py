# main.py

import os
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# --- Configuração do Banco de Dados com SQLAlchemy ---

# Define a URL do banco de dados. Usaremos SQLite, que cria um arquivo 'tasks.db' no mesmo diretório.
DATABASE_URL = "sqlite:///./tasks.db"

# A 'engine' é o ponto de entrada para o banco de dados.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 'SessionLocal' é uma fábrica de sessões. Cada instância dela será uma sessão de banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 'Base' é uma classe base para nossos modelos de tabela do SQLAlchemy.
Base = declarative_base()

# --- Modelo da Tabela do Banco de Dados ---

# Define a estrutura da nossa tabela 'tasks' no banco de dados.
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

# Cria a tabela no banco de dados (se ela ainda não existir).
Base.metadata.create_all(bind=engine)

# --- Configuração do FastAPI ---

app = FastAPI()

# Configura o diretório 'templates' para conter nossos arquivos HTML.
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# --- Dependência para a Sessão do Banco de Dados ---

# Função para obter uma sessão do banco de dados para cada requisição.
# Isso garante que a sessão seja criada e fechada corretamente.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints da Aplicação ---

# Endpoint Principal (GET /): Renderiza a página HTML.
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    """
    Este endpoint busca todas as tarefas do banco de dados e
    renderiza a página 'index.html', passando as tarefas para ela.
    """
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Endpoint para Adicionar Tarefa (POST /add): Adiciona uma nova tarefa.
@app.post("/add", response_class=HTMLResponse)
async def add_task(request: Request, task_description: str = Form(...), db: Session = Depends(get_db)):
    """
    Este endpoint recebe a descrição da tarefa do formulário HTML,
    cria um novo objeto Task, adiciona ao banco de dados e
    recarrega a página principal para mostrar a lista atualizada.
    """
    # Cria uma nova tarefa com a descrição recebida.
    new_task = Task(description=task_description)
    
    # Adiciona a nova tarefa à sessão e comita (salva) no banco.
    db.add(new_task)
    db.commit()
    
    # Recarrega a página principal para mostrar a lista atualizada.
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# Endpoint para Deletar Tarefa (POST /delete/{task_id})
@app.post("/delete/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    """
    Encontra a tarefa pelo ID e a remove do banco de dados.
    """
    task_to_delete = db.query(Task).filter(Task.id == task_id).first()
    if task_to_delete:
        db.delete(task_to_delete)
        db.commit()

    # Recarrega a página principal.
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/update/{task_id}", response_class=HTMLResponse)
async def update_task(request: Request, task_id: int, new_description: str = Form(...),db: Session = Depends(get_db)):
    """
    Encontra a tarefa pelo ID e a remove do banco de dados.
    """
    task_to_update = db.query(Task).filter(Task.id == task_id).first()
    if task_to_update:
        task_to_update.description = new_description
        db.commit()

    # Recarrega a página principal.
    tasks = db.query(Task).all()
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

