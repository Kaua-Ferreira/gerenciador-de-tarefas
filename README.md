# Gerenciador de Tarefas

Este é um ecossistema completo de produtividade desenvolvido para o curso de **Análise e Desenvolvimento de Sistemas**. O projeto evoluiu de uma lista simples para uma aplicação robusta com backend em Python, banco de dados persistente e uma interface focada na experiência do usuário (UX).

## Novas Funcionalidades

- **Dual Theme:** Modo claro e escuro persistente (salva sua preferência no navegador).
- **Modo Foco Integrado:** Cronômetro dinâmico por tarefa para aplicar a técnica Pomodoro.
- **Controle de Alerta:** Notificação sonora ao finalizar ciclos de foco com ajuste de volume.
- **Barra de Progresso:** Visualização em tempo real da conclusão das suas metas.
- **Design Responsivo:** Interface totalmente adaptada para uso em smartphones.
- **Segurança Avançada:** Senhas protegidas por criptografia de nível industrial (BCrypt).
- **Efeitos Visuais:** Animações interativas para celebrar a conclusão de tarefas.

## Tecnologias e Arquitetura

O projeto segue o padrão de **Separação de Preocupações**, com pastas organizadas para melhor manutenção:

- **Backend:** Python 3 + FastAPI.
- **Banco de Dados:** SQLite3 (Persistência local).
- **Criptografia:** Bcrypt.
- **Frontend:**
  - `index.html`: Estrutura semântica.
  - `css/style.css`: Estilização moderna com Variáveis CSS.
  - `js/script.js`: Lógica dinâmica e integração com API.
- **Assets:** Sons de alerta e ícones personalizados.

## Como rodar o projeto no seu notebook

1. **Ative o ambiente virtual:**
   ```bash
   source venv/bin/activate
   ```

2. **Inicie o Servidor Backend:**
   ```bash
   python3 -m uvicorn api.main:app --reload --host 0.0.0.0
   ```

3. **Inicie o Frontend:**
   Abra o `index.html` usando a extensão **Live Server** do VS Code.

## 📱 Acesso via Celular
Para usar o sistema no celular (na mesma rede Wi-Fi), acesse o IP do seu notebook seguido da porta do Live Server (ex: `http://192.168.x.x:5500`).

---
Documentação atualizada em: 30 de Abril de 2026.
Desenvolvido por **Kauã Ferreira** - Estudante de ADS.
