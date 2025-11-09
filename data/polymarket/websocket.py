# data/polymarket/websocket.py
import json
import time
import threading
import logging
from websocket import WebSocketApp
from config.settings import Config
from data.polymarket.client import PolyClient

logger = logging.getLogger(__name__)

class PolyWebSocket:
    """
    Управляет WebSocket-соединением с Polymarket.
    Может работать в двух режимах:
    - MARKET: получает цены (публичные данные)
    - USER: получает обновления по своим ордерам (приватные данные)
    """
    BASE_URL = "wss://ws-subscriptions-clob.polymarket.com"

    def __init__(self, channel_type, token_ids=None):
        self.channel_type = channel_type
        self.token_ids = token_ids or []
        self.ws = None
        self.thread = None
        self.keep_running = True

    def start(self):
        """Запускает WebSocket в отдельном потоке."""
        url = f"{self.BASE_URL}/ws/{self.channel_type}"
        logger.info(f"📡 WS [{self.channel_type}]: Connecting to {url}...")
        
        self.ws = WebSocketApp(
            url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def _on_open(self, ws):
        logger.info(f"📡 WS [{self.channel_type}]: Connected!")
        
        if self.channel_type == "market":
            # Подписываемся на токена (YES/NO)
            payload = {
                "assets_ids": self.token_ids,
                "type": "market"
            }
            ws.send(json.dumps(payload))
            logger.info(f"📡 WS [market]: Subscribed to {len(self.token_ids)} assets")

        elif self.channel_type == "user":
            # Для пользовательского канала нужна авторизация
            client = PolyClient.get_client()
            creds = client.get_api_creds() # ВАЖНО: нам нужны сами ключи

            auth_payload = {
                "type": "user",
                "auth": {
                    "apiKey": creds.api_key,
                    "secret": creds.api_secret,
                    "passphrase": creds.api_passphrase
                }
            }
            ws.send(json.dumps(auth_payload))
            logger.info("📡 WS [user]: Authenticated and subscribed to orders")

        # Запускаем пинг, чтобы соединение не разорвалось
        threading.Thread(target=self._ping_loop, args=(ws,), daemon=True).start()

    def _ping_loop(self, ws):
        while self.keep_running and ws.sock and ws.sock.connected:
            try:
                ws.send("PING")
                time.sleep(15) # Пинг каждые 15 секунд
            except Exception:
                break

    def _on_message(self, ws, message):
        # ТУТ БУДЕТ ГЛАВНАЯ МАГИЯ
        # Пока просто выводим, но потом направим в стратегии
        try:
            data = json.loads(message)
            # print(f"⚡ WS [{self.channel_type}] MSG: {data}")
            
            # Пример обработки (можно улучшить):
            if self.channel_type == "market":
                for item in data:
                     if 'price' in item:
                         # Это обновление цены!
                         # item = {'asset_id': '...', 'price': '0.55', 'side': 'BUY', 'size': '100'}
                         logger.debug(f"💲 Price update: {item.get('asset_id')} = {item.get('price')}")

        except Exception as e:
            logger.error(f"💥 WS Message Error: {e}")

    def _on_error(self, ws, error):
        logger.error(f"💥 WS [{self.channel_type}] Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        logger.warning(f"🔌 WS [{self.channel_type}] Closed: {close_msg}")
