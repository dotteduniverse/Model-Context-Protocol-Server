import psycopg2
from src.database import get_connection

def log_context_access(tenant_id: str, endpoint: str, user_id: str = None):
    """Log a context request."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audit_logs (tenant_id, endpoint, user_id) VALUES (%s, %s, %s)",
        (tenant_id, endpoint, user_id)
    )
    conn.commit()
    cur.close()
    conn.close()