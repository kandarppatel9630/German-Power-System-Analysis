# -----------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Step 1 - Defining File paths
# -----------------------------
GEN_FILE = Path("data/Electricity Generation.csv")
CON_FILE = Path("data/Electricity Consumption.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Step 2 - Loading the dataset
# -----------------------------
def load_data():
    gen = pd.read_csv(GEN_FILE, sep=";")
    con = pd.read_csv(CON_FILE, sep=";")
    return gen, con

# -----------------------------
# Step 3 Convert the date columns to real datetime format.
# -----------------------------
def convert_timestamps(gen, con):
    gen["Start date"] = pd.to_datetime(gen["Start date"])
    gen["End date"] = pd.to_datetime(gen["End date"])

    con["Start date"] = pd.to_datetime(con["Start date"])
    con["End date"] = pd.to_datetime(con["End date"])

    return gen, con

# -----------------------------
# Step 4 - Cleaning and converting columns into numeric data 
# -----------------------------
def clean_numeric_columns(df):
    for col in df.columns:
        if col not in ["Start date", "End date"]:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)  # remove thousand separator
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

# -----------------------------
# Step 5 - Column renaming
# -----------------------------
def rename_columns(gen, con):
    gen = gen.rename(columns={
        "Start date": "timestamp",
        "Biomass [MWh] Calculated resolutions": "biomass",
        "Hydropower [MWh] Calculated resolutions": "hydropower",
        "Wind offshore [MWh] Calculated resolutions": "wind_offshore",
        "Wind onshore [MWh] Calculated resolutions": "wind_onshore",
        "Photovoltaics [MWh] Calculated resolutions": "solar",
        "Other renewable [MWh] Calculated resolutions": "other_renewable",
        "Nuclear [MWh] Calculated resolutions": "nuclear",
        "Lignite [MWh] Calculated resolutions": "lignite",
        "Hard coal [MWh] Calculated resolutions": "hard_coal",
        "Fossil gas [MWh] Calculated resolutions": "fossil_gas",
        "Hydro pumped storage [MWh] Calculated resolutions": "pumped_storage_gen",
        "Other conventional [MWh] Calculated resolutions": "other_conventional"
    })

    con = con.rename(columns={
        "Start date": "timestamp",
        "grid load [MWh] Calculated resolutions": "grid_load",
        "Grid load incl. hydro pumped storage [MWh] Calculated resolutions": "grid_load_incl_pumped_storage",
        "Hydro pumped storage [MWh] Calculated resolutions": "pumped_storage_load",
        "Residual load [MWh] Calculated resolutions": "residual_load"
    })

    return gen, con

# -----------------------------
# Step 6 - Dropping unnecessary columns + Data merge
# -----------------------------
#def merge_data(gen, con):
#    gen = gen.drop(columns=["End date"])
#    con = con.drop(columns=["End date"])

#    df = pd.merge(gen, con, on="timestamp", how="inner")
#    return df

# Step 6 - Dropping unnecessary columns + Data merge
def merge_data(gen, con):
    
    # Remove DST duplicates
    gen = gen.drop_duplicates(subset="timestamp", keep="first")
    con = con.drop_duplicates(subset="timestamp", keep="first")
    
    gen = gen.drop(columns=["End date"])
    con = con.drop(columns=["End date"])

    df = pd.merge(gen, con, on="timestamp", how="inner")
    return df

# -----------------------------
# Step 7 - Generating features
# -----------------------------
def create_features(df):
    df["nuclear"] = df["nuclear"].fillna(0)

    df["renewable_generation"] = (
        df["biomass"]
        + df["hydropower"]
        + df["wind_offshore"]
        + df["wind_onshore"]
        + df["solar"]
        + df["other_renewable"]
    )

    df["fossil_generation"] = (
        df["lignite"]
        + df["hard_coal"]
        + df["fossil_gas"]
        + df["other_conventional"]
    )

    df["total_generation"] = (
        df["renewable_generation"]
        + df["nuclear"]
        + df["fossil_generation"]
        + df["pumped_storage_gen"]
    )

    df["renewable_share_pct"] = (
        df["renewable_generation"] / df["total_generation"]
    ) * 100

    return df

# -----------------------------
# Step 8 - Generating time-based features
# -----------------------------
def add_time_features(df):
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["month_name"] = df["timestamp"].dt.month_name()
    df["hour"] = df["timestamp"].dt.hour
    df["dayofweek"] = df["timestamp"].dt.day_name()
    df["is_weekend"] = df["dayofweek"].isin(["Saturday", "Sunday"])

    return df

