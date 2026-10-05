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

# ==============================================================================
# 1. BANCO DE DADOS EM MEMÓRIA (Variáveis globais)
# ==============================================================================
banco_clientes = []
fila_espera = []
banco_agendamentos = []

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
    cliente_encontrado = None
    for c in banco_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
            
    if not cliente_encontrado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado. Cadastre-o primeiro.")
    
    if cliente_encontrado in fila_espera:
        return {"mensagem": f"{cliente_encontrado.nome} já está na fila."}
        
    fila_espera.append(cliente_encontrado)
    return {"mensagem": f"{cliente_encontrado.nome} foi adicionado à fila de espera!", "posicao": len(fila_espera)}

@app.get("/fila/")
def ver_fila():
    return {"fila_atual": [c.nome for c in fila_espera]}

# --- Rotas para Agendamentos ---
@app.post("/agendamentos/", response_model=Agendamento)
def criar_agendamento(agendamento: Agendamento):
    # Verifica se o id já existe
    for a in banco_agendamentos:
        if a.id == agendamento.id:
            raise HTTPException(status_code=400, detail="ID de agendamento já cadastrado no sistema.")
    # Verifica se o cliente existe
    cliente_existe = any(c.id == agendamento.cliente_id for c in banco_clientes)
    if not cliente_existe:
        raise HTTPException(status_code=404, detail="Cliente não encontrado para este agendamento.")

    if agendamento.tatuador not in tatuadores_permitidos:
        raise HTTPException(status_code=400, detail=f"O tatuador {agendamento.tatuador} não existe nesse estúdio.")

    
    # Valida conflito de horário para o mesmo tatuador
    for agendado in banco_agendamentos:
        if agendado.data_hora == agendamento.data_hora and agendado.tatuador == agendamento.tatuador:
            raise HTTPException(status_code=400, detail="Horário não disponível com este tatuador.")
            
    banco_agendamentos.append(agendamento)
    return agendamento

@app.get("/agendamentos/", response_model=List[Agendamento])
def listar_agendamentos():
    return banco_agendamentos

@app.delete("/agendamentos/{agendamento_id}")
def cancelar_agendamento(agendamento_id: int):
    agendamento_encontrado = None
    for a in banco_agendamentos:
        if a.id == agendamento_id:
            agendamento_encontrado = a
            break

    if not agendamento_encontrado:
        raise HTTPException(status_code=404, detail=f"Agendamento com ID {agendamento_id} não foi encontrado.")

    banco_agendamentos.remove(agendamento_encontrado)
    return {"mensagem": f"Agendamento {agendamento_id} cancelado com sucesso."}

@app.delete("/fila/{cliente_id}")
def sair_da_fila(cliente_id: int):
    for c in fila_espera:
        if c.id == cliente_id:
            fila_espera.remove(c)
            return {"mensagem":f"{c.nome} saiu da fila de espera."}

    raise HTTPException(status_code=404, detail="Cliente não está na fila.")
