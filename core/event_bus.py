# core/event_bus.py
import asyncio
import logging
from typing import Callable, List, Dict
from core.models import MarketEvent

logger = logging.getLogger(__name__)

class EventBus:
    _instance = None

    def __init__(self):
        # Словарь подписчиков: { "PRICE_UPDATE": [func1, func2], "ALL": [func3] }
        self._subscribers: Dict[str, List[Callable[[MarketEvent], Any]]] = {}

    @classmethod
    def get_bus(cls):
        """Singleton: шина одна на всё приложение."""
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance

    def subscribe(self, event_type: str, callback: Callable):
        """
        Подписаться на определенный тип событий.
        Используй event_type="ALL", чтобы получать всё подряд (например, для логгера).
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        # logger.debug(f"🔌 EventBus: New subscriber for '{event_type}'")

    async def publish(self, event: MarketEvent):
        """
        Опубликовать событие. Оно мгновенно полетит всем подписчикам.
        """
        # 1. Отправляем тем, кто подписан на конкретный тип события
        if event.event_type in self._subscribers:
            for callback in self._subscribers[event.event_type]:
                # Запускаем задачу в фоне, чтобы не блокировать шину,
                # если подписчик медленный.
                asyncio.create_task(self._safe_execute(callback, event))

        # 2. Отправляем тем, кто подписан на ВСЁ ("ALL")
        if "ALL" in self._subscribers:
            for callback in self._subscribers["ALL"]:
                 asyncio.create_task(self._safe_execute(callback, event))

    async def _safe_execute(self, callback, event):
        """Защита от ошибок в подписчиках, чтобы одна ошибка не убила весь бот."""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)
        except Exception as e:
            logger.error(f"💥 Error in EventBus subscriber: {e}", exc_info=True)
