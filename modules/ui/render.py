# modules/ui/render.py - updated 2025-08-06

def render_table(title, headers, rows):
    html = (
        f"<h2>{title}</h2>\n"
        "<table border=1 cellpadding=4 "
        "cellspacing=0 "
        "style='border-collapse: collapse;'>"
    )
    html += "<tr>" + "".join(
        f"<th>{h}</th>" for h in headers
    ) + "</tr>"
    for row in rows:
        html += "<tr>"
        for val in row:
            align = (
                "right"
                if isinstance(val, str)
                and val.replace(",", "")
                     .replace("$", "")
                     .replace("%", "")
                     .replace(".", "")
                     .replace("-", "")
                     .isdigit()
                else "center"
            )
            html += (
                f"<td style='text-align: {align};'>"
                f"{val}</td>"
            )
        html += "</tr>"
    html += "</table><br>"
    return html

def render_data_as_html(
    timestamp, market, subaccount, position, filled_order,
    open_orders, order_plan, order_actions
):

    html = (
        "<html><head>"
        "<title>DYDX Account View</title></head>"
        "<body style='font-family: sans-serif;'>")
    html += (
        "<h1>DYDX Account View</h1>"
        f"<h4>⏱ Last Updated: {timestamp}</h4>")

    # 📊 Market Data
    try:
        oracle_price = market["oraclePrice"]
        market_fmt = [[
            market["ticker"],
            f"${oracle_price:,.2f}",
        ]]
    except Exception:
        market_fmt = [["—", "—"]]

    html += render_table(
        "📊 Market",
        ["Ticker", "Oracle Price"],
        market_fmt
    )

    # 📈 Open Position
    equity = subaccount["equity"]
    side = position["side"]
    size = position["size"]
    entry_price = position["entryPrice"]
    exit_price = position.get("exitPrice") or 0
    sum_open = position["sumOpen"]
    sum_close = position["sumClose"]
    realized_pnl = position["realizedPnl"]
    unrealized_pnl = position["unrealizedPnl"]
    net_funding = position["netFunding"]

    leverage = round(size * oracle_price / equity, 2)
    total_pnl = realized_pnl + unrealized_pnl
    risk = equity - total_pnl
    return_p = (100 * total_pnl / risk)

    pos_fmt = [[
        size,
        f"${risk:,.2f}",
        f"${total_pnl:,.2f}",
        f"${equity:,.2f}",
        f"{return_p:.2f}%",
        f"{leverage:,.2f}",
        f"{'-' if net_funding < 0 else ''}${abs(net_funding):,.2f}"
    ]]

    html += render_table(
        "📈 Position",
        ["Size", "Deposit", "Total PnL", "Equity",
            "Return %", "Leverage", "Net Funding"],
        pos_fmt
    )

    # 🧾 Open Orders
    orders_fmt = [
        [
            o.get("side", "—"),
            f"${o.get('price', 0):,.2f}",
            f"{o.get('size', 0):.4f}",
            f"{o.get('totalFilled', 0):.4f}",
        ]
        for o in open_orders
    ]
    html += render_table(
        "🧾 Open Orders",
        ["Side", "Price", "Size", "Filled"],
        orders_fmt
    )

    # 🛒 Order Plan (buy + sell)
    plan_fmt = [
        [
            p.get("side", "—").upper(),
            f"${p['orderPrice']:,.2f}",
            f"{p['orderSize']:.4f}",
            f"{p['positionSize']:.4f}",
            f"${p['totalPnL']:,.2f}",
            f"{p['equityLeverage']:,.2f}",
            "✅" if p.get("includeFlag") else "❌"
        ]
        for p in order_plan
    ]
    html += render_table(
        "🛒 Order Plan",
        ["Side", "Price", "Size", "Position",
         "Total PnL", "Leverage", "Include"],
        plan_fmt
    )

    # ⚙️ Planned Actions (Cancel + Place)
    order_actions = order_actions or []
    actions_fmt = [
        [
            a["type"].upper(),
            a.get("id", "—"),  # Only cancel actions have IDs
            a["side"],
            f"${a['price']:,.2f}",
            f"{a['size']:.4f}",
        ]
        for a in order_actions
    ]

    html += render_table(
        "⚙️ Order Actions",
        ["Type", "ID", "Side", "Price", "Size"],
        actions_fmt
    )

    html += "</body></html>"
    return html
