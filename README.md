# German Power System Analysis — Demand, Generation & Residual Load

An end-to-end analysis of Germany's electricity system using hourly data from the ENTSO-E Transparency Platform. The project explores demand patterns, renewable generation trends, and residual load dynamics — key concepts for understanding modern power systems with high renewable penetration.

## What it covers

- **Demand analysis** — yearly, monthly, and hourly demand profiles; weekday vs. weekend patterns
- **Generation mix** — breakdown of renewables (solar, wind onshore/offshore, hydro, biomass) vs. fossil fuels and nuclear over time
- **Renewable share** — growth trajectory of renewables as a percentage of total generation
- **Residual load** — distribution, time series, duration curve, and ramping behaviour
- **Duck curve** — comparison of residual load shape under low vs. high renewable scenarios
- **Negative residual load** — hours per year where renewables exceed demand

## Project structure

```
├── Deutsche Strom Analyse.py   # Main analysis script
├── data/
│   ├── Electricity Generation.csv
│   ├── Electricity Consumption.csv
│   └── Final_df_Deutsche Strom Analysis.csv
└── outputs/                    # Generated charts (PNG)
```

## Requirements

```
pandas
numpy
matplotlib
```

Install with:

```bash
pip install pandas numpy matplotlib
```

## Usage

```bash
python "Deutsche Strom Analyse.py"
```

Charts are saved to the `outputs/` directory.

## Data source

Electricity generation and consumption data from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/), covering Germany's bidding zone.
