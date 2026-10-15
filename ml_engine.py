#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MACHINE LEARNING CLASSIFIER (SYMMETRICAL QUANT ENGINE)
======================================================
Koreksi total dari bug v10.0:
Target BEARISH kini secara eksplisit menguji apakah harga TURUN >0.35%.
"""

import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.ensemble import RandomForestClassifier
from indicators import Indicators
from config import Config


class MLClassifierEngine:
    @staticmethod
    def evaluate_probability(df_h1: pd.DataFrame, df_m15: pd.DataFrame, bias: str) -> Tuple[bool, float, str]:
        """
        Melatih Random Forest terisolasi dengan target simetris:
        - Bullish: target 1 jika naik >= target_pct
        - Bearish: target 1 jika turun <= -target_pct
        """
        try:
            df = df_h1.copy()
            df['ema50'] = Indicators.ema(df['close'], 50)
            df['rsi'] = Indicators.rsi(df['close'], 14)
            df['atr'] = Indicators.atr(df, 14)
            df['return'] = df['close'].pct_change()

            target_pct = Config.ML_TARGET_PCT

            # TARGET SIMETRIS
            if bias == "BULLISH":
                df['target'] = (df['close'].shift(-4) > df['close'] * (1.0 + target_pct)).astype(int)
            else:
                # Perbaikan Kritis: Uji penurunan harga secara eksplisit!
                df['target'] = (df['close'].shift(-4) < df['close'] * (1.0 - target_pct)).astype(int)

            df = df.dropna()
            if len(df) < 50:
                return True, 0.65, "ML Check Bypassed (Data Historis Kurang)"

            features = ['rsi', 'atr', 'return']
            X = df[features]
            y = df['target']

            # Pastikan ada variasi label
            if len(np.unique(y)) < 2:
                return True, 0.65, "ML Check Bypassed (Data market satu arah)"

            # Random Forest terkontrol (max_depth=4 untuk mengurangi overfitting)
            model = RandomForestClassifier(n_estimators=50, max_depth=4, min_samples_leaf=3, random_state=42)
            model.fit(X, y)

            # Fitur real-time dari bar M15 yang SUDAH CLOSED
            latest_rsi = Indicators.rsi(df_m15['close'], 14).iloc[-1]
            latest_atr = Indicators.atr(df_h1, 14).iloc[-1]
            latest_ret = df_m15['close'].pct_change().iloc[-1]

            current_features = np.array([[latest_rsi, latest_atr, latest_ret]])
            prob = model.predict_proba(current_features)[0]

            # Keduanya mengambil prob[1] (probabilitas target tercapai)!
            win_prob = float(prob[1])

            threshold = Config.ML_WIN_PROB_THRESHOLD
            if win_prob >= threshold:
                return True, win_prob, f"ML Confidence: {win_prob*100:.1f}% (Lolos >= {threshold*100:.0f}%)"
            else:
                return False, win_prob, f"ML Ditolak: {win_prob*100:.1f}% (< {threshold*100:.0f}%)"

        except Exception as e:
            return True, 0.65, f"ML Check Bypassed ({e})"