# -----------------------------
# Step 9 - Quick Quality check function
# -----------------------------
def inspect_data(df):
    print("\nFirst 5 rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nSummary statistics:")
    print(df.describe())

# -----------------------------
# Step 10 - Data Processing Pipeline
# -----------------------------
gen, con = load_data()
gen, con = convert_timestamps(gen, con)
gen = clean_numeric_columns(gen)
con = clean_numeric_columns(con)
gen, con = rename_columns(gen, con)
df = merge_data(gen, con)
df = create_features(df)
df = add_time_features(df)

inspect_data(df)

# -----------------------------
# Step 11 - Demand Analysis
# -----------------------------
def demand_analysis(df):
    
    # Time series
    plt.figure(figsize=(14, 5))
    plt.plot(df["timestamp"], df["grid_load"])
    plt.title("Hourly Electricity Demand in Germany (2020–2025)")
    plt.xlabel("Time")
    plt.ylabel("Grid Load [MWh]")
    plt.savefig(OUTPUT_DIR / "hourly_demand_time_series.png", dpi=300, bbox_inches="tight")
    #plt.grid(False)
    plt.show()
    
    # Yearly average demand
    yearly_demand = df.groupby("year")["grid_load"].mean()
    
    plt.figure(figsize=(8, 5))
    ax = yearly_demand.plot(kind="bar")
    
    for i, v in enumerate(yearly_demand):
        ax.text(i, v, f"{v:,.0f}", ha="center", va="bottom")
    
    plt.title("Average Electricity Demand by Year")
    plt.xlabel("Year")
    plt.ylabel("Average Grid Load [MWh]")
    
    plt.savefig(OUTPUT_DIR / "yearly_demand.png",
                dpi=300, bbox_inches="tight")
    plt.grid(False)
    plt.show()

    
    # Monthly average demand
    monthly_demand = df.groupby("month")["grid_load"].mean()

    plt.figure(figsize=(10, 5))
    monthly_demand.plot(kind="bar")

    plt.title("Average Monthly Electricity Demand")
    plt.xlabel("Month")
    plt.ylabel("Average Grid Load [MWh]")

    plt.xticks(
        ticks=range(0, 12),
        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        rotation=0
    )

    plt.savefig(OUTPUT_DIR / "monthly_demand.png",
                dpi=300, bbox_inches="tight")
    plt.grid(False)
    plt.show()
    
    # Hourly average demand
    hourly_demand = df.groupby("hour")["grid_load"].mean()
    
    plt.figure(figsize=(10, 5))
    plt.plot(hourly_demand.index, hourly_demand.values, marker="o")
    
    plt.title("Average Hourly Electricity Demand Profile")
    plt.xlabel("Hour of Day")
    plt.ylabel("Average Grid Load [MWh]")
    
    plt.xticks(range(0, 24))
    
    plt.savefig(OUTPUT_DIR / "hourly_demand_profile.png",
                dpi=300, bbox_inches="tight")
    plt.grid(True)
    plt.show()
    
    # Weekday vs Weekend pattern
    week_pattern = df.groupby("is_weekend")["grid_load"].mean()

    plt.figure(figsize=(6,4))

    week_pattern.index = ["Weekday", "Weekend"]
    ax = week_pattern.plot(kind="bar")

    for i, v in enumerate(week_pattern):
        ax.text(i, v + 200, f"{v:,.0f}", ha="center")

    plt.title("Average Electricity Demand: Weekday vs Weekend")
    plt.xlabel("")
    plt.ylabel("Average Grid Load [MWh]")
    plt.xticks(rotation=0)
    plt.savefig("Weekday vs Weekend Demand Pattern.png", dpi=300, bbox_inches="tight")
    plt.grid(False)
    plt.show()

# Plotting the Demand Analysis
demand_analysis(df)

