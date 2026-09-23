"""
API-калькулятор на FastAPI.

Эндпоинты:
    GET  /health           - проверка живости сервиса (для Docker healthcheck)
    GET  /version          - текущая версия приложения (для CI/CD пайплайна)
    POST /add               {"a": 1, "b": 2}      -> {"result": 3}
    POST /subtract           {"a": 5, "b": 2}      -> {"result": 3}
    POST /multiply           {"a": 4, "b": 2}      -> {"result": 8}
    POST /divide              {"a": 10, "b": 2}     -> {"result": 5}
    POST /power               {"a": 2, "b": 10}     -> {"result": 1024}
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

app = FastAPI(
    title="Calculator API",
    description="Простой API-калькулятор для учебного DevOps-пайплайна",
    version=APP_VERSION,
)


class OperationRequest(BaseModel):
    a: float = Field(..., description="Первый операнд")
    b: float = Field(..., description="Второй операнд")


class OperationResponse(BaseModel):
    result: float


@app.get("/health", tags=["service"])
def health() -> dict:
    """Проверка живости сервиса."""
    return {"status": "ok"}


@app.get("/version", tags=["service"])
def version() -> dict:
    """Текущая версия приложения (обновляется пайплайном при каждом пуше)."""
    return {"version": APP_VERSION}


@app.post("/add", response_model=OperationResponse, tags=["calculator"])
def add(payload: OperationRequest) -> OperationResponse:
    return OperationResponse(result=payload.a + payload.b)


@app.post("/subtract", response_model=OperationResponse, tags=["calculator"])
def subtract(payload: OperationRequest) -> OperationResponse:
    return OperationResponse(result=payload.a - payload.b)


@app.post("/multiply", response_model=OperationResponse, tags=["calculator"])
def multiply(payload: OperationRequest) -> OperationResponse:
    return OperationResponse(result=payload.a * payload.b)


@app.post("/divide", response_model=OperationResponse, tags=["calculator"])
def divide(payload: OperationRequest) -> OperationResponse:
    if payload.b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль запрещено")
    return OperationResponse(result=payload.a / payload.b)


@app.post("/power", response_model=OperationResponse, tags=["calculator"])
def power(payload: OperationRequest) -> OperationResponse:
    try:
        result = payload.a ** payload.b
    except OverflowError:
        raise HTTPException(status_code=400, detail="Результат слишком большой")
    return OperationResponse(result=result)
