"""
Checkpoint management for incremental loads.
"""

def get_last_checkpoint(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT last_run_date
        FROM pipeline_checkpoint
        ORDER BY id DESC
        LIMIT 1;
    """)
    result = cursor.fetchone()
    return result[0] if result else None


def update_checkpoint(conn, run_date):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pipeline_checkpoint (last_run_date)
        VALUES (%s);
    """, (run_date,))