# -----------------------------
# Step 12 - Generation Analysis
# -----------------------------
def generation_analysis(df):
    generation_mix = df.groupby("year")[["nuclear", "fossil_generation", "renewable_generation"]].sum()

    generation_mix.plot(kind="bar", figsize=(10, 6))

    plt.title("Yearly Electricity Generation Mix in Germany")
    plt.xlabel("Year")
    plt.ylabel("Total Generation [MWh]")
    plt.xticks(rotation=0)

    plt.legend(
        ["Nuclear", "Fossil Fuels", "Renewables"],
        title="Generation Type",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.grid(False)

    plt.savefig(OUTPUT_DIR / "yearly_generation_mix.png",
                dpi=300, bbox_inches="tight")

    plt.show()
    
    # Renewable generation breakdown
    renewable_sources = df.groupby("year")[[
        "wind_onshore",
        "wind_offshore",
        "solar",
        "hydropower",
        "biomass",
        "other_renewable"
    ]].sum()
    
    renewable_sources.plot(kind="bar", stacked=True, figsize=(12, 6))
    
    plt.title("Renewable Electricity Generation by Source")
    plt.xlabel("Year")
    plt.ylabel("Total Generation [MWh]")
    plt.xticks(rotation=0)
    
    plt.legend(
        title="Renewable Source",
        bbox_to_anchor=(1, 0.5),
        loc="center left"
    )
    
    plt.grid(False)
    
    plt.savefig(OUTPUT_DIR / "renewable_generation_breakdown.png",
                dpi=300, bbox_inches="tight")
    
    plt.show()
    
    # Seasonal wind vs solar generation pattern
    monthly_renewables = df.groupby("month")[["solar", "wind_onshore", "wind_offshore"]].mean()
    
    monthly_renewables.plot(figsize=(10, 5), marker="o")
    
    plt.title("Seasonal Pattern of Wind and Solar Generation in Germany")
    plt.xlabel("Month")
    plt.ylabel("Average Generation [MWh]")
    
    plt.xticks(
        ticks=range(1, 13),
        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        rotation=0
    )
    
    plt.legend(
        ["Solar", "Wind Onshore", "Wind Offshore"],
        title="Generation Source",
        bbox_to_anchor=(1, 0.5),
        loc="center left"
    )
    
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    
    plt.savefig(OUTPUT_DIR / "seasonal_wind_solar_pattern.png",
                dpi=300, bbox_inches="tight")
    
    plt.show()
    
    # Renewable share over years
    renewable_share = df.groupby("year")["renewable_share_pct"].mean()
    
    plt.figure(figsize=(8, 5))
    plt.plot(renewable_share.index, renewable_share.values, marker="o")
    
    plt.title("Average Renewable Share in Electricity Generation")
    plt.xlabel("Year")
    plt.ylabel("Renewable Share [%]")
    
    plt.xticks(renewable_share.index)
    
    #plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.grid(True)
    
    plt.savefig(OUTPUT_DIR / "renewable_share_over_years.png",
                dpi=300, bbox_inches="tight")
    
    plt.show()
    
    # Monthly average renewable generation
    monthly_total_renewables = df.groupby("month")["renewable_generation"].mean()
    
    plt.figure(figsize=(8, 5))
    plt.plot(monthly_total_renewables.index,
             monthly_total_renewables.values,
             marker="o")
    
    plt.title("Seasonal Pattern of Total Renewable Generation")
    plt.xlabel("Month")
    plt.ylabel("Average Renewable Generation [MWh]")
    
    plt.xticks(
        ticks=range(1, 13),
        labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    )
    
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    
    plt.savefig(OUTPUT_DIR / "monthly_renewable_generation.png",
                dpi=300, bbox_inches="tight")
    
    plt.show()

# Plotting the Generation Analysis
generation_analysis(df)


# -----------------------------
# Step 13 - Residual Load Analysis
# -----------------------------
def residual_analysis(df):
    # Residual load time series
    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df["residual_load"])
    
    plt.title("Residual Load Time Series in Germany (2020–2025)")
    plt.xlabel("Time")
    plt.ylabel("Residual Load [MWh]")
    
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    
    plt.savefig(OUTPUT_DIR / "residual_load_time_series.png",
                dpi=300, bbox_inches="tight")
    
    plt.show()
    
    # Duck curve analysis (Multiple days)
    days = ["2023-06-11", "2023-07-28"]
    
    titles = [
        "High Renewable Day (Negative Residual Load)",
        "Lower Renewable Day (No Negative Residual Load)"
    ]
    
    filenames = [
        "duck_curve_high_RE.png",
        "duck_curve_low_RE.png"
    ]
    
    for day, title, fname in zip(days, titles, filenames):
    
        sample_day = df[df["timestamp"].dt.date == pd.to_datetime(day).date()]
    
        plt.figure(figsize=(10, 5))
    
        plt.plot(sample_day["hour"], sample_day["grid_load"], label="Demand")
        plt.plot(sample_day["hour"], sample_day["solar"], label="Solar")
        plt.plot(sample_day["hour"], sample_day["residual_load"], label="Residual Load")
    
        plt.fill_between(sample_day["hour"],
                         sample_day["residual_load"],
                         alpha=0.2)
    
        plt.title(title)
        plt.xlabel("Hour")
        plt.ylabel("Power [MWh]")
        plt.legend()
        plt.grid(True)
        plt.axhline(0, linestyle='--', linewidth=1)
    
        plt.tight_layout()
    
        plt.savefig(OUTPUT_DIR / fname, dpi=300, bbox_inches="tight")
        plt.show()

    # Residual load distribution
    plt.figure(figsize=(8, 5))
    plt.hist(df["residual_load"], bins=50, edgecolor="black")
    
    plt.axvline(0, linestyle="--", label="Zero Residual Load")
    
    plt.title("Distribution of Residual Load (2020–2025)")
    plt.xlabel("Residual Load [MWh]")
    plt.ylabel("Frequency")
    
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    
    plt.savefig(OUTPUT_DIR / "residual_load_distribution.png",
                dpi=300, bbox_inches="tight")
    
    plt.show()

    # Negative residual load analysis
    negative_hours = df[df["residual_load"] < 0]

    print("Total negative residual load hours:", len(negative_hours))

    percentage_negative = (len(negative_hours) / len(df)) * 100
    print(f"Percentage of negative residual load hours: {percentage_negative:.2f}%")

    negative_hours_per_year = negative_hours.groupby("year").size()

    plt.figure(figsize=(8, 5))
    negative_hours_per_year.plot(kind="bar")

    plt.title("Negative Residual Load Hours per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Hours")
    plt.xticks(rotation=0)

    plt.grid(False)

    plt.savefig(OUTPUT_DIR / "negative_residual_load_hours_per_year.png",
                dpi=300, bbox_inches="tight")

    plt.show()

    # Residual load duration curve
    sorted_residual = df["residual_load"].sort_values(ascending=False).reset_index(drop=True)

    plt.figure(figsize=(10, 5))
    plt.plot(sorted_residual)

    plt.title("Residual Load Duration Curve")
    plt.xlabel("Hour Rank")
    plt.ylabel("Residual Load [MWh]")

    plt.grid(axis="y", linestyle="--", alpha=0.3)

    plt.savefig(OUTPUT_DIR / "residual_load_duration_curve.png",
                dpi=300, bbox_inches="tight")

    plt.show()

    # Ramping analysis
    df["ramp"] = df["residual_load"].diff()

    plt.figure(figsize=(8, 5))
    plt.hist(df["ramp"].dropna(), bins=50, edgecolor="black")

    plt.title("Residual Load Ramping Distribution")
    plt.xlabel("Change in Residual Load [MWh]")
    plt.ylabel("Frequency")

    plt.grid(axis="y", linestyle="--", alpha=0.3)

    plt.savefig(OUTPUT_DIR / "residual_load_ramping_distribution.png",
                dpi=300, bbox_inches="tight")

    plt.show()

