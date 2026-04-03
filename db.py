import sqlite3
import datetime
from pathlib import Path

DB_FILE = 'bot_database.db'

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            text TEXT NOT NULL,
            lesson_date TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_message(chat_id: int, user_id: int, username: str, text: str, lesson_date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (chat_id, user_id, username, text, lesson_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (chat_id, user_id, username, text, lesson_date))
    conn.commit()
    conn.close()

def get_messages(chat_id: int, lesson_date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, text, timestamp FROM messages
        WHERE chat_id = ? AND lesson_date = ?
        ORDER BY timestamp ASC
    ''', (chat_id, lesson_date))
    rows = cursor.fetchall()
    conn.close()
    return rows
