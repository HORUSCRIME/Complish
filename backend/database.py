import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = "compliment_app.db"

def get_db():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    
    schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "compliment_schema.sql")
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
    
    conn.commit()
    conn.close()

@contextmanager
def get_db_context():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()