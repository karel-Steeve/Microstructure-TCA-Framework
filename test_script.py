"""
Market Microstructure Framework: Master Execution Simulator

This is the main entry point for running full-scale execution simulations. 
It integrates data generation, microstructure analysis, and risk-managed execution.

Scenario:
    - Generates 200 minutes of high-frequency market data
    - Executes 100,000 shares via TWAP and VWAP
    - Applies a 100ms latency and 2bps fee structure
    - Monitors a 15bps Risk Budget with automated Circuit Breaker
    - Generates a full TCA Report and Performance Visualization

Author: Tchami Karel
Date: 2026-02-04
"""
from src.data_generator import generate_market_data
from src.microstructure import calculate_spreads, calculate_amihud_illiquidity
from src.execution import (execute_twap, execute_vwap, 
                           calculate_market_impact, apply_real_world_constraints, 
                           execute_with_risk_limit)
from src.reporting import generate_trade_report, compare_strategies
from src.visualization import plot_execution_results, plot_risk_stop

# 1. GÉNÉRATION DES DONNÉES
print("1. Génération des données de marché...")
df = generate_market_data(n_steps=200)
total_to_buy = 100000
market_price = df['mid'].mean()
daily_vol = df['volume'].sum()

# 2. CALCULS DE MICROSTRUCTURE
df = calculate_spreads(df)
df = calculate_amihud_illiquidity(df)

# 3. EXÉCUTION AVEC CONTRAINTES RÉELLES (TCA)
print("2. Simulation des stratégies TWAP/VWAP...")
p_twap_raw = execute_twap(df, total_to_buy)
p_vwap_raw = execute_vwap(df, total_to_buy)

# Application de la latence (100ms) et des frais (2.0 bps)
p_twap = apply_real_world_constraints(p_twap_raw, latency_ms=100, fee_bps=2.0)
p_vwap = apply_real_world_constraints(p_vwap_raw, latency_ms=100, fee_bps=2.0)

# 4. GESTION DU RISQUE (STOP-LOSS)
print("3. Vérification des limites de risque...")
p_risk, completion, stop_idx = execute_with_risk_limit(df, total_to_buy, risk_budget_bps=15)

# 5. AFFICHAGE DU RAPPORT FINAL
print("\n" + "="*45)
print("     FINAL QUANT RESEARCH REPORT (TCA)")
print("="*45 + "\n")
print(f"Complétion : {completion:.2f}%")
if stop_idx:
    print(f"L'algorithme s'est arrêté à l'étape : {stop_idx}")

impact = calculate_market_impact(total_to_buy, daily_vol)
generate_trade_report("STRATÉGIE TWAP", p_twap, market_price, impact)
generate_trade_report("STRATÉGIE VWAP", p_vwap, market_price, impact)
compare_strategies(p_twap, p_vwap)

print(f"\n[RISK CHECK] Ordre avec Stop-Loss : {completion:.2f}% exécuté")
print("="*45)

# 6. VISUALISATION
plot_risk_stop(df, p_risk, stop_idx)
plot_execution_results(df, p_twap, p_vwap)