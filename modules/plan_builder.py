# plan_builder.py - updated 2025-08-13

import os
import math
import psycopg2
import sqlite3

def build_order_plan(subaccount, filled_order, position):
    """Build combined order plan for 'buy' and 'sell' sides."""
    plan = []

    # Select configuration values from Neon Postgres plan_cfg table
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set")
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    buy_order_size,
                    sell_order_size,
                    buy_price_delta,
                    sell_price_delta,
                    buy_orders_max_qty,
                    sell_orders_max_qty,
                    leverage_max,
                    leverage_min
                FROM plan_cfg
            """)
            (
                buy_order_size,
                sell_order_size,
                buy_price_delta,
                sell_price_delta,
                buy_orders_max_qty,
                sell_orders_max_qty,
                leverage_max,
                leverage_min
            ) = cur.fetchone()

    filled_price = filled_order["price"]
    position_size = position["size"]
    net_funding = position["netFunding"]
    realized_pnl = position["realizedPnl"]
    unrealized_pnl = position["unrealizedPnl"]
    sum_open = position["sumOpen"]
    sum_close = position["sumClose"]

    # Build Buy Plan
    side = "buy"
    equity = subaccount["equity"]
    entry_price = position["entryPrice"]
    exit_price = position["exitPrice"]
    order_size = buy_order_size
    delta = buy_price_delta
    count = buy_orders_max_qty
    price = math.floor((filled_price - delta) / 1000) * 1000 + 500
    pos_size = position_size + order_size
    entry_sum = sum_open + order_size
    entry_price = (
        entry_price * sum_open + order_size * price) / entry_sum
    exit_sum = sum_close

    for i in range(count):
        if i > 0:
            price -= delta
            pos_size += order_size
            entry_sum += order_size
            entry_price = (
                entry_price * (entry_sum - order_size)
                + order_size * price
            ) / entry_sum
        unreal = (price - entry_price) * pos_size
        realized = (
            (exit_price - entry_price) * exit_sum + net_funding
        )
        buy_total = unreal + realized

        if i == 0:
            equity = (
                equity - unrealized_pnl - realized_pnl + buy_total
            )
        else:
            equity = equity - prev_buy_total + buy_total

        lev = round((pos_size * price) / equity, 2)
        pos_size = round(pos_size, 4)
        include = lev <= leverage_max
        prev_buy_total = buy_total

        plan.append({
            "side": side,
            "orderPrice": round(price, 2),
            "orderSize": order_size,
            "positionSize": round(pos_size, 4),
            "entrySum": round(entry_sum, 4),
            "entryPrice": round(entry_price, 2),
            "exitSum": round(exit_sum, 6),
            "exitPrice": round(exit_price, 2),
            "fundingPmt": net_funding,
            "realizedPnL": round(realized, 2),
            "unrealizedPnL": round(unreal, 2),
            "totalPnL": round(buy_total, 2),
            "equityLeverage": lev,
            "includeFlag": include
        })

    # Build sell Plan
    side = "sell"
    equity = subaccount["equity"]
    entry_price = position["entryPrice"]
    exit_price = position["exitPrice"]
    order_size = sell_order_size
    delta = sell_price_delta
    count = sell_orders_max_qty
    price = math.floor(
        (filled_price + delta) / 1000
    ) * 1000 + 500
    pos_size = position_size - order_size
    entry_sum = sum_open
    entry_price = entry_price
    exit_sum = sum_close + order_size
    exit_price = (
        exit_price * sum_close + order_size * price
    ) / exit_sum

    for i in range(count):
        if i > 0:
            price += delta
            pos_size -= order_size
            exit_sum += order_size
            exit_price = (
                exit_price * (exit_sum - order_size)
                + order_size * price
            ) / exit_sum
        unreal = (price - entry_price) * pos_size
        realized = (
            (exit_price - entry_price) * exit_sum + net_funding
        )
        sell_total = unreal + realized

        if i == 0:
            equity = (
                equity - unrealized_pnl - realized_pnl + sell_total
            )
        else:
            equity = equity - prev_sell_total + sell_total

        lev = round((pos_size * price) / equity, 2)
        pos_size = round(pos_size, 4)
        include = lev >= leverage_min
        prev_sell_total = sell_total

        plan.append({
            "side": side,
            "orderPrice": round(price, 2),
            "orderSize": order_size,
            "positionSize": round(pos_size, 4),
            "entrySum": round(entry_sum, 4),
            "entryPrice": round(entry_price, 2),
            "exitSum": round(exit_sum, 6),
            "exitPrice": round(exit_price, 2),
            "fundingPmt": net_funding,
            "realizedPnL": round(realized, 2),
            "unrealizedPnL": round(unreal, 2),
            "totalPnL": round(sell_total, 2),
            "equityLeverage": lev,
            "includeFlag": include
        })

    # Sort by orderPrice descending
    plan.sort(key=lambda x: x["orderPrice"], reverse=True)

    return plan
