# SAMOSTALNA VEZBA: CISCENJE I PRIPREMA CSV-A U PYTHON-U
# pripremiti odgovarajuce data type-ove
# preminovati kolone
# dodati nove kolone sa statusom za svaki nivo zagadjenja



import pandas as pd
import numpy as np

# Učitaj CSV
df = pd.read_csv("air_pollution_new.csv")

# Pogledaj prvih 10 redova da vidiš kako podaci izgledaju
print("=== Prvih 10 redova ===")
print(df.head(10))

print("\n=== Nazivi kolona ===")
print(df.columns)

print("\n=== Tipovi podataka ===")
print(df.dtypes)

print("\n=== Statistika numeričkih kolona ===")
print(df.describe())  # daje count, mean, min, max, std...

# Prve dve kolone u string (već su object, ali osiguravamo)
df['city'] = df['city'].astype(str)
df['country'] = df['country'].astype(str)

# Ostale kolone (2017-2023) očisti i pretvori u float
years = [str(y) for y in range(2017, 2024)]
for y in years:
    # trim whitespace i konvertuj u float, greske -> NaN
    df[y] = df[y].astype(str).str.strip()  # uklanja whitespace
    df[y] = pd.to_numeric(df[y], errors='coerce')  # non-numerics -> NaN

print("\n=== Tipovi podataka_2 ===")
print(df.dtypes)

# --- Promeni nazive kolona ---
new_columns = ['city', 'country'] + [f"AQI_{y}" for y in range(2017, 2024)]
df.columns = new_columns

print(df.dtypes)
print(df.head(5))

# Dodaj AQI_Status kolone
for y in range(2017, 2024):
    col_name = f"AQI_{y}"  # ovo je sada pravi naziv kolone
    conditions = [
        (df[col_name] <= 100),
        (df[col_name] > 100) & (df[col_name] <= 150),
        (df[col_name] > 150) & (df[col_name] <= 200),
        (df[col_name] > 200) & (df[col_name] <= 300),
        (df[col_name] > 300)
    ]
    choices = [
        "Moderate",
        "Unhealthy for Sensitive Groups",
        "Unhealthy",
        "Very Unhealthy",
        "Hazardous"
    ]
    df[f"Status_{y}"] = np.select(conditions, choices, default="Unknown")

print("\n")
print(df.head(3))

# Preuredi raspored kolona
cols = ["city", "country"]

for y in range(2017, 2024):
    cols.append(f"AQI_{y}"),
    cols.append(f"Status_{y}")

df = df[cols]

print("\n", df.head(15))

# Ispitati da li se u koloni Status_2017 nalazi vrednost "Hazardous"
# hazardous_2017 = df[df["Status_2017"]=="Hazardous"]
# print(hazardous_2017[["city", "country", "Status_2017"]])


# ----Svi jedinstveni statusi za 2017
print(df['Status_2017'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2017'].value_counts())


# ----Svi jedinstveni statusi za 2018
print(df['Status_2018'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2018'].value_counts())


# ----Svi jedinstveni statusi za 2019
print(df['Status_2019'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2019'].value_counts())


# ----Svi jedinstveni statusi za 2020
print(df['Status_2020'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2020'].value_counts())


# ----Svi jedinstveni statusi za 2021
print(df['Status_2021'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2021'].value_counts())


# ----Svi jedinstveni statusi za 2022
print(df['Status_2022'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2022'].value_counts())


# ----Svi jedinstveni statusi za 2023
print(df['Status_2023'].unique())

# Koliko puta se svaka vrednost pojavljuje
print(df['Status_2023'].value_counts())
