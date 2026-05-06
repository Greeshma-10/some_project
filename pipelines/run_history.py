"""
Track pipeline execution history.
"""

def log_run(conn, status: str):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pipeline_run_history (status)
        VALUES (%s);
    """, (status,))
    conn.commit()