# Базовый образ - минимальный, чтобы уменьшить поверхность атаки
FROM python:3.12-slim

# Метаданные, которые пайплайн сможет обновлять при каждом пуше
ARG APP_VERSION=0.1.0
ENV APP_VERSION=${APP_VERSION}
LABEL org.opencontainers.image.title="calculator-api" \
      org.opencontainers.image.version="${APP_VERSION}"

WORKDIR /app

# Сначала зависимости - для кэширования слоёв Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем код приложения
COPY app ./app

# Создаём непривилегированного пользователя и переключаемся на него
RUN addgroup --system app && adduser --system --ingroup app app
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
