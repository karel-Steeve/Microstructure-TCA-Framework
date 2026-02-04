"""
Market Microstructure Framework: Strategic Visualization

This module generates high-fidelity charts for monitoring execution performance 
and identifying risk management events.

Features:
    - Execution Monitoring: Visualization of strategy benchmarks vs. Market Mid-price
    - Risk Event Tracking: Vertical mapping of Stop-Loss triggers and execution halts
    - Dynamic Plotting: Multi-asset and multi-strategy performance overlay
    - Visual TCA: Graphical representation of slippage and price drift

Requirements:
    - matplotlib
    
Author: Tchami Karel
Date: 2026-02-04
"""
import matplotlib.pyplot as plt

def plot_execution_results(df, p_twap, p_vwap):
    plt.figure(figsize=(12, 6))
    
    # Tracer le prix Mid
    plt.plot(df['timestamp'], df['mid'], label='Prix Marché (Mid)', color='gray', alpha=0.5)
    
    # Tracer les lignes horizontales pour nos exécutions
    plt.axhline(y=p_twap, color='blue', linestyle='--', label=f'Exécution TWAP: {p_twap:.4f}')
    plt.axhline(y=p_vwap, color='green', linestyle='-', label=f'Exécution VWAP: {p_vwap:.4f}')
    
    plt.title("Comparaison des Stratégies d'Exécution")
    plt.xlabel("Temps")
    plt.ylabel("Prix")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_risk_stop(df, p_risk, stop_index):
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['mid'], label='Prix Marché', color='gray', alpha=0.6)
    
    if stop_index is not None:
        # Ligne verticale au moment de l'arrêt
        stop_time = df['timestamp'].iloc[stop_index]
        plt.axvline(x=stop_time, color='red', linestyle='--', label='STOP-LOSS ACTIVÉ')
        
        # Colorer la zone après l'arrêt en rouge clair
        plt.axvspan(stop_time, df['timestamp'].iloc[-1], color='red', alpha=0.1, label='Exécution stoppée')
        
        # Ligne horizontale du prix moyen obtenu
        plt.axhline(y=p_risk, color='orange', linestyle='-', label=f'Prix moyen Risk: {p_risk:.4f}')

    plt.title("Visualisation du Stop-Loss d'Exécution")
    plt.legend()
    plt.show()