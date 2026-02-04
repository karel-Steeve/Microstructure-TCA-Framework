"""
Market Microstructure Framework: Order Execution & Risk Control

This module implements institutional execution strategies (TWAP/VWAP) with 
real-world constraints and automated risk management guardrails.

Features:
    - Slicing Algorithms: Implementation of TWAP and VWAP execution logic
    - Transaction Cost Analysis (TCA): Integration of latency, fees, and market impact
    - Execution Risk Control: Automated Stop-Loss (Circuit Breaker) in Basis Points
    - Fill Simulation: Calculation of completion rates and average execution prices

Requirements:
    - pandas
    - numpy

Author: Tchami Karel
Date: 2026-02-04
"""
import numpy as np
import pandas as pd

def execute_twap(df, total_quantity):
    """
    Simule une exécution TWAP (Time Weighted Average Price).
    On divise la quantité également sur chaque minute.
    """
    n_steps = len(df)
    qty_per_step = total_quantity / n_steps
    
    # On achète au prix 'ask' (prix de vente du marché)
    execution_price = (df['ask'] * qty_per_step).sum() / total_quantity
    
    return execution_price

def execute_vwap(df, total_quantity):
    """
    Simule une exécution VWAP (Volume Weighted Average Price).
    On suit le profil du volume historique du marché.
    """
    total_market_volume = df['volume'].sum()
    
    # On calcule quelle part du volume total chaque minute représente
    df['volume_participation'] = df['volume'] / total_market_volume
    
    # On achète proportionnellement au volume du marché
    df['shares_to_buy'] = df['volume_participation'] * total_quantity
    
    execution_price = (df['ask'] * df['shares_to_buy']).sum() / total_quantity
    
    return execution_price

def calculate_market_impact(quantity, market_daily_vol, sigma=0.01):
    """
    Modèle de Square Root Law (Loi de la racine carrée).
    Impact = sigma * sqrt(Quantité_ordonnée / Volume_journalier)
    """
    # Plus on achète par rapport au volume global, plus on décale le prix
    impact_pct = sigma * np.sqrt(quantity / market_daily_vol)
    return impact_pct

def apply_real_world_constraints(execution_price, latency_ms=50, fee_bps=1.0):
    """
    Ajoute des frais (en points de base) et simule un impact de latence.
    1 bps = 0.01%
    """
    # Simulation simplifiée : la latence nous fait souvent acheter un peu plus cher
    latency_impact = (latency_ms / 1000) * 0.0001 
    
    # Calcul des frais
    fees = execution_price * (fee_bps / 10000)
    
    final_price = execution_price + latency_impact + fees
    return final_price

def execute_with_risk_limit(df, total_quantity, risk_budget_bps=50):
    n_steps = len(df)
    qty_per_step = total_quantity / n_steps
    initial_price = df['mid'].iloc[0]
    limit_price = initial_price * (1 + risk_budget_bps / 10000)
    
    executed_shares = 0
    total_cost = 0
    stop_index = None # On stocke le moment de l'arrêt
    
    for i in range(n_steps):
        current_ask = df['ask'].iloc[i]
        if current_ask > limit_price:
            stop_index = i
            break
        total_cost += current_ask * qty_per_step
        executed_shares += qty_per_step
        
    avg_price = total_cost / executed_shares if executed_shares > 0 else 0
    completion_rate = (executed_shares / total_quantity) * 100
    
    return avg_price, completion_rate, stop_index