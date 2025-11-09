# main.py
import logging
import time
from data.polymarket.client import PolyClient
# 👇 Импортируем наш новый поисковик
from data.polymarket.market_finder import MarketFinder 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🤖 Bot starting...")
    
    # 1. Проверка подключения (можно оставить для уверенности)
    PolyClient.get_client()

    # 2. Бесконечный цикл поиска (как в реальной работе)
    while True:
        try:
            logger.info("🔎 --- Starting new search cycle ---")
            
            # Ищем рынок
            market = MarketFinder.find_eth_15m_market()
            
            if market:
                # Если нашли - выводим детали и (в будущем) запускаем стратегию
                logger.info(f"✅ Ready to trade on: {market['question']}")
                # Тут будет: strategy.run(market)
                
                # Для теста пока просто подождем подольше, чтобы не спамить
                logger.info("💤 Waiting 60s before next check...")
                time.sleep(60)
            else:
                logger.info("💤 Market not found, retrying in 10s...")
                time.sleep(10)

        except KeyboardInterrupt:
            logger.info("🛑 Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"💥 Unexpected error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
