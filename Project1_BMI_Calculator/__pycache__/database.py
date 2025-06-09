import sqlite3
from datetime import datetime

DB_PATH = "bmi_data.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            height REAL,
            weight REAL,
            bmi REAL,
            category TEXT,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    return conn

def register_user(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def save_bmi_record(user_id, height, weight, bmi, category):
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO bmi_records (user_id, height, weight, bmi, category, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, height, weight, bmi, category, date))
    conn.commit()
    conn.close()

def get_bmi_history(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT date, height, weight, bmi, category FROM bmi_records WHERE user_id = ? ORDER BY date", (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records


