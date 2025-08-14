# modules/order_canceller.py

import json
import os
from pathlib import Path
from v4_proto.dydxprotocol.clob.order_pb2 import Order
from dydx_v4_client import Client, MAX_CLIENT_ID, OrderFlags

# Load mnemonic from env var
MNEMONIC = os.getenv("DYDX_MNEMONIC")

# Network config for mainnet
NETWORK = "mainnet"
GRPC_ENDPOINT = "https://dydx-mainnet.grpc.io"

# Path to your pipeline output file
OUTPUT_FILE = Path(__file__).parent.parent / "output" / "data.json"


def cancel_orders_from_file():
    """
    Reads the pipeline output file,
    extracts wallet address + order IDs,
    cancels all long-term orders,
    and exits without errors if nothing to cancel.
    """
    if not MNEMONIC:
        print("DYDX_MNEMONIC not set — cannot cancel orders.")
        return

    if not OUTPUT_FILE.exists():
        print(f"No output file found: {OUTPUT_FILE}")
        return

    # Load JSON
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Output file is not valid JSON.")
            return

    wallet_address = data["subaccount"]["address"]
    if not wallet_address:
        print("No wallet address found — skipping cancellation.")
        return

    # Extract only cancel actions
    orders_to_cancel = [
        action for action in data["order_actions"]
        if action["type"] == "cancel"
    ]

    if not orders_to_cancel:
        print("No orders to cancel — done.")
        return

    # Initialize dYdX client
    client = Client(
        network=NETWORK,
        grpc_endpoint=GRPC_ENDPOINT,
        mnemonic=MNEMONIC,
        address=wallet_address,
    )

    # Build cancel requests (long-term only)
    cancel_requests = [
        Order(id=action["id"], flags=OrderFlags.LONG_TERM, client_id=MAX_CLIENT_ID)
        for action in orders_to_cancel
    ]

    print(f"Cancelling {len(cancel_requests)} orders for wallet {wallet_address}...")
    try:
        response = client.cancel_orders(cancel_requests)
        print("Cancel response:", response)
    except Exception as e:
        print(f"Error cancelling orders: {e}")


if __name__ == "__main__":
    cancel_orders_from_file()