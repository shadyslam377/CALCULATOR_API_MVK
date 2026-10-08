# Calculator API

Простой API-калькулятор на FastAPIшке, упакованный в Докер

## Структура проекта

```
CALCULATOR_API_MVK/
├── app/
│   ├── __init__.py
│   ├── main.py          # код приложения
│   └── test_main.py     # тесты
├── scripts/
│   └── bump_version.sh  # автообновление версии (CI/CD)
├── .github/
│   └── workflows/
│       └── ci.yml       # пайплайн CI/CD + security-сканеры
├── .gitignore
├── .dockerignore
├── VERSION              # базовый semver
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── SECURITY_REPORT.md   # отчёт по инструментам безопасности
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

## версионирование

базовая версия хранится в файле `VERSION` (semver: `MAJOR.MINOR.PATCH`).

версия обновляется автоматически в пайплайне скриптом `scripts/bump_version.sh`:

- по умолчанию инкрементится **патч** (`0.1.0` → `0.1.1`);
- `[minor]` в сообщении коммита → инкремент минора (`0.1.1` → `0.2.0`);
- `[major]` в сообщении коммита → инкремент мажора (`0.2.0` → `1.0.0`).

итоговый тег версии для сборки: `<semver>-build.<GITHUB_RUN_NUMBER>` — уникален для каждой сборки.

версия попадает в приложение через `--build-arg APP_VERSION=...` и отдаётся эндпоинтом `GET /version`.

## CI/CD пайплайн

пайплайн описан в `.github/workflows/ci.yml` и запускается на каждый push в `main` и на pull request.

пайплайн состоит из job'ов:

| Job           | Что делает                                                       |
|---------------|------------------------------------------------------------------|
| `test`        | запуск `pytest`                                                  |
| `version`     | расчёт новой версии через `scripts/bump_version.sh`               |
| `build`       | сборка и публикация Docker-образа в `ghcr.io`                     |
| `semgrep`     | SAST-анализ кода (Semgrep)                                        |
| `trivy_fs`    | SCA + secrets + misconfig в репозитории (Trivy)                   |
| `trivy_image` | скан собранного образа (Trivy)                                    |
| `gitleaks`    | поиск секретов и ключей в коде                                    |
| `hadolint`    | линтер Dockerfile                                                 |

### как обновляется версия при пуше

1. пайплайн читает `VERSION`;
2. анализирует сообщение последнего коммита;
3. формирует новую версию и уникальный тег сборки;
4. собирает образ с этим тегом и публикует в `ghcr.io`.

## инструменты безопасности в пайплайне

на каждый push запускаются:

| Инструмент    | Тип                       | Что проверяет                                          |
|---------------|---------------------------|--------------------------------------------------------|
| Semgrep       | SAST                      | небезопасные паттерны в Python/FastAPI, OWASP Top 10   |
| Trivy (fs)    | SCA / secrets / misconfig | уязвимости в зависимостях, секреты, слабые конфиги     |
| Trivy (image) | scan образа               | уязвимости в базовом образе и слоях контейнера         |
| Gitleaks      | secrets                   | токены, ключи и пароли в коде репозитория              |
| Hadolint      | Dockerfile lint           | best practices для Dockerfile                          |

## где смотреть отчёты безопасности

1. GitHub → **Actions** → выбрать workflow run.
2. Скачать артефакты job'ов (`semgrep-reports`, `trivy-fs-report`, `trivy-image-report`, `gitleaks-report`, `hadolint-report`).
3. Для SARIF-отчётов — GitHub → **Security → Code scanning alerts**.

## реестр образов

образ публикуется в GitHub Container Registry:

```
ghcr.io/<user>/calculator_api_mvk:<APP_VERSION>
ghcr.io/<user>/calculator_api_mvk:latest
```

теги видны в GitHub → **Packages** (в профиле пользователя или организации).

## отчёт по безопасности

разбор находок инструментов, слабых мест калькулятора и рекомендаций — в [SECURITY_REPORT.md](SECURITY_REPORT.md).