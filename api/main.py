from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def conectar_banco():
    conn = sqlite3.connect("estudos.db")
    cursor = conn.cursor()
    # Criando tabela com colunas de data e status
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT, 
            concluida INTEGER DEFAULT 0,
            data_criacao TEXT
        )
    """)
    conn.commit()
    return conn

@app.get("/tarefas")
def listar():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, concluida, data_criacao FROM tarefas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return [{"id": t[0], "nome": t[1], "concluida": bool(t[2]), "data": t[3]} for t in dados]

@app.post("/tarefas")
def adicionar(item: dict):
    data_atual = datetime.now().strftime("%d/%m %H:%M")
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (nome, data_criacao) VALUES (?, ?)", (item["nome"], data_atual))
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
