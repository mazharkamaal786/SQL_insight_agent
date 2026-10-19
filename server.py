import os
import re
import pymysql
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("mysql-insight-agent")

FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|create|grant|replace)\b",
    re.I,
)


def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@mcp.tool()
def get_schema() -> str:
    """Show all tables and columns in the database. Call this first before writing any query."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = DATABASE()
                ORDER BY table_name, ordinal_position
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    out, current = [], None
    for table, col, dtype in rows:
        if table != current:
            out.append(f"\nTable: {table}")
            current = table
        out.append(f"  - {col} ({dtype})")
    return "\n".join(out)


@mcp.tool()
def run_sql_query(query: str) -> str:
    """Run a single read-only SELECT query on the MySQL database and return the rows."""
    q = query.strip().rstrip(";")
    if not q.lower().startswith("select") or FORBIDDEN.search(q) or ";" in q:
        return "Error: only a single SELECT query is allowed."
    if not re.search(r"\blimit\b", q, re.I):
        q += " LIMIT 100"

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(q)
            cols = [c[0] for c in cur.description]
            rows = cur.fetchall()
    except Exception as e:
        return f"SQL error: {e}"
    finally:
        conn.close()

    lines = [" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows]
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
    