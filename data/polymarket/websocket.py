# data/polymarket/websocket_adapter.py
import logging
import json
from core.event_bus import EventBus
from core.models import MarketEvent
# ... остальные импорты ...

class PolyWebSocketAdapter:
    def __init__(self):
        # Слушаем шину: когда найдут рынок, мы хотим знать!
        EventBus.get_bus().subscribe("MARKET_FOUND", self.on_market_found)
        EventBus.get_bus().subscribe("MARKET_EXPIRED", self.on_market_expired)
        self.ws = None # Наш PolyWebSocket (который мы писали ранее)

    async def on_market_found(self, event: MarketEvent):
        if event.symbol == "ETH" and event.source == "polymarket":
            market_data = event.data
            # Достаем ID токенов из события
            token_ids = [
                market_data['tokens'][0]['token_id'], # YES
                market_data['tokens'][1]['token_id']  # NO
            ]
            logger.info(f"📡 WS Adapter: Получил новый рынок! Подписываюсь на {len(token_ids)} токенов...")
            
            # Если уже было соединение - закрываем старое (упрощенно)
            if self.ws: self.ws.stop() 
            
            # Запускаем наш WebSocket клиент с новыми токенами
            self.ws = PolyWebSocket("market", token_ids)
            self.ws.start() # Он начнет слать данные

    async def on_market_expired(self, event: MarketEvent):
        logger.info("📡 WS Adapter: Рынок закрыт. Останавливаю поток цен.")
        if self.ws:
            self.ws.stop()
            self.ws = None

    # А ВНУТРИ PolyWebSocket._on_message мы добавляем отправку цен в шину:
    # def _on_message(self, ws, msg):
    #    ... парсим msg ...
    #    event = MarketEvent("PRICE_UPDATE", "polymarket", "ETH", price=..., data=msg)
    #    # Так как _on_message в другом потоке, тут нужен thread-safe способ,
    #    # но для asyncio часто используют loop.call_soon_threadsafe
    #    # Для простоты пока можно использовать синхронную очередь или сделать WS асинхронным.
