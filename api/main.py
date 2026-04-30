from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import bcrypt
from datetime import datetime

app = FastAPI()

# Configuração de Segurança (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FUNÇÕES DE BANCO DE DADOS ---
def conectar_banco():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(diretorio_atual, "estudos.db"))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT, 
            categoria TEXT, 
            tempo_foco INTEGER DEFAULT 25, 
            concluida INTEGER DEFAULT 0, 
            data_criacao TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE, 
            password TEXT
        )
    """)
    conn.commit()
    return conn

# --- FUNÇÕES DE SEGURANÇA ---
def gerar_senha_hash(password: str):
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72: pwd_bytes = pwd_bytes[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verificar_senha(password: str, hashed_password: str):
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72: pwd_bytes = pwd_bytes[:72]
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))

# --- ROTAS DE LOGIN E CADASTRO ---
@app.post("/cadastro")
def cadastro(dados: dict):
    username = dados.get("username")
    password = dados.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Dados incompletos")
    senha_hash = gerar_senha_hash(password)
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, senha_hash))
        conn.commit()
        conn.close()
        return {"status": "Usuário criado!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Usuário já existe!")

@app.post("/login")
def login(dados: dict):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (dados["username"],))
    user = cursor.fetchone()
    conn.close()
    if user and verificar_senha(dados["password"], user[0]):
        return {"status": "sucesso", "username": dados["username"]}
    raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

# --- ROTAS DE TAREFAS (CORRIGIDAS E ÚNICAS) ---

@app.get("/tarefas")
def listar():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, concluida, data_criacao, categoria, tempo_foco FROM tarefas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return [{"id": t[0], "nome": t[1], "concluida": bool(t[2]), "data": t[3], "categoria": t[4], "tempo": t[5]} for t in dados]

@app.post("/tarefas")
def adicionar(item: dict):
    data_atual = datetime.now().strftime("%d/%m %H:%M")
    conn = conectar_banco()
    cursor = conn.cursor()
    # Enviando os 4 valores para os 4 espaços (?)
    cursor.execute("""
        INSERT INTO tarefas (nome, data_criacao, categoria, tempo_foco) 
        VALUES (?, ?, ?, ?)
    """, (item["nome"], data_atual, item.get("categoria", "Estudo"), item.get("tempo_foco", 25)))
    conn.commit()
    conn.close()
    return {"status": "Adicionado!"}

@app.put("/tarefas/{id_tarefa}")
def alternar_status(id_tarefa: int):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = NOT concluida WHERE id = ?", (id_tarefa,))
    conn.commit()
    conn.close()
    return {"status": "Status atualizado!"}

@app.put("/tarefas/editar/{id_tarefa}")
def editar_tarefa(id_tarefa: int, item: dict):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET nome = ? WHERE id = ?", (item["nome"], id_tarefa))
    conn.commit()
    conn.close()
    return {"status": "Editado!"}

@app.delete("/tarefas/{id_tarefa}")
def excluir(id_tarefa: int):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
    conn.commit()
    conn.close()
    return {"status": "Excluído!"}

@app.delete("/limpar")
def limpar():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas")
    conn.commit()
    conn.close()
    return {"status": "Banco limpo!"}

# Inicialização automática
conectar_banco()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
