# ОБЩИЕ настройки (ключи, хост)


Только то, что точно общее для всех (ключи, адрес API Polymarket, Chain ID)



import os
from dotenv import load_dotenv

# Загружаем секреты из .env
load_dotenv()

class Config:
    # --- Доступы ---
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    FUNDER_ADDRESS = os.getenv("FUNDER_ADDRESS")
    HOST = "https://clob.polymarket.com/"
    CHAIN_ID = 137
    
    # --- Настройки Торговли ---
    BET_SIZE_USD = 5.0        # Размер ставки $5
    MIN_EDGE = 0.05           # Входим, если EV > 5%
