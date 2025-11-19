import sqlite3
import time
from typing import Optional

DB_NAME = "game.db"

def init_db():
    """Создає таблицю транзакцій, якщо не існує."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Таблиця транзакцій: id, value, type, timestamp
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL NOT NULL,
                type TEXT NOT NULL,
                created_at REAL
            )
        ''')
        conn.commit()

def add_transaction(value: float, trans_type: str):
    """Добавляє запис о транзакції (ставка, виграш або ініт)."""
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (value, type, created_at) VALUES (?, ?, ?)",
            (value, trans_type, time.time())
        )
        conn.commit()

def get_balance() -> float:
    """повертає суму всіх транзакцій."""
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(value) FROM transactions")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0

def has_transactions() -> bool:
    """Перевіряє чи є транзакция"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM transactions")
        return cursor.fetchone()[0] > 0

init_db()