# modules/dydx_data_fetchers.py - updated 2025-08-11

import requests

MARKET_URL = "https://indexer.dydx.trade/v4/perpetualMarkets"
ACCOUNT_URL = "https://indexer.dydx.trade/v4/addresses"
FILLS_URL = "https://indexer.dydx.trade/v4/fills"
ORDERS_URL = "https://indexer.dydx.trade/v4/orders"

def fetch_market(ticker="BTC-USD"):
    try:
        url = MARKET_URL
        params = {"ticker": ticker}
        headers = {"Accept": "application/json"}

        resp = requests.get(
            url, params=params, headers=headers, timeout=10
        )
        resp.raise_for_status()

        markets = resp.json()

        return markets

    except Exception as e:
        print(f"❌ Fetch market failed: {e}")
        return None

def fetch_account(address, subaccount_number=0):
    try:
        url = (
            f"{ACCOUNT_URL}/{address}/"
            f"subaccountNumber/{subaccount_number}/")
        headers = {"Accept": "application/json"}
        resp = requests.get(
            url,
            headers=headers,
            timeout=10)
        resp.raise_for_status()
        account = resp.json()
        return account
    except Exception as e:
        print(f"❌ Fetch account failed: {e}")
        return None

def fetch_filled_order(address, subaccount_number=0, limit=1):
    try:
        url = FILLS_URL
        params = {
            "address": address,
            "subaccountNumber": subaccount_number,
            "limit": limit}
        headers = {"Accept": "application/json"}
        resp = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10)
        resp.raise_for_status()
        data = resp.json()
        filled_order = data.get("fills", [])
        return filled_order
    except Exception as e:
        print(f"❌ Fetch last filled order failed: {e}")
        return None

def fetch_open_orders(address, subaccount_number=0):
    try:
        url = ORDERS_URL
        params = {
            "address": address,
            "subaccountNumber": subaccount_number,
            "status": "OPEN"}
        headers = {"Accept": "application/json"}
        resp = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        open_orders = resp.json()

        # Sort by price descending
        open_orders.sort(key=lambda x: x["price"], reverse=True)

        return open_orders
    except Exception as e:
        print(f"❌ Fetch open orders failed: {e}")
        return None

