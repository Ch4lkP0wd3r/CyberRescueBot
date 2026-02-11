import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

DB_NAME = "cyberrescue.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            incident_type TEXT,
            amount_lost TEXT,
            incident_date TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id INTEGER PRIMARY KEY,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_user(user_id, username, language='en'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO users (user_id, username, language) VALUES (?, ?, ?)', (user_id, username, language))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'en'

def save_report(user_id, incident_type, amount_lost, incident_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reports (user_id, incident_type, amount_lost, incident_date) VALUES (?, ?, ?, ?)', (user_id, incident_type, amount_lost, incident_date))
    conn.commit()
    conn.close()

def log_activity(user_id, action):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO activity_log (user_id, action) VALUES (?, ?)', (user_id, action))
    conn.commit()
    conn.close()

def subscribe_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def unsubscribe_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subscribers WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_all_subscribers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM subscribers')
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results]

def get_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    users = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM reports')
    reports = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM subscribers')
    subs = cursor.fetchone()[0]
    conn.close()
    return {"users": users, "reports": reports, "subscribers": subs}

def get_user_reports(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT incident_type, amount_lost, incident_date, timestamp FROM reports WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def init_checklist(user_id):
    steps = [
        "Call 1930 / Helpline 📞",
        "Block Bank Account/Card 💳",
        "Change Critical Passwords 🔑",
        "File Official FIR 📝",
        "Secure Devices (Scan/Reset) 📱"
    ]
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user_checklists (user_id INTEGER, step TEXT, status INTEGER DEFAULT 0, PRIMARY KEY (user_id, step))')
    for step in steps:
        cursor.execute('INSERT OR IGNORE INTO user_checklists (user_id, step) VALUES (?, ?)', (user_id, step))
    conn.commit()
    conn.close()

def get_checklist(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT step, status FROM user_checklists WHERE user_id = ?', (user_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def update_checklist_step(user_id, step, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE user_checklists SET status = ? WHERE user_id = ? AND step = ?', (status, user_id, step))
    conn.commit()
    conn.close()
