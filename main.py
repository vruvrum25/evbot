# main.py
import logging
# 👇 ВОТ ТУТ ТЕПЕРЬ ПРАВИЛЬНЫЙ ИМПОРТ 👇
from data.polymarket.client import PolyClient 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🤖 Запуск теста подключения...")
    try:
        client = PolyClient.get_client()
        server_time = client.get_server_time()
        logger.info(f"⏰ Время сервера Polymarket: {server_time}")
        logger.info("🎉 ТЕСТ ПРОЙДЕН!")
    except Exception as e:
        logger.error(f"💀 ТЕСТ ПРОВАЛЕН. Ошибка: {e}")

if __name__ == "__main__":
    main()
