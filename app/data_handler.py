import sqlite3
import hashlib
from datetime import datetime
import os
# Create a data directory for DB if not exists
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)  # <-- this ensures folder exists

DB_PATH = os.path.join(DATA_DIR, 'candidates.db')  # Use absolute path

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        experience INTEGER,
        position TEXT,
        location TEXT,
        tech_stack TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS candidate_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        question TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS candidate_answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        question TEXT,
        answer TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    )
    ''')
    conn.commit()
    conn.close()

def mask_email(email):
    # Show only domain and first letter of username to mask PII
    parts = email.split("@")
    if len(parts) != 2:
        return email
    user, domain = parts
    masked_user = user[0] + "***"
    return f"{masked_user}@{domain}"

def mask_phone(phone):
    # Show only last 3 digits
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) <= 3:
        return "***"
    return "***" + digits[-3:]

def insert_candidate(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO candidates (full_name, email, phone, experience, position, location, tech_stack)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("full_name"),
        data.get("email"),
        data.get("phone"),
        data.get("experience"),
        data.get("position"),
        data.get("location"),
        data.get("tech_stack")
    ))
    candidate_id = c.lastrowid
    conn.commit()
    conn.close()
    return candidate_id

def insert_questions(candidate_id, questions):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for q in questions:
        c.execute('''
        INSERT INTO candidate_questions (candidate_id, question) VALUES (?, ?)
        ''', (candidate_id, q))
    conn.commit()
    conn.close()

def get_candidate(candidate_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM candidates WHERE id=?", (candidate_id,))
    candidate = c.fetchone()
    conn.close()
    return candidate
def insert_answer(candidate_id, question_text, answer_text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO candidate_answers (candidate_id, question, answer)
        VALUES (?, ?, ?)
    """, (candidate_id, question_text, answer_text))
    conn.commit()
    conn.close()

