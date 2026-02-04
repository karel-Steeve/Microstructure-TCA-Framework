"""
Market Microstructure Framework: Performance Reporting & TCA

This module provides standardized reporting tools to evaluate the efficiency 
of execution strategies compared to market benchmarks.

Features:
    - Slippage Metrics: Calculation of execution performance in Basis Points (bps)
    - Benchmarking: Comparison of strategy prices against Arrival and Mid prices
    - Comparative Analysis: Direct statistical comparison between TWAP and VWAP
    

Requirements:
    - pandas

Author: Tchami Karel
Date: 2026-02-04
"""
def generate_trade_report(strategy_name, price, market_price, impact):
    """
    Génère un rapport détaillé de Transaction Cost Analysis (TCA).
    """
    # Calcul du slippage en Points de Base (1 bps = 0.01%)
    # Formule : (Prix_Exécution / Prix_Benchmark - 1) * 10000
    slippage_bps = (price / market_price - 1) * 10000
    
    print(f"--- Rapport détaillé : {strategy_name} ---")
    print(f"Prix d'Exécution Moyen : {price:.4f}")
    print(f"Benchmark (Mid Moyen)  : {market_price:.4f}")
    
    if slippage_bps > 0:
        print(f"Slippage (Coût)        : +{slippage_bps:.2f} bps (Plus cher que le marché)")
    else:
        print(f"Slippage (Gain)        : {slippage_bps:.2f} bps (Mieux que le marché)")
        
    print(f"Impact de Marché estimé: {impact*100:.4f}%")
    print("-" * 40)

def compare_strategies(p_twap, p_vwap):
    """Compare directement les deux stratégies."""
    diff_bps = (p_twap / p_vwap - 1) * 10000
    better = "VWAP" if p_twap > p_vwap else "TWAP"
    print(f"RÉSULTAT COMPARATIF : {better} est plus efficace de {abs(diff_bps):.2f} bps.")