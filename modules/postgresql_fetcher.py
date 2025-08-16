# modules/postgresql_fetcher.py - updated 2025-08-15

import os, psycopg2

DB_URL = os.environ.get("DATABASE_URL")

def fetch_config():
    """
    Fetch the configuration from the `config` table.
    """
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    address,
                    ticker,
                    highest_recorded_price,
                    buy_order_size,
                    sell_order_size,
                    buy_price_delta,
                    sell_price_delta,
                    buy_orders_max_qty,
                    sell_orders_max_qty,
                    leverage_max,
                    leverage_min,
                    accumulation_order_multiple,
                    accumulation_trigger_flag,
                    accumulation_trigger_order_leverage,
                    accumulation_trigger_on_leverage,
                    trailing_high_percentage_below_high
                FROM config
            """)
            row = cur.fetchone()
            if row is None:
                return None

            return {
                "address": row[0],
                "ticker": row[1],
                "highest_recorded_price": row[2],
                "buy_order_size": row[3],
                "sell_order_size": row[4],
                "buy_price_delta": row[5],
                "sell_price_delta": row[6],
                "buy_orders_max_qty": row[7],
                "sell_orders_max_qty": row[8],
                "leverage_max": row[9],
                "leverage_min": row[10],
                "accumulation_order_multiple": row[11],
                "accumulation_trigger_flag": row[12],
                "accumulation_trigger_order_leverage": row[13],
                "accumulation_trigger_on_leverage": row[14],
                "trailing_high_percentage_below_high": row[15],
            }
