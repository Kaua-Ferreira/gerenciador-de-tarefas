# Gerenciador de Tarefas

Este é um sistema de gerenciamento de tarefas de estudo desenvolvido como projeto prático para o curso de **Análise e Desenvolvimento de Sistemas**. O sistema permite organizar matérias por categorias, monitorar o progresso das atividades e garante a segurança dos dados com autenticação de usuários.

## Funcionalidades

- **Autenticação Segura:** Sistema de login e cadastro com criptografia de senhas (BCrypt).
- **Gestão de Tarefas (CRUD):** Adicionar, listar, marcar como concluído e excluir tarefas.
- **Categorização:** Organização de atividades por etiquetas (Estudo, Urgente, Lazer).
- **Barra de Progresso:** Visualização dinâmica da porcentagem de conclusão das tarefas.
- **Persistência de Dados:** Banco de dados local para manter as informações salvas.
- **Design Responsivo:** Interface moderna (Dark Mode) acessível via notebook ou celular na rede local.

## Tecnologias Utilizadas

- **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript (Fetch API).
- **Backend:** Python 3, FastAPI (Framework de alta performance).
- **Servidor:** Uvicorn.
- **Banco de Dados:** SQLite3.
- **Criptografia:** Bcrypt para hashing de senhas.

## Como rodar o projeto

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd gerenciador-de-estudos
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install fastapi uvicorn bcrypt
   ```

4. **Inicie o servidor:**
   ```bash
   python3 -m uvicorn api.main:app --reload --host 0.0.0.0
   ```

5. **Acesse no navegador:**
   Abra o arquivo `index.html` (recomenda-se o uso da extensão Live Server no VS Code).

---
Desenvolvido por Kauã Ferreira - Estudante de ADS.
