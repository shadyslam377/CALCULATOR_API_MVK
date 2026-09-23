# Calculator API

Простой API-калькулятор на FastAPI, упакованный в Docker.

## Структура проекта

```
calculator-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # код приложения
│   └── test_main.py     # тесты
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

## Запуск локально (без Docker)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Открыть документацию: http://localhost:8000/docs

## Запуск тестов

```bash
python -m pytest app/test_main.py -v
```

## Сборка и запуск в Docker

```bash
# Сборка образа (можно передать версию через build-arg)
docker build -t calculator-api:0.1.0 --build-arg APP_VERSION=0.1.0 .

# Запуск контейнера
docker run -d -p 8000:8000 --name calculator-api calculator-api:0.1.0

# Проверка
curl http://localhost:8000/health
curl http://localhost:8000/version

curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"a": 2, "b": 3}'
```

Ожидаемый ответ: `{"result": 5.0}`

Документация Swagger будет доступна на http://localhost:8000/docs

## Остановка контейнера

```bash
docker stop calculator-api
docker rm calculator-api
```

## Эндпоинты

| Метод | Путь        | Описание                    |
|-------|-------------|------------------------------|
| GET   | /health     | Проверка живости сервиса     |
| GET   | /version    | Текущая версия приложения    |
| POST  | /add        | Сложение (a + b)             |
| POST  | /subtract   | Вычитание (a - b)            |
| POST  | /multiply   | Умножение (a * b)            |
| POST  | /divide     | Деление (a / b)              |
| POST  | /power      | Возведение в степень (a^b)   |

Тело запроса для операций: `{"a": <число>, "b": <число>}`
