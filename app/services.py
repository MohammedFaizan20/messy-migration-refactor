import sqlite3
import bcrypt

DB_PATH = 'users.db'

def create_user(username, email, full_name, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, full_name, password) VALUES (?, ?, ?, ?)",
                (username, email, full_name, password)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def get_user_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, full_name FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
    if row:
        return {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'full_name': row[3]
        }
    return None

def update_user(user_id, data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            return False  # User not found

        # Optional update for username if provided
        username = data.get('username')
        email = data['email']
        full_name = data['full_name']

        if username:
            cursor.execute(
                "UPDATE users SET username = ?, email = ?, full_name = ? WHERE id = ?",
                (username, email, full_name, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET email = ?, full_name = ? WHERE id = ?",
                (email, full_name, user_id)
            )

        conn.commit()
        return True

def delete_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            return False  # User not found

        # Proceed to delete
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True

def get_all_users():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, full_name FROM users")
        rows = cursor.fetchall()
        return [
            {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'full_name': row[3]
            }
            for row in rows
        ]

def search_users_by_full_name(name_query):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, full_name FROM users WHERE full_name LIKE ?",
            ('%' + name_query + '%',)
        )
        rows = cursor.fetchall()
        return [
            {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'full_name': row[3]
            }
            for row in rows
        ]

def get_user_by_email(email):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, full_name, password FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
    if row:
        return {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'full_name': row[3],
            'password': row[4]  
        }
    return None
    
def login_user(email, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, full_name, password FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
    if row:
        user_id, username, email, full_name, hashed_pw = row
        if bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
            return {
                'id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name
            }
    return None