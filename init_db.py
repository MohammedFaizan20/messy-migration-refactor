import sqlite3
import bcrypt

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        password TEXT NOT NULL
)
''')

cursor.execute("DELETE FROM users")  # Optional reset

cursor.execute("INSERT INTO users (username, email, full_name, password) VALUES (?, ?, ?, ?)",
               ('john123', 'john@example.com', 'John Doe', hash_password('password123')))

cursor.execute("INSERT INTO users (username, email, full_name, password) VALUES (?, ?, ?, ?)",
               ('jane_smith', 'jane@example.com', 'Jane Smith', hash_password('secret456')))

cursor.execute("INSERT INTO users (username, email, full_name, password) VALUES (?, ?, ?, ?)",
               ('bobbyJ', 'bob@example.com', 'Bob Johnson', hash_password('qwerty789')))


conn.commit()
conn.close()

print("Database initialized with bcrypt-hashed passwords.")
