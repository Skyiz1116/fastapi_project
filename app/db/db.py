from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Загружаем переменные из .env файла
load_dotenv()

# Получаем URL базы данных из переменной окружения
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Проверяем, что переменная найдена
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в .env файле!")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()