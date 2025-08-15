# modules/postgresql_fetcher.py - updated 2025-08-15

import psycopg2

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
                FROM comfig
            """)
            (
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
            ) = cur.fetchone()
