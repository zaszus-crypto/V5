#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import load_dotenv

# Load file .env jika ada
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)


class Config:
    BOT_NAME = "XAU/USD PREDATOR"
    VERSION = "10.1-QUANT-PRODUCTION"

    # Instrumen & Simbol
    # Disarankan 'XAUUSD=X' untuk spot broker, atau 'GC=F' untuk futures
    PRIMARY_SYMBOL = os.getenv("SYMBOL", "GC=F")
    FALLBACK_SYMBOLS = ["GC=F", "GLD", "SI=F"]    
    DXY_SYMBOL = "DX-Y.NYB"

    # Manajemen Resiko & Akun
    ACCOUNT_BALANCE = float(os.getenv("ACCOUNT_BALANCE", "10000.0"))
    RISK_PERCENT = float(os.getenv("RISK_PERCENT", "1.0"))
    MAX_ALLOWED_RISK_PERCENT = float(os.getenv("MAX_ALLOWED_RISK_PERCENT", "1.5")) # Hard stop ceiling
    CONTRACT_SIZE = float(os.getenv("CONTRACT_SIZE", "100.0"))                     # 100 troy oz per 1 lot
    MIN_RR_RATIO = float(os.getenv("MIN_RR_RATIO", "2.0"))
    COOLDOWN_HOURS = int(os.getenv("COOLDOWN_HOURS", "4"))
    MIN_PRICE_MOVE_DOLLARS = float(os.getenv("MIN_PRICE_MOVE_DOLLARS", "8.0"))

    # Machine Learning Thresholds
    ML_WIN_PROB_THRESHOLD = float(os.getenv("ML_WIN_PROB_THRESHOLD", "0.62"))
    ML_TARGET_PCT = float(os.getenv("ML_TARGET_PCT", "0.0035")) # 0.35% (~$9-$10 pada harga emas $2700)

    # Parameter SMC (Smart Money Concepts)
    H4_LOOKBACK_SWING = int(os.getenv("H4_LOOKBACK_SWING", "5"))
    M15_LOOKBACK_CHOCH = int(os.getenv("M15_LOOKBACK_CHOCH", "3"))
    FVG_LOOKBACK_BARS = int(os.getenv("FVG_LOOKBACK_BARS", "24"))
    FVG_MIN_ATR_RATIO = float(os.getenv("FVG_MIN_ATR_RATIO", "0.30"))
    FVG_TOLERANCE = float(os.getenv("FVG_TOLERANCE", "0.0025"))
    SL_BUFFER_ATR_MULT = float(os.getenv("SL_BUFFER_ATR_MULT", "0.40"))

    # Sesi Trading (WIB) - London & New York (13:00 s/d 23:00 WIB)
    SESSION_START_HOUR = int(os.getenv("SESSION_START_HOUR", "13"))
    SESSION_END_HOUR = int(os.getenv("SESSION_END_HOUR", "23"))

    # Indikator Teknis
    EMA_FAST = 50
    EMA_SLOW = 200
    RSI_PERIOD = 14
    MIN_ATR_PERCENTILE = 30

    # Eksekusi Loop / Cron
    RUN_CONTINUOUS_LOOP = os.getenv("RUN_CONTINUOUS_LOOP", "false").lower() == "true"
    POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "300")) # 5 menit

    # MetaTrader 5 Bridge
    MT5_AUTO_EXECUTION = os.getenv("MT5_AUTO_EXECUTION", "false").lower() == "true"
    MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))
    MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
    MT5_SERVER = os.getenv("MT5_SERVER", "")
    MT5_MAGIC_NUMBER = int(os.getenv("MT5_MAGIC_NUMBER", "888101"))

    # Telegram Credentials
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

    # File Paths
    STATE_FILE = "predator_state.json"
    CHART_FILE = "chart_signal.png"
