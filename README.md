# Тестовое задание на FastAPI + React + PostgreSQL + Docker

## 🚀 Как запускать проект

### 1. Запуск через Docker
Для запуска через Docker необходимо в терминал прописать команду `docker-compose up --build`

**Проект поднимется вместе с базой данных и будет доступен по:**
- Бэкенд: http://localhost:8000
- Фронтенд: http://localhost:3000

### 2. Запуск без Docker
Для запуска без Docker необходимо в терминале выполнить следующие команды

*Для Windows:*
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

*Для Linux/Mac:*
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Далее необходимо создать бд в PostgreSQL согласно данным в .env или запустить через Docker

Теперь необходимо применить миграции с помощью команды `alembic upgrade head`

Наконец можно запускать бэк и фронт в разных терминалах с помощью следующих команд:

*Backend:*
```
cd backend
uvicorn main:app --reload
```

*Frontend:*
```
cd frontend
npm run dev
```
