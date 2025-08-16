# modules/action_builder.py - updated 2025-08-09

from collections import Counter

def build_order_actions(open_orders, order_plans):
    """Build order actions from dydx data and generated plan."""

    # Normalize open orders
    open_orders = [
        {
            "id"   : o.get("id"),
            "side" : o["side"].upper(),
            "price": float(o["price"]),
            "size" : float(o["size"]),
        }
        for o in open_orders
    ]

    # Normalize planned orders
    order_plans = [
        {
            "side" : p["side"].upper(),
            "price": float(p["orderPrice"]),
            "size" : float(p["orderSize"]),
        }
        for p in order_plans
        if p.get("includeFlag")
    ]

    return order_actions(open_orders, order_plans)


def order_actions(open_orders, order_plans):
    actions = []

    # Count identical orders
    open_counter = Counter(
        (o["side"], o["price"], o["size"])
        for o in open_orders
    )
    plan_counter = Counter(
        (p["side"], p["price"], p["size"])
        for p in order_plans
    )

    # Cancel extra open orders
    for order_key, open_count in open_counter.items():
        plan_count = plan_counter.get(order_key, 0)
        if open_count > plan_count:
            extra = open_count - plan_count
            for o in (
                o for o in open_orders
                if (o["side"], o["price"], o["size"])
                == order_key
            ):
                if extra <= 0:
                    break
                actions.append({
                    "type" : "CANCEL",
                    "id"   : o["id"],  # ID needed to cancel
                    "side" : o["side"],
                    "price": o["price"],
                    "size" : o["size"],
                })
                extra -= 1

    # Place missing planned orders
    for order_key, plan_count in plan_counter.items():
        open_count = open_counter.get(order_key, 0)
        if plan_count > open_count:
            missing = plan_count - open_count
            for _ in range(missing):
                actions.append({
                    "type" : "PLACE",
                    "side" : order_key[0],
                    "price": order_key[1],
                    "size" : order_key[2],
                })

    return actions
