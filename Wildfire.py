import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


# 1. Read the CSV directly from the URL
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
df =pd.read_csv(url)
print ("Data read into a pandas dataframe!")

# 2. Peek at the data
print(df.head())
print(df.dtypes)

# 3. Convert Date to datetime, and create Year & Month columns
df["Date"]=pd.to_datetime(df["Date"])
df["Year"]=df["Date"].dt.year
df["Month"]=df["Date"].dt.month
# Updated column list
print(df.columns)

#  TASK 1.1 – Line chart: average estimated fire area over time
avg_area_by_year = df.groupby("Year")["Estimated_fire_area"].mean()
plt.figure(figsize = (10,5))
avg_area_by_year.plot(kind="line", marker="o")
plt.title("Average estimated fire area per year")
plt.xlabel("Year")
plt.ylabel("Average Estimated Fire Area (km²)")
plt.grid(True)
plt.show()


# ✅ TASK 1.2 – Estimated fire area by month (for Year: 2010–2013)

# A. Create a mask (filter) to keep only the years 2010–2013
mask=(df["Year"]>=2010)&(df["Year"]<=2013)
df_2010_2013 = df[mask]

# B. Group by Year and Month and compute average fire area
avg_area_by_year= (df_2010_2013.groupby(["Year","Month"])["Estimated_fire_area"].mean().reset_index())

#Plot
plt.figure(figsize = (10,5))
for year in sorted(df_2010_2013["Year"].unique()):
    subset=avg_area_by_year[avg_area_by_year["Year"]==year]
    plt.plot(subset["Month"], subset["Estimated_fire_area"], marker="o",label=str(year))

plt.title("Average Estimated Fire Area by Month (2010–2013)")
plt.xlabel("Month")
plt.ylabel("Average Estimated Fire Area (km²)")
plt.legend(title="Year")
plt.xticks(range(1, 13),
           ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])

plt.grid(True)
plt.tight_layout()
plt.show()


# ✅ TASK 1.3 – Barplot: mean fire brightness across regions (Seaborn)
print(df["Region"].unique())

# TASK 1.3
plt.figure(figsize=(8, 5))
sns.barplot(
    data=df,
    x="Region",
    y="Mean_estimated_fire_brightness",
    estimator=np.mean,
    ci=None
)
plt.title("Mean Estimated Fire Brightness by Region")
plt.xlabel("Region")
plt.ylabel("Mean Fire Brightness (K)")
plt.tight_layout()
plt.show()


#✅ TASK 1.4 – Pie chart: total pixel count by region
region_counts = df.groupby("Region")["Count"].sum()

#B. Create a pie chart
plt.figure(figsize = (6,6))

region_counts.plot(
    kind="pie",
    autopct="%1.1f%%", # Show percentages on slices
    startangle=90,     # rotate so the first slice starts at the top
)

# C. Add title
plt.title("Share of Fire Pixels (Count) by Region")
plt.tight_layout()
plt.show()


# ✅ TASK 1.5 – Better pie chart with legend instead of overlapping labels


plt.figure(figsize=(6, 6))
plt.pie(region_counts, startangle=90)

plt.title("Share of Fire Pixels (Count) by Region")

# Build legend entries: (Region, percentage)
legend_labels = [
    (i, round(k / region_counts.sum() * 100, 2))
    for i, k in zip(region_counts.index, region_counts)
]

plt.legend(
    legend_labels,
    title="Region, %",
    loc="best"
)
plt.tight_layout()
plt.show()

#✅ TASK 1.6 – Histogram of mean estimated fire brightness (Matplotlib)

plt.figure(figsize=(8, 5))
plt.hist(df["Mean_estimated_fire_brightness"], bins=30)
plt.title("Histogram of Mean Estimated Fire Brightness")
plt.xlabel("Mean Estimated Fire Brightness (K)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

#✅ TASK 1.7 – Distribution of brightness across regions (Seaborn + hue)

# TASK 1.7 - version 1
plt.figure(figsize=(8, 5))
sns.histplot(
    data=df,
    x="Mean_estimated_fire_brightness",
    hue="Region",
    bins=30,
)
plt.title("Distribution of Mean Fire Brightness by Region")
plt.xlabel("Mean Estimated Fire Brightness (K)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# TASK 1.7 - version 2 (stacked)
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df,
    x="Mean_estimated_fire_brightness",
    hue="Region",
    bins=30,
    multiple="stack"
)
plt.title("Stacked Distribution of Mean Fire Brightness by Region")
plt.xlabel("Mean Estimated Fire Brightness (K)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()


# ✅ TASK 1.8 – Scatter plot: radiative power vs confidence

# TASK 1.8
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=df,
    x="Mean_estimated_fire_radiative_power",
    y="Mean_confidence",
    alpha=0.5
)
plt.title("Radiative Power vs Confidence")
plt.xlabel("Mean Estimated Fire Radiative Power (MW)")
plt.ylabel("Mean Confidence (%)")
plt.tight_layout()
plt.show()


# ✅ TASK 1.9 – Mark the seven regions on a map (Folium)

# TASK 1.9

region_data = {
    "region": ["NSW", "QL", "SA", "TA", "VI", "WA", "NT"],
    "Lat": [-31.8759835, -22.1646782, -30.5343665, -42.035067, -36.5986096, -25.2303005, -19.491411],
    "Lon": [147.2869493, 144.5844903, 135.6301212, 146.6366887, 144.6780052, 121.0187246, 132.550964],
}

reg = pd.DataFrame(region_data)
print(reg)

# Create a map centered on Australia
m = folium.Map(location=[-25, 135], zoom_start=4)

# Add markers
for _, row in reg.iterrows():
    folium.Marker(
        location=[row["Lat"], row["Lon"]],
        popup=row["region"]
    ).add_to(m)

# Save the map to an HTML file and open it in a browser
m.save("australia_wildfire_regions.html")
print("Map saved to australia_wildfire_regions.html")
