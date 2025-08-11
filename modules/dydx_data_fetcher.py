# modules/dydx_data_fetcher.py - updated 2025-08-11

import json, copy

import modules.dydx_data_fetchers as dydx
from modules.type_caster import cast_type

def dydx_fetch_data(address, ticker="BTC-USD", subaccount_number=0):
    sub_num = subaccount_number
    try:
        market = dydx.fetch_market(ticker)
        account = dydx.fetch_account(address)
        filled_order = dydx.fetch_filled_order(address, sub_num)
        open_orders = dydx.fetch_open_orders(address, sub_num)

        market = market["markets"][ticker]
        account["subaccount"].pop("assetPositions")
        subaccount = copy.deepcopy(account["subaccount"])
        position = subaccount["openPerpetualPositions"].pop(ticker)
        subaccount.pop("openPerpetualPositions")
        filled_order = filled_order[0]

        market = cast_type(market, "market")
        subaccount = cast_type(subaccount, "subaccount")
        position = cast_type(position, "position")
        filled_order = cast_type(filled_order, "filled_order")
        open_orders = cast_type(open_orders, "open_orders")

        #print(f"Market:\n{json.dumps(market, indent=2)}")
        #print(f"Subaccount:\n{json.dumps(subaccount, indent=2)}")
        #print(f"Position:\n{json.dumps(position, indent=2)}")
        #print(f"Filled Order:\n{json.dumps(filled_order, indent=2)}")
        #print(f"Open Orders:\n{json.dumps(open_orders, indent=2)}")

        if not all(
            [market, subaccount, position, filled_order, open_orders]
        ):
            print("❌ Failed to fetch all dydx data")
            return None

        dydx_data = {
            "market"      : market,
            "subaccount"  : subaccount,
            "position"    : position,
            "filled_order": filled_order,
            "open_orders" : open_orders,
        }

        print("✅ Fetched all dydx data")

        return dydx_data

    except Exception as e:
        print(f"❌ Unexpected error in fetch_all_dydx: {e}")
        return None
