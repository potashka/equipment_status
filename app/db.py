# db.py
"""
Этот модуль управляет подключением к базе данных и управлением сессиями.
Функции:
    get_db: Предоставляет сессию базы данных для использования в зависимостях.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/monitoring"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Предоставляет сессию базы данных для использования в зависимостях.
    Возвращает:
        Session: Объект сессии SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
