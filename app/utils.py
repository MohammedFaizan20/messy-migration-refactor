from flask import g
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('users.db')
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def serialize_user(row):
    return {
        'id': row[0],
        'name': row[1],
        'email': row[2],
    }
