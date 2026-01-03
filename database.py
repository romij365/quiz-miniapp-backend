cat > backend/database.py << EOL
import sqlite3
conn = sqlite3.connect("quiz.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(\"""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0,
    answered INTEGER DEFAULT 0,
    last_date TEXT,
    current_q INTEGER,
    last_bonus TEXT
)\""")

cursor.execute(\"""CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    answer TEXT
)\""")

cursor.execute(\"""CREATE TABLE IF NOT EXISTS withdraws(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    method TEXT,
    number TEXT,
    status TEXT
)\"""")
conn.commit()
EOL
