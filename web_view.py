# web_view.py - updated 2025-08-11

import os, json
from flask import Flask, redirect, request
from modules.ui.render import render_data_as_html

app = Flask(__name__)

@app.route("/")
def view():
    if not os.path.exists("output/data.json"):
        return "Waiting for pipeline to generate data..."
    with open("output/data.json") as f:
        data = json.load(f)
    paused = os.path.exists("output/paused.flag")
    html = render_data_as_html(
        timestamp=data["timestamp"],
        market=data["market"],
        subaccount=data["subaccount"],
        position=data["position"],
        filled_order=data["filled_order"],
        open_orders=data["open_orders"],
        order_plan=data["order_plan"],
        order_actions=data["order_actions"]
    )

    btn = (
        "<form method='post' action='/toggle'>"
        f"<input type='submit' value='{'Start' if paused else 'Stop'}'>"
        "</form>"
    )
    meta_refresh = "" if paused else (
        "<meta http-equiv='refresh' content='60'>"
    )
    return (
        "<html><head>"
        + meta_refresh +
        "<title>DYDX View</title></head><body>"
        + html + btn + "</body></html>"
    )

@app.route("/toggle", methods=["POST"])
def toggle():
    flag = "output/paused.flag"
    if os.path.exists(flag):
        os.remove(flag)
    else:
        open(flag, "w").close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
