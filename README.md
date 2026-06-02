# German Power System Analysis
### Demand, Generation & Residual Load (2020–2025)

An end-to-end analysis of Germany's electricity system using hourly data from the SMARD platform. The project explores demand patterns, renewable generation trends, and residual load dynamics — key concepts for understanding modern power grids with high renewable penetration.

---

## Highlights

- Hourly data spanning **2020–2025** (~47,000 data points)
- Full data pipeline: loading, cleaning, merging, feature engineering
- **14 visualisations** covering demand, generation mix, and residual load
- Key performance indicators (KPIs) on renewable share and grid flexibility

---

## Visualisations

### Demand Analysis

**Hourly Electricity Demand Time Series**
![Hourly Demand](outputs/hourly_demand_time_series.png)
Demand follows a clear seasonal cycle — higher in winter, lower in summer — with a noticeable dip in 2020 likely linked to reduced industrial activity during COVID-19 lockdowns.

**Average Yearly Demand**
![Yearly Demand](outputs/yearly_demand.png)
Overall demand has remained relatively stable across years, reflecting a balance between efficiency gains and electrification of heating and transport.

**Average Monthly Demand**
![Monthly Demand](outputs/monthly_demand.png)
Winter months (December–January) show significantly higher demand than summer, driven by heating and shorter daylight hours reducing natural light usage.

**Average Hourly Demand Profile**
![Hourly Profile](outputs/hourly_demand_profile.png)
Demand peaks twice daily — a morning ramp around 8–9 AM and an evening peak around 6–7 PM — with a deep overnight trough between midnight and 5 AM.

**Weekday vs Weekend Demand**
![Weekday vs Weekend](outputs/Weekday%20vs%20Weekend%20Demand%20Pattern.png)
Weekday demand is noticeably higher than weekends, reflecting the dominant role of industrial and commercial activity in shaping overall grid load.

---

### Generation Analysis

**Yearly Generation Mix (Nuclear / Fossil / Renewable)**
![Generation Mix](outputs/yearly_generation_mix.png)
Renewable generation has grown steadily while nuclear output dropped sharply after Germany's final phase-out in April 2023, with fossil fuels partially filling the gap.

**Renewable Generation Breakdown by Source**
![Renewable Breakdown](outputs/renewable_generation_breakdown.png)
Wind (onshore and offshore) dominates the renewable mix, with solar contributing a growing share — biomass and hydro remain relatively stable year over year.

**Seasonal Wind & Solar Pattern**
![Seasonal Wind Solar](outputs/seasonal_wind_solar_pattern.png)
Solar and wind are complementary seasonal resources — solar peaks in summer while wind is strongest in winter, together providing more balanced year-round coverage.

**Renewable Share Over Years**
![Renewable Share](outputs/renewable_share_over_years.png)
The renewable share has grown consistently, approaching and at times exceeding 60% of total generation — a sign of Germany's accelerating energy transition (Energiewende).

**Monthly Renewable Generation**
![Monthly Renewables](outputs/monthly_renewable_generation.png)
Total renewable output is highest in the winter-to-spring transition (February–May), driven by strong wind combined with rising solar output as days lengthen.

---

### Residual Load Analysis

**Residual Load Time Series**
![Residual Load Time Series](outputs/residual_load_time_series.png)
Residual load has been declining over the years and increasingly dips into negative territory, meaning renewables are producing more than total demand during certain hours.

**Duck Curve — High Renewable Day**
![Duck Curve High RE](outputs/duck_curve_high_RE.png)
On high-renewable days, solar generation causes a deep midday dip in residual load — the classic "duck curve" shape — requiring fast-ramping dispatchable plants in the evening.

**Duck Curve — Low Renewable Day**
![Duck Curve Low RE](outputs/duck_curve_low_RE.png)
On low-renewable days, residual load closely tracks total demand, highlighting the continued dependence on conventional generation when wind and solar output is low.

**Residual Load Distribution**
![Residual Distribution](outputs/residual_load_distribution.png)
The distribution is centered around 30,000–40,000 MWh with a notable left tail below zero, showing that negative residual load — once rare — is becoming a regular occurrence.

**Negative Residual Load Hours per Year**
![Negative Residual Hours](outputs/negative_residual_load_hours_per_year.png)
The number of hours with negative residual load has grown each year, indicating that grid flexibility, storage, and export capacity are becoming increasingly critical.

**Residual Load Duration Curve**
![Duration Curve](outputs/residual_load_duration_curve.png)
The duration curve shows that very high residual load persists for only a small fraction of the year, while a growing share of hours sit near or below zero — underscoring the need for flexible backup capacity.

**Residual Load Ramping Distribution**
![Ramping](outputs/residual_load_ramping_distribution.png)
Most hour-to-hour changes in residual load are small, but the tails reveal significant ramp events — particularly in the evening when solar drops off and demand rises simultaneously.

---

## Project Structure

```
├── Deutsche Strom Analyse.py        # Main analysis script
├── data/
│   ├── Electricity Generation.csv
│   ├── Electricity Consumption.csv
│   └── Final_df_Deutsche Strom Analysis.csv
└── outputs/                         # All generated charts (PNG)
```

---

## Data Source

Electricity generation and consumption data from [SMARD](https://www.smard.de/) (Strommarktdaten), the German Federal Network Agency's (Bundesnetzagentur) official energy market data platform.
