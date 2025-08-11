# modules/type_caster_models.py - updated 2025-08-11

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Type, Dict


class Market(BaseModel):
    clobPairId: str
    ticker: str
    status: str
    oraclePrice: float
    priceChange24H: float
    volume24H: float
    trades24H: int
    nextFundingRate: float
    initialMarginFraction: float
    maintenanceMarginFraction: float
    openInterest: float
    atomicResolution: int
    quantumConversionExponent: int
    tickSize: float
    stepSize: float
    stepBaseQuantums: int
    subticksPerTick: int
    marketType: str
    openInterestLowerCap: float
    openInterestUpperCap: float
    baseOpenInterest: float
    defaultFundingRate1H: float


class FilledOrder(BaseModel):
    id: str
    side: str
    liquidity: str
    type: str
    market: str
    marketType: str
    price: float
    size: float
    fee: float
    affiliateRevShare: float
    createdAt: datetime
    createdAtHeight: int
    orderId: str
    clientMetadata: str
    subaccountNumber: int


class OpenOrders(BaseModel):
    id: str
    subaccountId: str
    clientId: str
    clobPairId: str
    side: str
    size: float
    totalFilled: float
    price: float
    type: str
    status: str
    timeInForce: str
    reduceOnly: bool
    orderFlags: str
    goodTilBlockTime: datetime
    createdAtHeight: int
    clientMetadata: str
    updatedAt: datetime
    updatedAtHeight: int
    postOnly: bool
    ticker: str
    subaccountNumber: int


class Subaccount(BaseModel):
    address: str
    subaccountNumber: int
    equity: float
    freeCollateral: float
    marginEnabled: bool
    updatedAtHeight: int
    latestProcessedBlockHeight: int


class Position(BaseModel):
    market: str
    status: str
    side: str
    size: float
    maxSize: float
    entryPrice: float
    exitPrice: float
    realizedPnl: float
    unrealizedPnl: float
    createdAt: datetime
    createdAtHeight: int
    closedAt: Optional[datetime]
    sumOpen: float
    sumClose: float
    netFunding: float
    subaccountNumber: int


_MODEL_REGISTRY: Dict[str, Type[BaseModel]] = {
    "market": Market,
    "filled_order": FilledOrder,
    "open_orders": OpenOrders,
    "subaccount": Subaccount,
    "position": Position,
}
