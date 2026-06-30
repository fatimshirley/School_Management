import sqlite3

DB_NAME = "school.db"

def get_connection():
    conn = sqlite3.connect("school.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

