# German Power System Analysis
### Demand, Generation & Residual Load (2020–2025)

An end-to-end analysis of Germany's electricity system using hourly data from the ENTSO-E Transparency Platform. The project explores demand patterns, renewable generation trends, and residual load dynamics — key concepts for understanding modern power grids with high renewable penetration.

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

**Average Yearly Demand**
![Yearly Demand](outputs/yearly_demand.png)

**Average Monthly Demand**
![Monthly Demand](outputs/monthly_demand.png)

**Average Hourly Demand Profile**
![Hourly Profile](outputs/hourly_demand_profile.png)

**Weekday vs Weekend Demand**
![Weekday vs Weekend](outputs/Weekday%20vs%20Weekend%20Demand%20Pattern.png)

---

### Generation Analysis

**Yearly Generation Mix (Nuclear / Fossil / Renewable)**
![Generation Mix](outputs/yearly_generation_mix.png)

**Renewable Generation Breakdown by Source**
![Renewable Breakdown](outputs/renewable_generation_breakdown.png)

**Seasonal Wind & Solar Pattern**
![Seasonal Wind Solar](outputs/seasonal_wind_solar_pattern.png)

**Renewable Share Over Years**
![Renewable Share](outputs/renewable_share_over_years.png)

**Monthly Renewable Generation**
![Monthly Renewables](outputs/monthly_renewable_generation.png)

---

### Residual Load Analysis

**Residual Load Time Series**
![Residual Load Time Series](outputs/residual_load_time_series.png)

**Duck Curve — High Renewable Day**
![Duck Curve High RE](outputs/duck_curve_high_RE.png)

**Duck Curve — Low Renewable Day**
![Duck Curve Low RE](outputs/duck_curve_low_RE.png)

**Residual Load Distribution**
![Residual Distribution](outputs/residual_load_distribution.png)

**Negative Residual Load Hours per Year**
![Negative Residual Hours](outputs/negative_residual_load_hours_per_year.png)

**Residual Load Duration Curve**
![Duration Curve](outputs/residual_load_duration_curve.png)

**Residual Load Ramping Distribution**
![Ramping](outputs/residual_load_ramping_distribution.png)

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

---

## Usage

```bash
python "Deutsche Strom Analyse.py"
```

Charts are saved automatically to the `outputs/` directory.

---

## Data Source

Electricity generation and consumption data from the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/), covering Germany's bidding zone.
