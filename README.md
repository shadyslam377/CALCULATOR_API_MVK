# Calculator API

Простой API-калькулятор на FastAPIшке, упакованный в Докер

## Структура проекта

```
CALCULATOR_API_MVK/
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

## запуск локально (без докера)

```bash
python -m venv venv
source venv/bin/activate        # винда: venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

открыть документацию: http://localhost:8000/docs

## Запуск тестов

```bash
python -m pytest app/test_main.py -v
```

## сборка и запуск в докере

```bash
# сборка образа (можно передать версию через build-arg)
docker build -t calculator_api_mvk:0.1.0 --build-arg APP_VERSION=0.1.0 .

# запуск контейнера
docker run -d -p 8000:8000 --name calculator_api_mvk calculator_api_mvk:0.1.0

# проверка
curl http://localhost:8000/health
curl http://localhost:8000/version

curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"a": 2, "b": 3}'
```

ожидаемый ответ: `{"result": 5.0}`

документация Swagger будет доступна на http://localhost:8000/docs

## остановка контейнера

```bash
docker stop calculator_api_mvk
docker rm calculator_api_mvk
```

## доступные эндпоинты

| Метод | Путь        | Описание                    |
|-------|-------------|------------------------------|
| GET   | /health     | Проверка живости сервиса     |
| GET   | /version    | Текущая версия приложения    |
| POST  | /add        | Сложение (a + b)             |
| POST  | /subtract   | Вычитание (a - b)            |
| POST  | /multiply   | Умножение (a * b)            |
| POST  | /divide     | Деление (a / b)              |
| POST  | /power      | Возведение в степень (a^b)   |

тело запроса для операций: `{"a": <число>, "b": <число>}`
