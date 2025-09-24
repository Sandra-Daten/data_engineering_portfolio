from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, regexp_replace, when
from pyspark.sql.types import DoubleType

# Kreiranje Spark sesije
spark = SparkSession.builder.appName("global-airpollution").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Učitavanje CSV-a
df = spark.read.csv(
    "/data/air_pollution_new.csv",
    sep=",",
    header=True,
    inferSchema=False  # pazimo, da Spark ne pravi nevidljive tipove
)

# # Očisti nazive kolona od whitespace karaktera
# df = df.toDF(*[c.strip() for c in df.columns])

# # Proveri nazive i tipove kolona
# print("Kolone i tipovi pre cast:", df.dtypes, flush=True)
# df.show(5, truncate=False)

# Lista godina
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]

# Čišćenje vrednosti: whitespace i nebrojčani karakteri
for year in years:
    df = df.withColumn(
        f"{year}",
        trim(col(f"{year}")).cast(DoubleType())
    )

# # Proveri da li je cast uspeo
# print("\nSchema posle cast:", df.dtypes, flush=True)
df.printSchema()
df.show(5, truncate=False)

# Dodavanje AQI_Status kolona
for year in years:
    df = df.withColumn(
        f"AQI_Status_{year}",
        when(col(f"{year}") <= 100, "Moderate")
        .when((col(f"{year}") > 100) & (col(f"{year}") <= 150), "Unhealthy for Sensitive Groups")
        .when((col(f"{year}") > 150) & (col(f"{year}") <= 200), "Unhealthy")
        .when((col(f"{year}") > 200) & (col(f"{year}") <= 300), "Very Unhealthy")
        .otherwise("Hazardous")
    )

# Forsiraj izvršavanje da Spark materializuje DataFrame
df.cache().count()
print(f"Ukupno redova: {df.count()}")

df.describe().show()

# Prikaz finalnog DataFrame-a sa statusom
print("=== Finalni DataFrame sa AQI_Status ===")
df.show(10, truncate=False)

# spark.stop()
