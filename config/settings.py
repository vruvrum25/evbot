import os
from pathlib import Path
from dotenv import load_dotenv

# --- МАГИЯ ПУТЕЙ ---
# Path(__file__) - это путь к самому файлу settings.py (он внутри config/)
# .parent - это сама папка config/
CONFIG_DIR = Path(__file__).resolve().parent

# Явно говорим: загрузи .env, который лежит ПРЯМО ЗДЕСЬ, в папке config
load_dotenv(CONFIG_DIR / ".env")

class Config:
    # --- Доступы ---
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    FUNDER_ADDRESS = os.getenv("FUNDER_ADDRESS")
    
    # --- Константы Polymarket ---
    HOST = "https://clob.polymarket.com/"
    CHAIN_ID = 137