# Plotting the Residual Load Analysis
residual_analysis(df)

# -----------------------------
# Step 14 - Key Performance Indicators
# -----------------------------
def print_kpis(df):
    print("\n--- Key Performance Indicators ---\n")

    #total_demand = df["grid_load"].sum()
    avg_demand = df["grid_load"].mean()

    avg_renewable_share = df["renewable_share_pct"].mean()

    negative_hours = len(df[df["residual_load"] < 0])
    negative_percentage = (negative_hours / len(df)) * 100

    max_residual = df["residual_load"].max()
    min_residual = df["residual_load"].min()

    #print(f"Total Electricity Demand: {total_demand:,.0f} MWh")
    print(f"Average Hourly Electricity Demand: {avg_demand:,.0f} MWh")

    print(f"\nAverage Renewable Share: {avg_renewable_share:.2f} %")

    print(f"\nNegative Residual Load Hours: {negative_hours}")
    print(f"Percentage of Negative Residual Load: {negative_percentage:.2f} %")

    print(f"\nMaximum Residual Load: {max_residual:,.0f} MWh")
    print(f"Minimum Residual Load: {min_residual:,.0f} MWh")

# Extracting KPIs
print_kpis(df)

# Saving the final Dataframe into csv
df.to_csv("outputs/Final_df_Deutsche Strom Analysis.csv", index=False)




