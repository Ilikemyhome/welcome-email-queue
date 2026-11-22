import sqlite3

DB_NAME = "jobs.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            email TEXT,
            name TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_job(job_id, email, name):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO jobs
        VALUES (?, ?, ?, ?)
        """,
        (job_id, email, name, "queued")
    )

    conn.commit()
    conn.close()


def get_job(job_id):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        """
        SELECT id, email, name, status
        FROM jobs
        WHERE id = ?
        """,
        (job_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return row


def update_status(job_id, status):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        UPDATE jobs
        SET status = ?
        WHERE id = ?
        """,
        (status, job_id)
    )

    conn.commit()
    conn.close()