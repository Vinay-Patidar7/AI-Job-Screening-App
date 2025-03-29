import sqlite3

def add_job(title, description, posted_by):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, description, posted_by) VALUES (?, ?, ?)", (title, description, posted_by))
    conn.commit()
    conn.close()

def get_jobs():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs
