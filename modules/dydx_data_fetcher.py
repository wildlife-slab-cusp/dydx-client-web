# modules/dydx_data_fetcher.py - updated 2025-08-13

import json, copy

import modules.dydx_data_fetchers as dydx
from modules.type_caster import cast_type

def dydx_fetch_data(address, ticker="BTC-USD", subaccount_number=0):
    sub_num = subaccount_number
    try:
        block_height = dydx.fetch_block_height()
        market = dydx.fetch_market(ticker)
        account = dydx.fetch_account(address)
        filled_order = dydx.fetch_filled_order(address, sub_num)
        open_orders = dydx.fetch_open_orders(address, sub_num)

        market = market["markets"][ticker]
        subaccount = account["subaccounts"].pop(0)
        subaccount.pop("assetPositions")
        position = subaccount["openPerpetualPositions"].pop(ticker)
        subaccount.pop("openPerpetualPositions")
        filled_order = filled_order[0]

        block_height = cast_type(block_height, "block_height")
        market = cast_type(market, "market")
        subaccount = cast_type(subaccount, "subaccount")
        position = cast_type(position, "position")
        filled_order = cast_type(filled_order, "filled_order")
        open_orders = cast_type(open_orders, "open_orders")

        open_orders.sort(key=lambda x: x["price"], reverse=True)

        #print(f"Block Height:\n{json.dumps(block_height, indent=2)}")
        #print(f"Market:\n{json.dumps(market, indent=2)}")
        #print(f"Subaccount:\n{json.dumps(subaccount, indent=2)}")
        #print(f"Position:\n{json.dumps(position, indent=2)}")
        #print(f"Filled Order:\n{json.dumps(filled_order, indent=2)}")
        #print(f"Open Orders:\n{json.dumps(open_orders, indent=2)}")

        if not all(
            [
                block_height, market, subaccount,
                position, filled_order, open_orders
            ]
        ):
            print("❌ Failed to fetch all dydx data")
            return None

        dydx_data = {
            "block_height": block_height,
            "market": market,
            "subaccount": subaccount,
            "position": position,
            "filled_order": filled_order,
            "open_orders": open_orders,
        }

        timestamp = block_height["time"][14:16]
        print("✅ Fetched all dydx data with timestamp "
            f"of {timestamp} minutes past the hour")

        return dydx_data

    except Exception as e:
        print(f"❌ Unexpected error in fetch_all_dydx: {e}")
        return None
