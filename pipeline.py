# pipeline.py - updated 2025-08-13

import os, json, time
from datetime import datetime, timezone, timedelta
from modules.address_store import get_address
from modules.dydx_data_fetcher import dydx_fetch_data
from modules.plan_builder import build_order_plan
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

        block_height = dydx_data["block_height"]
        market = dydx_data["market"]
        subaccount = dydx_data["subaccount"]
        position = dydx_data["position"]
        filled_order = dydx_data["filled_order"]
        open_orders = dydx_data["open_orders"]

        try:
            order_plan = build_order_plan(
                subaccount, filled_order, position
            )
            actions = build_order_actions(open_orders, order_plan)
            out = {
                "block_height": block_height,
                "market": market,
                "subaccount": subaccount,
                "position": position,
                "filled_order": filled_order,
                "open_orders": open_orders,
                "order_plan": order_plan,
                "order_actions": actions
            }
            os.makedirs("output", exist_ok=True)
            with open("output/data.json", "w") as f:
                json.dump(out, f, indent=2)

        except Exception as e:
            print("Error in pipeline:", e)

        #def start_process(cmd):
        #    print(f"Starting: {' '.join(cmd)}", flush=True)
        #    return subprocess.Popen(cmd)

        #canceller = start_process(
        #    ["python", "modules/order_canceller.py"]
        #)

        time.sleep(60)

if __name__ == "__main__":
    main()
