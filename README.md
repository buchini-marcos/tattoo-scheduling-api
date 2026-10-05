# 🎨 Tattoo Scheduling & Queue API
Uma API REST moderna desenvolvida em Python com **FastAPI** para gerenciar o fluxo de atendimento, agendamentos e filas de espera em um estúdio de tatuagem. Ideal para otimizar o dia a dia de estúdios e gerenciar eventos como *Flash Days*.

## 🚀 Funcionalidades Atuais

*   **Cadastro de Clientes:** Registro com ID único, nome, telefone e estilo de tatuagem preferido.
*   **Fila de Espera por Ordem de Chegada:** Entrada e visualização da fila para atendimentos dinâmicos.
*   **Painel do Tatuador:** Sistema para chamar e remover o próximo cliente da fila automaticamente.
*   **Agendamentos com Data e Hora:** Marcação de sessões individuais por tatuador, contando com validação inteligente contra conflitos de horários (bloqueia o agendamento se o profissional já estiver ocupado) e inexistência do nome do profissional no "estúdio".

## 🛠️ Tecnologias Utilizadas

*   **Python 3** - Linguagem base do projeto.
*   **FastAPI** - Framework web moderno, veloz e de alto desempenho.
*   **Uvicorn** - Servidor ASGI para rodar a aplicação localmente.
*   **SQLite** - Validação e estruturação de dados.

## 📦 Como Rodar o Projeto Localmente

Siga os passos abaixo no terminal para clonar e executar a API na sua máquina:

# 1. Clonar o repositório
git clone https://github.com/buchini-marcos/tattoo-scheduling-api.git

# 2. Entrar na pasta do projeto
cd tattoo-scheduling-api

# 3. Criar o ambiente virtual
python -m venv venv

# 4. Ativar o ambiente virtual (Windows)
.\venv\Scripts\activate

# 5. Instalar as dependências necessárias
pip install -r requirements.txt

# 6. Iniciar o servidor de desenvolvimento
uvicorn "main:app" --reload


Após iniciar o servidor, abra o seu navegador e acesse a documentação interativa em:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---
🛠️ **Este projeto está sendo desenvolvido como parte dos meus estudos para aprender Engenharia de Software e Back-end com Python e consolidação de dados com SQL.**