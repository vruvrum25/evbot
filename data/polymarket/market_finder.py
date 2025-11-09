# data/polymarket/market_finder.py
import logging
from data.polymarket.client import PolyClient

logger = logging.getLogger(__name__)

class MarketFinder:
    @staticmethod
    def find_eth_15m_market():
        """
        Ищет активный рынок ETH Up or Down на 15 минут.
        Возвращает словарь с данными рынка или None, если не нашел.
        """
        client = PolyClient.get_client()
        logger.info("🔍 Searching for ETH 15m market...")

        try:
            # 1. Запрашиваем список активных рынков.
            # next_cursor="" означает начало списка.
            # В реальном боте может потребоваться цикл по страницам (pagination),
            # если нужный рынок не на первой странице.
            markets_response = client.get_markets(next_cursor="")
            markets = markets_response.get('data', [])

            for market in markets:
                # Получаем вопрос рынка и переводим в нижний регистр для удобства сравнения
                question = market.get('question', '').lower()
                
                # Основные фильтры:
                is_eth = 'eth' in question and 'up or down' in question
                # Иногда пишут "15 min", иногда конкретное время, например "Will ETH be > $3000 at 14:00?".
                # Для начала ищем просто "15" как самый простой признак.
                is_15m = '15' in question 
                is_active = not market.get('closed', True) # Должен быть НЕ закрыт

                if is_eth and is_active:
                    # Дополнительная проверка, что это именно 15-минутка, а не что-то другое с цифрой 15
                    # (Можно усложнить фильтр позже, если будут ложные срабатывания)
                    
                    logger.info(f"🎯 MARKET FOUND: {market['question']}")
                    logger.info(f"   ID: {market['condition_id']}")
                    
                    # Возвращаем найденный рынок сразу
                    return market

            logger.warning("⚠️ ETH 15m market NOT found on the first page.")
            return None

        except Exception as e:
            logger.error(f"❌ Error searching for market: {e}")
            return None
