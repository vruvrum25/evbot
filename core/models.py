# core/models.py
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time

@dataclass
class MarketEvent:
    """
    Универсальное событие рынка.
    Подходит для цен, сделок, новых рынков и т.д.
    """
    event_type: str      # Тип события: "PRICE_UPDATE", "ORDER_FILLED", "NEW_MARKET"
    source: str          # Источник: "polymarket", "binance"
    symbol: str          # Символ: "ETH", "BTC", "ETH_YES_TOKEN_ID"
    timestamp: float = field(default_factory=time.time) # Время создания события
    data: Dict[str, Any] = field(default_factory=dict)  # Все остальные данные (цена, объем и т.д.)
