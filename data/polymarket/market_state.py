# data/polymarket/market_state_producer.py
import asyncio
import logging
from datetime import datetime, timezone
from core.event_bus import EventBus
from core.models import MarketEvent
from .market_finder import MarketFinder

logger = logging.getLogger(__name__)

class MarketStateProducer:
    """
    Активный компонент. Периодически проверяет наличие и статус рынка.
    Если находит новый или теряет старый - сообщает в Шину.
    """
    def __init__(self):
        self._current_market = None
        self._keep_running = True

    async def start(self):
        logger.info("🚀 MarketStateProducer запущен.")
        while self._keep_running:
            # 1. Проверяем текущий рынок
            if self._current_market:
                if self._is_expired(self._current_market):
                    logger.info("⌛ Рынок истёк! Сообщаю в шину...")
                    # Публикуем событие окончания
                    await EventBus.get_bus().publish(MarketEvent(
                        event_type="MARKET_EXPIRED",
                        source="polymarket",
                        symbol="ETH",
                        data={"condition_id": self._current_market['condition_id']}
                    ))
                    self._current_market = None

            # 2. Если рынка нет - ищем
            if not self._current_market:
                new_market = MarketFinder.find_eth_15m_market()
                if new_market:
                    self._current_market = new_market
                    logger.info(f"🎉 Найден новый рынок! Сообщаю в шину: {new_market['question']}")
                    
                    # Публикуем событие о новом рынке
                    # ВАЖНО: Передаем ID токенов, чтобы WS мог подписаться
                    await EventBus.get_bus().publish(MarketEvent(
                        event_type="MARKET_FOUND",
                        source="polymarket",
                        symbol="ETH",
                        data=new_market # Передаем весь объект рынка
                    ))

            # Пауза между проверками (10 секунд достаточно)
            await asyncio.sleep(10)

    def stop(self):
        self._keep_running = False

    # _is_expired оставляем тот же, что был раньше
    @staticmethod
    def _is_expired(market):
        # ... (тот же код проверки времени) ...
        pass
