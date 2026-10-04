# from fastapi import FastAPI HTTPException
# from pydantic import BaseModel
# from typing import List, Optional

# app = FastAPI(title="Estúdio de Tatuagem - Agendamento e Fila")

# # -- BANCO DE DADOS EM MEMÓRIA (Temporário para testes) --
# # Como estou começando o projeto, usarei listas comuns para salvar os dados enquanto a API roda.

# banco_clientes = []
# fila_espera = []

# # -- MODELOS DE DADOS --
# # Aqui vai definir o que o Python espera receber quando um cliente for cadastrado
# class Cliente(BaseModel):
#     id: int
#     nome: str
#     telefone: str
#     estilo_tatuagem: str

#     # -- ROTAS DA API (ENDPOINTS) --

#     #1. Rota de boas-vindas
#     @app.get("/")
#     def home():
#         return{"mensagem": "Bem-vindo à API do Estúdio de Tatuagem!"}

#     #2. Rota para cadastrar o cliente.
#     @app.post("/clientes/", response_model=Cliente)
#     def cadastrar_cliente(cliente: Cliente):
#         #Verifica se o ID já existe
#         for c in banco_clientes:
#             if c.id == cliente.id:
#                 raise HTTPException(status_code=400, detail="ID de cliente já cadastrado.")

#             banco_clientes.append(cliente)
#             return cliente

#     #3. Rota para listar todos os clientes cadastrados.
#     @app.get("/clientes/", response_model=List[Cliente])
#     def listar_clientes():
#         return banco_clientes

#     #4. Rota para adicionar um cliente na FILA DE ESPERA (por ordem de chegada).
#     @app.post("/fila/{cliente_id}")
#     def entrar_na_fila(cliente_id: int):
#         #Verifica se o cliente existo no banco
#         cliente_encontrado = None
#         for c in banco_clientes:
#             if c.id == cliente_id:
#                 cliente_encontrado = c
#                 break

#             if not cliente_encontrado:
#                 raise HTTPException(status_code=404, detail="Cliente não encontrado. Cadastre-o primeiro.")

#             # Evita duplicados na fila
#             if cliente_encontrado in fila_espera:
#                 return {"mensagem": f"{cliente_encontrado.nome} já está na fila."}

#             fila_espera.append(cliente_encontrado)
#             return {"mensagem": f"{cliente_encontrado.nome} foi adicionado à fila de espera!", "Posição": len(fila_espera)}

#         #5. Rota para ver a fila de espera atual.
#         @app.get("/fila/")
#         def ver_fila():
#             return {"fila_atual":[c.nome for c in fila_espera]}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Estúdio de Tatuagem - Agendamento e Fila")

# --- BANCO DE DADOS EM MEMÓRIA (Temporário para testes) ---
# Como estamos começando, usaremos listas comuns para salvar os dados enquanto a API roda.
banco_clientes = []
fila_espera = []

# --- MODELOS DE DADOS ---
# Define o que o Python espera receber quando um cliente for cadastrado
class Cliente(BaseModel):
    id: int
    nome: str
    telefone: str
    estilo_tatuagem: str

# --- ROTAS DA API (ENDPOINTS) ---

# 1. Rota de boas-vindas
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API do Estúdio de Tatuagem!"}

# 2. Rota para cadastrar um cliente
@app.post("/clientes/", response_model=Cliente)
def cadastrar_cliente(cliente: Cliente):
    # Verifica se o ID já existe
    for c in banco_clientes:
        if c.id == cliente.id:
            raise HTTPException(status_code=400, detail="ID de cliente já cadastrado.")
    
    banco_clientes.append(cliente)
    return cliente

# 3. Rota para listar todos os clientes cadastrados
@app.get("/clientes/", response_model=List[Cliente])
def listar_clientes():
    return banco_clientes

# 4. Rota para adicionar um cliente na FILA DE ESPA (Ordem de chegada)
@app.post("/fila/{cliente_id}")
def entrar_na_fila(cliente_id: int):
    # Verifica se o cliente existe no nosso banco
    cliente_encontrado = None
    for c in banco_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
            
    if not cliente_encontrado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado. Cadastre-o primeiro.")
    
    # Evita duplicados na fila
    if cliente_encontrado in fila_espera:
        return {"mensagem": f"{cliente_encontrado.nome} já está na fila."}
        
    fila_espera.append(cliente_encontrado)
    return {"mensagem": f"{cliente_encontrado.nome} foi adicionado à fila de espera!", "posicao": len(fila_espera)}

# 5. Rota para ver a fila de espera atual
@app.get("/fila/")
def ver_fila():
    return {"fila_atual": [c.nome for c in fila_espera]}
