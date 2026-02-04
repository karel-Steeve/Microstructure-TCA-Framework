"""
Market Microstructure Framework: Synthetic Data Generation

This module simulates high-frequency market data, providing the foundational price 
and volume dynamics required for execution benchmarking.

Features:
    - Geometric Random Walk: Generation of realistic Mid-price movements
    - Dynamic Order Book: Simulation of Bid/Ask spreads and liquidity depth
    - Volume Modeling: Generation of market volumes for VWAP strategy testing
    - Seeded Randomness: Support for reproducible market scenarios

Requirements:
    - numpy
    - pandas

Author: Tchami Karel
Date: 2026-02-04
"""
import pandas as pd
import numpy as np

def generate_market_data(n_steps=1000, seed=None):
    """Génère des données de marché synthétiques avec Spread et Volume."""
    if seed is not None:
        np.random.seed(seed)
    else:
        # On ne fixe pas de seed, ou on en utilise une basée sur l'heure
        np.random.seed(np.random.randint(0, 10000))
    
    # Simulation du prix Mid (Marche aléatoire)
    returns = np.random.normal(0, 0.0001, n_steps)
    mid_price = 100 * np.exp(np.cumsum(returns))
    
    # Ajout d'un spread (entre 0.01 et 0.05)
    spread = np.random.uniform(0.01, 0.05, n_steps)
    bid_price = mid_price - (spread / 2)
    ask_price = mid_price + (spread / 2)
    
    # Volume (Log-normal pour être réaliste)
    volume = np.random.lognormal(mean=10, sigma=1, size=n_steps).astype(int)
    
    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=n_steps, freq='min'),
        'bid': bid_price,
        'ask': ask_price,
        'mid': mid_price,
        'volume': volume
    })
    return df

# Test
df = generate_market_data()
print(df.head())