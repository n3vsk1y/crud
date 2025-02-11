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

Далее необходимо создать бд в PostgreSQL согласно данным в .env или запустить через Docker: `psql -U DB_USER -d postgres -c "CREATE DATABASE DB_NAME;"` 

Теперь необходимо применить миграции с помощью команды `alembic upgrade head`

А также добавить данные в бд: `python seed.py`

Наконец можно запустить сервер и клиент в разных терминалах с помощью следующих команд:

*Backend:*
```
cd backend
uvicorn main:app --reload
```

*Frontend:*
```
cd frontend
npm install
npm run dev
```

- Бэкенд: http://localhost:8000
- Фронтенд: http://localhost:5173


## 🧪 Как тестировать проект

### Тестирование через Swagger в FastAPI

После запуска проекта необходимо перейти на http://localhost:8000/docs и теперь можно тестировать различные роуты

Тестовые данные для вебхука можно найти в папке бэкэнда в файле data_for_webhook_test, только надо будет поправить id юзера на существующий

Для тестирования роутов получения данных и роутов админа, необходимо войти:

1. Для начала необходимо получить access токен при помощи роута login
2. Затем необходимо справа сверху нажать кнопку Authorize
3. Вставить токен в поле Value и нажать Authorize
4. Теперь можно тестировать роуты, которым нужны данные о юзере

## КРЕДЫ ДЛЯ ТЕСТА:

### user:
email: user@example.com
password: user

2 счета - 500 и 100
3 транзакции

### admin:
email: admin@example.com
password: admin

1 счет - 5000
1 транзакция

# P.S. env файлы и данные в docker-compode.yml добалены в репозиторий специально для работы докера






