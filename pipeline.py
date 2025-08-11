# pipeline.py - updated 2025-08-11

import os, json, time
from datetime import datetime, timezone
from modules.address_store import get_address
from modules.dydx_data_fetcher import dydx_fetch_data
from modules.plan_builder import (
    build_order_plan, select_plan_cfg, extract_plan_values
)
from modules.action_builder import build_order_actions

def main():
    while True:
        if os.path.exists("output/paused.flag"):
            time.sleep(60)
            continue
        db_url = os.environ.get("DATABASE_URL")
        address = get_address(db_url)
        if not address:
            print("No address found.")
            time.sleep(60)
            continue
        dydx_data = dydx_fetch_data(address)
        if not dydx_data:
            print("Failed to fetch dydx data")
            time.sleep(60)
            continue

        market = dydx_data["market"]
        subaccount = dydx_data["subaccount"]
        position = dydx_data["position"]
        filled_order = dydx_data["filled_order"]
        open_orders = dydx_data["open_orders"]

        try:
            now = datetime.now(timezone.utc)
            timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
            plan_values = extract_plan_values(
                subaccount, filled_order, position
            )
            plan_cfg = select_plan_cfg()
            buy_plan = build_order_plan(plan_values, plan_cfg, "buy")
            sell_plan = build_order_plan(plan_values, plan_cfg, "sell")
            actions = build_order_actions(
                open_orders, sell_plan + buy_plan
            )
            out = {
                "timestamp": timestamp,
                "market": market,
                "subaccount": subaccount,
                "position": position,
                "filled_order": filled_order,
                "open_orders": open_orders,
                "order_plan": sell_plan + buy_plan,
                "order_actions": actions
            }
            os.makedirs("output", exist_ok=True)
            with open("output/data.json", "w") as f:
                json.dump(out, f, indent=2)
            print(f"Updated at {timestamp}")
        except Exception as e:
            print("Error in pipeline:", e)
        time.sleep(60)

if __name__ == "__main__":
    main()
