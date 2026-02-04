# -Microstructure-TCA-Framework
General Overview:
This project implements a quantitative research framework dedicated to Market Microstructure and Transaction Cost Analysis (TCA).

The framework generates high-frequency synthetic market data, calculates advanced liquidity indicators, and benchmarks institutional execution strategies (TWAP, VWAP) under real-world constraints (latency, fees, market impact) and risk limits (Stop-Loss).

Philosophy:
The simulator is built upon three fundamental pillars of quantitative execution:

Microstructure Analysis Identifying order book dynamics through the calculation of spreads, flow imbalance (OIB), and illiquidities.

Execution Optimization Implementing order slicing algorithms designed to minimize the average execution price relative to market benchmarks.

Realism & Risk Control Systematic integration of market frictions (Slippage, Fees) and "Guardrails" to halt execution during adverse price movements.

Microstructure Indicators:
At each time step, the framework computes key metrics to characterize market conditions:

Quoted Spread: A measure of the immediate cost of liquidity.

Order Imbalance (OIB): Calculated via a rolling Tick Test (range [-1, +1]), this indicator measures the relative pressure of buyer vs. seller flows.

Amihud Illiquidity Ratio: An estimation of the average price change induced by a specific traded volume.

Execution Strategies & Benchmarks:
The project compares two industry-standard approaches:

1. TWAP (Time Weighted Average Price)
Method: Linear slicing of the total order over the entire duration of the session.

Objective: Time-neutrality and reduction of instantaneous market impact.

2. VWAP (Volume Weighted Average Price)
Method: Volume allocation proportional to the market’s historical (or simulated) volume profile.

Objective: Mimic market liquidity for a more "invisible" execution.

Risk Management: Execution Stop-Loss
The framework includes a critical safety feature for any execution desk:

Risk Budget (bps): Defines a maximum tolerance for price deviation from the Arrival Price.

Circuit Breaker: If the Ask price exceeds the limit defined in basis points, the algorithm instantly halts execution to protect capital.

Completion Reporting: Analysis of the percentage of the order successfully filled before the stop-loss was triggered.

Transaction Cost Analysis (TCA):
Execution success is measured using normalized industry metrics:

Slippage in BPS: The gap between the average execution price and the market's average Mid-price.

Market Impact (Square Root Law): A theoretical estimation of the price decay induced by our own order size.

Real-world Constraints: Adjusted execution prices accounting for network latency (in ms) and brokerage fees (Basis Points).

Repository Structure:
src/data_generator.py: Synthetic price and volume generation engine (Random Walk).

src/microstructure.py: Calculation of OIB, Spread, and Illiquidity indicators.

src/execution.py: Core logic for TWAP, VWAP, and Risk Controls.

src/reporting.py: Statistical performance analysis and Slippage calculation.

src/visualization.py: Benchmark charts and Stop-Loss monitoring visualizations.

test_script.py: Main entry point for running a full simulation.
