import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM users")
conn.commit()
conn.close()

print("All users deleted from the database.")
