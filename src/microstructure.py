"""
Market Microstructure Framework: Liquidity & Flow Analysis

This module implements advanced microstructure indicators to quantify market 
dynamics and liquidity constraints.

Features:
    - Order Imbalance (OIB): Detection of buy/sell pressure via Tick Test logic
    - Spread Analysis: Calculation of Quoted and Effective Spreads
    - Amihud Illiquidity: Estimation of price impact per unit of volume
    - Rolling Metrics: Time-series analysis of market state transitions

Requirements:
    - pandas
    

Author: Tchami Karel
Date: 2026-02-04
"""
import pandas as pd

def calculate_spreads(df):
    """Calcule le Quoted Spread et le Relative Spread."""
    df['quoted_spread'] = df['ask'] - df['bid']
    df['relative_spread'] = df['quoted_spread'] / df['mid']
    return df

def calculate_order_imbalance(df, window=10):
    """
    Simule l'Order Imbalance (OIB). 
    En réalité, il faudrait les flux d'ordres, ici on utilise 
    la direction du prix comme proxy (Tick Test simplifié).
    """
    df['price_diff'] = df['mid'].diff()
    # 1 si prix monte, -1 si baisse
    df['direction'] = df['price_diff'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    df['oib'] = df['direction'].rolling(window=window).mean()
    return df

def calculate_amihud_illiquidity(df, window=10):
    """Calcule le ratio d'illiquidité d'Amihud (|Return| / Volume)."""
    df['returns'] = df['mid'].pct_change().abs()
    df['amihud'] = (df['returns'] / df['volume']).rolling(window=window).mean()
    return df