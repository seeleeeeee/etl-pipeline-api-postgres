import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = "pipeline_db"
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASS")
DB_HOST = "localhost"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_posts(posts):
    conn = get_connection()
    cur = conn.cursor()
    
    # очистка
    cur.execute("DELETE FROM raw_posts")
    
    data = [(p['id'], p['userId'], p['title'], p['body']) for p in posts]
    cur.executemany(
        "INSERT INTO raw_posts (id, user_id, title, body) VALUES (%s, %s, %s, %s);",
        data
    )
    conn.commit()
    print(f"Сохранено {len(data)} записей в базу")
    
    cur.close()
    conn.close()