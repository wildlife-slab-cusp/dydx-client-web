# modules/address_store.py - updated 2025-08-08

import psycopg2

def _connect(db_url):
    return psycopg2.connect(db_url)

def get_address(db_url):
    """
    Fetch the one and only address from the `account` table.
    Returns None if the table is empty.
    """
    conn = _connect(db_url)
    with conn.cursor() as cur:
        cur.execute("SELECT address FROM account;")
        row = cur.fetchone()
    conn.close()
    return row[0] if row else None
