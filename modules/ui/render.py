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
    block_height, market, subaccount, position, filled_order,
    open_orders, order_plans, order_actions, calculated
):

    timestamp = block_height["time"][14:16]

    html = (
        "<html><head>"
        "<title>DYDX Account View</title></head>"
        "<body style='font-family: sans-serif;'>")
    html += (
        "<h1>DYDX Account View</h1>"
        f"<h4>Time Stamped: {timestamp} minutes past the hour</h4>")

    # 📊 Market Data
    market_fmt = [[
        market["ticker"],
        f"${market['oraclePrice']:,.2f}",
        f"${calculated['liquidation']:,.2f}",
        f"${calculated['cushion']:,.2f}",
    ]]

    html += render_table(
        "📊 Market",
        ["Ticker", "Oracle Price", "Liq. Est.", "Cushion"],
        market_fmt
    )

    # 📈 Open Position
    pnl = calculated["pnl"]
    pnl_p = calculated["pnl_p"]
    funding = position["netFunding"]

    pos_fmt = [[
        f"{position['size']:,.4f}",
        f"${calculated['deposit']:,.2f}",
        f"{'-' if pnl < 0 else '+'}${abs(pnl):,.2f}",
        f"{'' if pnl_p < 0 else '+'}{pnl_p:.2f}%",
        f"${subaccount['equity']:,.2f}",
        f"{calculated['leverage']:,.2f}",
        f"{'-' if funding < 0 else '+'}${abs(funding):,.2f}",
    ]]

    html += render_table(
        "📈 Position",
        ["Size", "Deposit", "PnL", "PnL%", "Equity",
            "Leverage", "Funding"],
        pos_fmt
    )

    # 🧾 Orders (filled & open)
    filled_row = [
        "🏁",
        filled_order["side"],
        f"${filled_order['price']:,.2f}",
        f"{filled_order['size']:.4f}",
        f"{filled_order['size']:.4f}",
    ]
    open_rows = [
        [
            "⏳",
            o["side"],
            f"${o['price']:,.2f}",
            f"{o['size']:.4f}",
            f"{o['totalFilled']:.4f}"
        ]
        for o in open_orders
    ]
    combined_rows = [filled_row] + open_rows
    combined_rows.sort(
        key=lambda row: float(row[2].replace("$", "").replace(",", "")),
        reverse=True
    )
    html += render_table(
        "🧾 Orders",
        ["Status", "Side", "Price", "Size", "Filled"],
        combined_rows
    )

    # 🛒 Order Plans (buy + sell)
    plan_fmt = [
        [
            p["side"],
            f"${p['orderPrice']:,.2f}",
            f"{p['orderSize']:.4f}",
            f"{p['positionSize']:.4f}",
            f"${p['totalPnL']:,.2f}",
            f"{p['equityLeverage']:,.2f}",
            "✅" if p["includeFlag"] else "❌",
        ]
        for p in order_plans
    ]
    html += render_table(
        "🛒 Order Plan",
        ["Side", "Price", "Size", "Position",
         "PnL", "Leverage", "Include"],
        plan_fmt
    )

    # ⚙️ Planned Actions (Cancel + Place)
    order_actions = order_actions or []
    actions_fmt = [
        [
            a["type"],
            a["side"],
            f"${a['price']:,.2f}",
            f"{a['size']:.4f}",
        ]
        for a in order_actions
    ]

    html += render_table(
        "⚙️ Order Actions",
        ["Type", "Side", "Price", "Size"],
        actions_fmt
    )

    html += "</body></html>"
    return html
