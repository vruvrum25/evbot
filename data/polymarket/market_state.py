#MarketFinder (в data/polymarket/) — тупой исполнитель. Просто ищет и возвращает то, что нашел сейчас.

#MarketState (в data/) — умный менеджер. Хранит рынок в памяти, проверяет время, обновляет при необходимости.

# data/market_state.py
import logging
from datetime import datetime, timezone
from data.polymarket.market_finder import MarketFinder

logger = logging.getLogger(__name__)

class MarketState:
    _current_market = None # Наша "память"

    @classmethod
    def get_active_market(cls):
        """
        Главный метод: возвращает активный рынок.
        Сам решает, нужно ли искать новый или можно взять из памяти.
        """
        # Если рынка нет или он истёк - ищем новый
        if cls._current_market is None or cls._is_expired(cls._current_market):
            logger.info("🔄 MarketState: Требуется обновление рынка...")
            new_market = MarketFinder.find_eth_15m_market()
            
            if new_market:
                cls._current_market = new_market
                logger.info(f"💾 MarketState: Рынок запомнен [{new_market['condition_id']}]")
            else:
                # Если не нашли, сбрасываем память на всякий случай
                cls._current_market = None
                
        return cls._current_market

    @staticmethod
    def _is_expired(market):
        """Проверка времени истечения (внутренний метод)."""
        try:
            end_time_str = market.get('end_date_iso')
            if not end_time_str: return True
            
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            is_expired = now >= end_time
            if is_expired:
                 logger.info("⌛ MarketState: Текущий рынок истёк.")
            
            return is_expired
        except Exception as e:
            logger.error(f"⚠️ Ошибка проверки времени рынка: {e}")
            return True
