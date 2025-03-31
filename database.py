import sqlite3

def create_tables():
    conn = sqlite3.connect("database.db")  # ✅ Ensure consistency
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT)''')

    # Jobs Table (Recreate if needed)
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        recruiter TEXT)''')

    # Resumes Table
     # ✅ Updated: Resumes Table (Only store one resume per user)
    cursor.execute('''CREATE TABLE IF NOT EXISTS resumes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        resume_file BLOB)''')  # Store resumes as PDF BLOBs

    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        job_id INTEGER,
                        resume_file BLOB,
                        FOREIGN KEY (username) REFERENCES users(username),
                        FOREIGN KEY (job_id) REFERENCES jobs(id))''')
    conn.commit()
    conn.close()

def insert_user(username, password, role):
    conn = sqlite3.connect("database.db")  # ✅ Fix
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  
    finally:
        conn.close()

def check_user(username, password):
    conn = sqlite3.connect("database.db")  # ✅ Fix
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None  

def insert_job(title, description, recruiter):
    conn = sqlite3.connect("database.db")  # ✅ Fix
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, description, recruiter) VALUES (?, ?, ?)", (title, description, recruiter))
    conn.commit()
    conn.close()

def get_jobs():
    conn = sqlite3.connect("database.db")  # ✅ Fix
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_jobs_by_recruiter(recruiter_username):
    """Fetches jobs posted by a specific recruiter."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, description FROM jobs WHERE recruiter = ?", (recruiter_username,))
    jobs = cursor.fetchall()
    
    conn.close()
    return jobs
    
def insert_resume(username, name, email, phone, skills, experience, education, resume_file):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO resumes (username, name, email, phone, skills, experience, education, resume_file) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (username, name, email, phone, skills, experience, education, resume_file.read()))  # Read file as binary

    conn.commit()
    conn.close()


def get_applicants(job_id):
    """Fetches applicants for a given job ID with their username and resume file."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT a.username, a.resume_file
        FROM applications a
        WHERE a.job_id = ?
    ''', (job_id,))

    applicants = cursor.fetchall()
    conn.close()
    return applicants
    
def get_resume(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT resume_file FROM resumes WHERE username=?", (username,))
    resume = cursor.fetchone()
    conn.close()
    return resume[0] if resume else None  # Return resume file if exists


create_tables()
