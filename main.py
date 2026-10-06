# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional

# app = FastAPI(title="Estúdio de Tatuagem - Agendamento e Fila")

# # --- BANCO DE DADOS EM MEMÓRIA (Temporário para testes) ---
# # Como estamos começando, usaremos listas comuns para salvar os dados enquanto a API roda.
# banco_clientes = []
# fila_espera = []
# banco_agendamentos = []

# # --- MODELOS DE DADOS ---
# # Define o que o Python espera receber quando um cliente for cadastrado
# class Cliente(BaseModel):
#     id: int
#     nome: str
#     telefone: str
#     estilo_tatuagem: str

#     class Agendamento(BaseModel):
#         id: int
#         cliente_id: int
#         data_hora: str # Formato esperado: "2026-10-15 14:00"
#         tatuador: str

# # --- ROTAS DA API (ENDPOINTS) ---

# # 1. Rota de boas-vindas
# @app.get("/")
# def home():
#     return {"mensagem": "Bem-vindo à API do Estúdio de Tatuagem!"}

# # 2. Rota para cadastrar um cliente
# @app.post("/clientes/", response_model=Cliente)
# def cadastrar_cliente(cliente: Cliente):
#     # Verifica se o ID já existe
#     for c in banco_clientes:
#         if c.id == cliente.id:
#             raise HTTPException(status_code=400, detail="ID de cliente já cadastrado.")
    
#     banco_clientes.append(cliente)
#     return cliente

# # 3. Rota para listar todos os clientes cadastrados
# @app.get("/clientes/", response_model=List[Cliente])
# def listar_clientes():
#     return banco_clientes

# # 4. Rota para adicionar um cliente na FILA DE ESPERA (Ordem de chegada)
# @app.post("/fila/{cliente_id}")
# def entrar_na_fila(cliente_id: int):
#     # Verifica se o cliente existe no banco de dados
#     cliente_encontrado = None
#     for c in banco_clientes:
#         if c.id == cliente_id:
#             cliente_encontrado = c
#             break
            
#     if not cliente_encontrado:
#         raise HTTPException(status_code=404, detail="Cliente não encontrado. Cadastre-o primeiro.")
    
#     # Evita duplicados na fila
#     if cliente_encontrado in fila_espera:
#         return {"mensagem": f"{cliente_encontrado.nome} já está na fila."}
        
#     fila_espera.append(cliente_encontrado)
#     return {"mensagem": f"{cliente_encontrado.nome} foi adicionado à fila de espera!", "posicao": len(fila_espera)}

# # 5. Rota para ver a fila de espera atual
# @app.get("/fila/")
# def ver_fila():
#     return {"fila_atual": [c.nome for c in fila_espera]}

# #6. Rota para cancelar um agendamento existente
# @app.delete("/agendamentos/{agendamento_id}")
# def cancelar_agendamento(agendamento_id: int):
#     #Procura o agendamento na lista pelo ID fornecido
#     agendamento_encontrado = None
#     for a in banco_agendamentos:
#         if a.id == agendamento_id:
#             agendamento_encontrado = a
#             break

#     #Se o agendamento não existir, avisa o usuário
#     if not agendamento_encontrado:
#         raise HTTPException(status_code=404, detail=f"Agendamento com ID {agendamento_id} não foi encontrado.")

#     #Se encontrou, remove o agentamento da lista
#     banco_agendamentos.remove(agendamento_encontrado)

#     return {"mensagem": f"Agendamento {agendamento_id} cancelado com sucesso."}

# #7. Rota para agendamentos (horários marcados)
# @app.post("/agendamentos/", response_model=Agendamento)
# def criar_agendamento(Agendamento: Agendamento):
#     #Verifica se o cliente existe
#     cliente_existe = any(c.id == agendamento.cliente_id for c in banco_clientes)
#     if not cliente_existe:
#         raise HTTPException(status_code=404, detail="Este tatuador não possui este horário disponível.")

#     banco_agendamentos.append(agendamento)
#     return agendamento

# @app.get("/agendamentos/", response_model=List[Agendamento])
# def listar_agendamentos():
#     return banco_agendamentos






#reestruturando o código após alguns erros e o mantendo antiormente para revisão e análise de aprendizado.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import sqlite3
nome_banco = "estudio.db"

def conectar():
    conexao = sqlite3.connect(nome_banco)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabelas():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            estilo_tatuagem TEXT NOT NULL,
            local_tatuagem TEXT NOT NULL
        )   
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS fila_espera (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    """)

    conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY,
            cliente_id INTEGER NOT NULL,
            data_hora TEXT NOT NULL,
            tatuador TEXT NOT NULL,
            UNIQUE (data_hora, tatuador),
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )

    """)

    conexao.commit()
    conexao.close()

criar_tabelas()

app = FastAPI(title="Estúdio de Tatuagem - Agendamento e Fila")


# --- LISTA OFICIAL DE TATUADORES DO ESTÚDIO ---
# Modifique os nomes abaixo para os profissionais do seu estúdio fictício!
tatuadores_permitidos = ["Bianca", "Gabi", "Rafael"]

# ==============================================================================
# 2. MODELOS DE DADOS (Classes - Devem vir antes de qualquer rota)
# ==============================================================================
class Cliente(BaseModel):
    id: int
    nome: str
    telefone: str
    estilo_tatuagem: str
    local_tatuagem: str

class Agendamento(BaseModel):
    id: int
    cliente_id: int
    data_hora: str  # Formato esperado: "2026-10-15 14:00"
    tatuador: str
# ==============================================================================
# 3. ROTAS DA API (ENDPOINTS)
# ==============================================================================

# --- Rota de boas-vindas ---
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API do Estúdio de Tatuagem!"}

# --- Rotas para Clientes ---
@app.post("/clientes/", response_model=Cliente)
def cadastrar_cliente(cliente: Cliente):
    conexao = conectar()
    try:
        conexao.execute(
            """
            INSERT INTO clientes (id, nome, telefone, estilo_tatuagem, local_tatuagem)
            VALUES (?,?,?,?,?)
            """,
            (cliente.id, cliente.nome, cliente.telefone, cliente.estilo_tatuagem, cliente.local_tatuagem),
        )
        conexao.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="ID de cliente já cadastrado.")
    finally:
        conexao.close()
    return cliente

@app.get("/clientes/", response_model=List[Cliente])
def listar_clientes():
    conexao = conectar()
    linhas = conexao.execute("SELECT * FROM clientes").fetchall()
    conexao.close()
    return [dict(linha) for linha in linhas]


# --- Rotas para Fila de Espera ---
@app.post("/fila/{cliente_id}")
def entrar_na_fila(cliente_id: int):
    conexao = conectar()
    try:
        cliente = conexao.execute(
            "SELECT nome FROM clientes WHERE id = ?", (cliente_id,),
        ).fetchone()

        if cliente is None:
            raise HTTPException(status_code=404, detail="CLiente não encontrado. Cadastre-o primeiro.")

        ja_na_fila = conexao.execute(
            "SELECT 1 FROM fila_espera WHERE cliente_id = ?", (cliente_id,)
        ).fetchone()

        if ja_na_fila:
            return {"mensagem": f"{cliente['nome']} já está na fila."}

        conexao.execute("INSERT INTO fila_espera (cliente_id) VALUES (?)", (cliente_id,))
        conexao.commit()

        posicao = conexao.execute("SELECT COUNT(*) FROM fila_espera").fetchone()[0]
        return {"mensagem": f"{cliente['nome']} foi adicionado à fila de espera!", "Posição": posicao}

    finally:
        conexao.close()
   

@app.get("/fila/")
def ver_fila():
    conexao = conectar()
    linhas = conexao.execute(
        """
        SELECT clientes.id AS id_cliente, clientes.nome AS nome_cliente
        FROM fila_espera
        JOIN clientes ON clientes.id = fila_espera.cliente_id
        ORDER BY fila_espera.id
        """
    ).fetchall()
    conexao.close()

    fila = []
    for posicao, linha in enumerate(linhas, start=1):
        fila.append({
            "posicao": posicao,
            "nome": linha["nome_cliente"],
            "id_cliente": linha["id_cliente"],
        })

    return {"fila_atual": fila}

@app.delete("/fila/{cliente_id}")
def sair_da_fila(cliente_id: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "DELETE FROM fila_espera WHERE cliente_id = ?", (cliente_id,)
        )   
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cliente não está na fila.")

        return {"mensagem": f"Cliente {cliente_id} saiu da fila de espera."}
    finally:
        conexao.close()

# --- Rotas para Agendamentos ---
@app.post("/agendamentos/", response_model=Agendamento)
def criar_agendamento(agendamento: Agendamento):
    if agendamento.tatuador not in tatuadores_permitidos:
        raise HTTPException(status_code=400, detail=f"O tatuador {agendamento.tatuador} não existe nesse estúdio.")

    conexao = conectar()
    try:
        cliente = conexao.execute(
            "SELECT 1 FROM clientes WHERE id = ?", (agendamento.cliente_id,)
        ).fetchone()

        if cliente is None:
            raise HTTPException(status_code=404, detail="Cliente não encontrado para este agendamento.")

        conexao.execute(
            """
            INSERT INTO agendamentos (id, cliente_id, data_hora, tatuador)
            VALUES (?,?,?,?)
            """,
            (agendamento.id, agendamento.cliente_id, agendamento.data_hora, agendamento.tatuador),
        )
        conexao.commit()
    except sqlite3.IntegrityError as erro:
        if "agendamentos.id" in str(erro):
            raise HTTPException(status_code=400, detail="ID de agendamento já cadastrado no sistema.")
        raise HTTPException(status_code=400, detail="Horário não disponível com este tatuador.")
    finally:
        conexao.close()

    return agendamento

@app.get("/agendamentos/", response_model=List[Agendamento])
def listar_agendamentos():
    conexao = conectar()
    linhas = conexao.execute("SELECT * FROM agendamentos ORDER BY data_hora").fetchall() # 2026-10-21 14:00
    conexao.close()
    return [dict(linha) for linha in linhas] 

@app.delete("/agendamentos/{agendamento_id}")
def cancelar_agendamento(agendamento_id: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "DELETE FROM agendamentos WHERE id = ?", (agendamento_id,)
        )
        conexao.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Agendamento com ID {agendamento_id} não foi encontrado.")

        return {"mensagem": f"Agendamento {agendamento_id} cancelado com sucesso."}
    finally:
        conexao.close()

