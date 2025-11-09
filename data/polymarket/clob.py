# data/polymarket/client.py
import logging
from py_clob_client.client import ClobClient
from config.settings import Config # <-- Импортируем наши настройки

logger = logging.getLogger(__name__)

class PolyClient:
    _client = None # Здесь будет жить единственное подключение

    @classmethod
    def get_client(cls):
        """
        Возвращает готового к работе клиента.
        Если подключения еще нет - создает его.
        """
        if cls._client is None:
            try:
                logger.info("🔌 Connecting to Polymarket CLOB...")
                
                # 1. Создаем клиента с параметрами из Config
                cls._client = ClobClient(
                    host=Config.HOST,
                    key=Config.PRIVATE_KEY,
                    chain_id=Config.CHAIN_ID,
                    signature_type=1,            # Мы используем Proxy (Email/Magic)
                    funder=Config.FUNDER_ADDRESS # Наш Proxy-адрес
                )
                
                # 2. Самое важное: получаем API ключи (derive)
                # Это позволяет боту "представиться" бирже
                creds = cls._client.create_or_derive_api_creds()
                cls._client.set_api_creds(creds)
                
                logger.info("✅ Successfully connected and authorized!")
                
            except Exception as e:
                # Если что-то пошло не так (например, неверный ключ),
                # мы должны узнать об этом сразу.
                logger.critical(f"⛔ Connection failed: {e}")
                raise e # Останавливаем бота, без связи работать нельзя

        return cls._client





#Singleton (Одиночка): Мы используем PolyClient.get_client(). Сколько бы раз мы его ни вызывали (из разных стратегий), он создаст подключение только один раз и будет переиспользовать его. Это экономит память и ускоряет работу.

#Использование Config: Мы не пишем ключи прямо здесь, а берем их из Config. Если поменяется ключ, мы изменим его только в .env, а этот файл трогать не будем.
