# modules/calculation_handler.py - new 2025-08-16

def handle_calculations(market, subaccount, position):
    """
    Handles calculations for rendering.
    Returns a dict with derived values.
    """

    equity = subaccount["equity"]
    size = position["size"]
    mmf = market["maintenanceMarginFraction"]
    oracle_price = market["oraclePrice"]

    # Leverage & Liquidation
    leverage = size * oracle_price / equity
    liquidation = (
        (1 + mmf) * (leverage - 1) * equity / size
    )
    cushion = oracle_price - liquidation
    leverage = round(leverage, 2)

    # PnL
    pnl = position["realizedPnl"] + position["unrealizedPnl"]
    deposit = equity - pnl
    pnl_p = (100 * pnl / deposit)

    return {
        "leverage": leverage,
        "liquidation": liquidation,
        "cushion": cushion,
        "pnl": pnl,
        "deposit": deposit,
        "pnl_p": pnl_p,
    }
