from fastapi import FastAPI
from app.api import books, categories
from app.db.db import engine, Base

# Создаём таблицы в БД (если нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book API",
    description="API для управления книгами и категориями",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)

@app.get("/health")
def health_check():
    """Проверка работоспособности API"""
    return {"status": "ok", "message": "API is running"}

@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "Welcome to Book API",
        "docs": "/docs",
        "health": "/health"
    }