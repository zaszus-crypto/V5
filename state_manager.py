#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STATE & ANTI-SPAM MANAGER
=========================
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any
from config import Config

log = logging.getLogger("STATE_MGR")


class StateManager:
    def __init__(self):
        self.file_path = Path(Config.STATE_FILE)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.file_path.exists():
            try:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save(self, signal_type: str, price: float):
        self.data = {
            "last_signal": signal_type,
            "last_price": float(price),
            "last_time": datetime.now(timezone.utc).isoformat()
        }
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            log.error(f"Gagal menyimpan state: {e}")

    def is_spam(self, signal_type: str, price: float) -> bool:
        """Memeriksa apakah sinyal serupa sudah pernah dikirim dalam rentang waktu & harga berdekatan."""
        if "last_time" not in self.data or price <= 0:
            return False

        last_time = datetime.fromisoformat(self.data["last_time"])
        now = datetime.now(timezone.utc)
        hours_passed = (now - last_time).total_seconds() / 3600.0

        if hours_passed < Config.COOLDOWN_HOURS:
            if self.data.get("last_signal") == signal_type:
                # Perbaikan: gunakan toleransi dollar absolut ($8.00) bukan 0.15% yang terlalu sempit
                dollar_diff = abs(price - self.data.get("last_price", 0.0))
                if dollar_diff < Config.MIN_PRICE_MOVE_DOLLARS:
                    return True
        return False
