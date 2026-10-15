#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
METATRADER 5 (MT5) AUTO-EXECUTION BRIDGE
========================================
Menyediakan integrasi langsung ke broker MT5 (IC Markets, Exness, RoboForex, dll).
"""

import logging
from typing import Dict, Any
from config import Config

log = logging.getLogger("MT5_BRIDGE")

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False


class MT5Bridge:
    @staticmethod
    def initialize() -> bool:
        """Koneksi ke terminal MetaTrader 5."""
        if not MT5_AVAILABLE:
            log.warning("Library 'MetaTrader5' belum terinstall (pip install MetaTrader5). MT5 Bridge nonaktif.")
            return False

        if not mt5.initialize():
            log.error(f"Gagal inisialisasi MT5: {mt5.last_error()}")
            return False

        if Config.MT5_LOGIN and Config.MT5_PASSWORD and Config.MT5_SERVER:
            authorized = mt5.login(Config.MT5_LOGIN, password=Config.MT5_PASSWORD, server=Config.MT5_SERVER)
            if not authorized:
                log.error(f"Gagal login MT5: {mt5.last_error()}")
                return False
            log.info(f"Berhasil login ke MT5 Server: {Config.MT5_SERVER}")

        return True

    @staticmethod
    def execute_market_order(setup: Dict[str, Any]) -> bool:
        """Mengirimkan Market Order otomatis ke akun broker MT5."""
        if not MT5Bridge.initialize():
            return False

        symbol = "XAUUSD" # Sesuaikan dengan simbol broker (misal: XAUUSD, XAUUSDm, GOLD)
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            symbol = "GOLD"
            symbol_info = mt5.symbol_info(symbol)

        if symbol_info is None:
            log.error("Simbol XAUUSD/GOLD tidak ditemukan di MT5.")
            mt5.shutdown()
            return False

        if not symbol_info.visible:
            mt5.symbol_select(symbol, True)

        order_type = mt5.ORDER_TYPE_BUY if setup['signal'] == "BUY" else mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).ask if setup['signal'] == "BUY" else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(setup['lot']),
            "type": order_type,
            "price": price,
            "sl": float(setup['sl']),
            "tp": float(setup['tp']),
            "deviation": 20,
            "magic": Config.MT5_MAGIC_NUMBER,
            "comment": f"Predator {Config.VERSION}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            log.error(f"Gagal order MT5: {result.comment} (RetCode: {result.retcode})")
            mt5.shutdown()
            return False

        log.info(f"✅ ORDER MT5 BERHASIL! Ticket: {result.order}, Volume: {setup['lot']} lot")
        mt5.shutdown()
        return True
