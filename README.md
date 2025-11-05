# Secure User API

## Problema (dor)
Em vários sistemas que acompanhei, não havia controle de tentativas de login e faltavam logs claros — resultando em tentativas repetidas de accesso indevido e dificuldade para auditar incidentes. A ideia surgiu quando um conhecido teve sua conta alvo de tentativas de força bruta por dias; não havia trilha de auditoria.

## O que este projeto resolve
- Registro seguro de usuários (senhas com hash)
- Autenticação via JWT
- Logging de tentativas de autenticação
- Bloqueio temporário de IP após N tentativas falhas

## Tecnologias usadas
- Python, FastAPI, Uvicorn
- SQLAlchemy + SQLite
- Passlib (bcrypt)
- PyJWT
- pytest para testes

## Como rodar localmente
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `uvicorn app.main:app --reload`
4. Acesse `http://127.0.0.1:8000/docs`

## Endpoints
- `POST /register` — cria usuário: `{ "username": "...", "email": "...", "password": "..." }`
- `POST /login` — login: `{ "username": "...", "password": "..." }` -> retorna token JWT

## Observações de segurança / próximos passos
- Mover rate-limiter para Redis para persistência e escalabilidade.
- Implementar refresh tokens, blacklisting de tokens, e revalidação.
- Implementar verificação de e-mail, 2FA, e CSRF para rotas sensíveis.
