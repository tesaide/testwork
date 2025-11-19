import sqlite3
import time
from typing import Optional

DB_NAME = "game.db"

def init_db():
    """Creates transactions table if it does not exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Transactions table: id, value, type, timestamp
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
    """Adds a transaction record (bet, win, or init)."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (value, type, created_at) VALUES (?, ?, ?)",
            (value, trans_type, time.time())
        )
        conn.commit()

def get_balance() -> float:
    """Returns the sum of all transactions."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(value) FROM transactions")
        result = cursor.fetchone()[0]
        return result if result is not None else 0.0

def has_transactions() -> bool:
    """Checks if any transactions exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM transactions")
        return cursor.fetchone()[0] > 0

# Initialize DB on module import
init_db()