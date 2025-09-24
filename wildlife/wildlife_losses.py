# --------------------------------------------------------------------------------------------------------- #
# Analiza podataka o gubitku divljači u lovu i saobraćaju na teritorije Republiek Srbije za period 2011-2023.

# ------------------------- ZADATAK_1. deo: Priprema DataFrame-a i osnovna analiza ------------------------ #



from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window

# Funkcija za smanjenje logova Spark/Java
def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

# Kreiranje Spark sesije
spark = SparkSession \
    .builder \
    .appName("wildlifeLosses") \
    .getOrCreate()

quiet_logs(spark)


# ----------------- Učitavanje CSV fajlova ----------------- #

df_hunting = spark.read.csv("/opt/wildlife/wildlife_hunting_losses.csv", sep=";", header=True, encoding="UTF-8", inferSchema=True)
df_traffic = spark.read.csv("/opt/wildlife/wildlife_traffic_losses.csv", sep=";", header=True, encoding="UTF-8", inferSchema=True)

# df_hunting.printSchema()
# df_traffic.printSchema()

# Spajanje oba DataFrame-a u jedan
df = df_hunting.join(
    df_traffic.select("IDVrstaDivljaci","god","vrednost","Indikator"),
    on = ["IDVrstaDivljaci","god"],
    how="left"
    ).withColumnRenamed("vrednost","vrednost_traffic").withColumnRenamed("Indikator", "Indikator_traffic")

# df.show()
# print(df.columns)
# print(len(df.columns))

# Preimenovanje kolona radi preglednosti
new_columns = [
    'ID_VrstaDivljaci', 'God', 'ID_Indikator', 'ID_Ter', 'N_Ter', 
    'N_VrstaDivljaci', 'Mes', 'Vrednost_Lov', 'ID_JedinicaMere', 
    'N_JedinicaMere', 'N_Izvori', 'Indikator_Lov', 
    'ID_StatusPodatka', 'N_StatusPodatka', 'Vrednost_Saobraćaj', 'Indikator_Saobraćaj'
]
df=df.toDF(*new_columns)
# df.printSchema()
print("INITIAL DATAFRAME:")
df.show()

# ----------------- Podizanje DataFrame-a na HDFS ----------------- #

df.write.csv(
    "hdfs://namenode:9000/user/sandra/wildlife_losses_combined",
    header="True",
    mode="overwrite"
    )

# ----------------- Pregled podataka ----------------- #

# show(n) vs. take(n) 

# Ispisati prvih 5 redova:
##      * kao formatiranu tabelu: --> koristi se .show(n)
print("FIRST 5 ROWS:")
df.show(5)

##      * kao Row objekte: --> koristi se .take(n)
# for row in df.take(5):
#     print(row)

# Ispisati sve različite vrste divljači
print("WILDLIFE SPECIES:")
df.select("N_VrstaDivljaci").distinct().show(50, truncate=False)

# Ispisati koliko ima vrsta divljači
broj_divljaci = df.select("N_VrstaDivljaci").distinct().count()
print("NUMBER OF WILDLIFE:")
print(broj_divljaci)




# --------------------------------------------------------------------------------------------------------- #
# ------------------------------------ ZADATAK_2. deo: Analiza po godini ---------------------------------- #


# Vrste sa > 1000 gubitaka u lovu 2015.
hunting_1000 = df.select("N_VrstaDivljaci", "God", "Vrednost_Lov").where((col("Vrednost_Lov") > 1000) & (col("God") == 2015))
print("HUNTING LOSSES > 1000:")
hunting_1000.show(truncate = False)


# Vrste sa > 100 gubitaka u saobraćaju 2015.
traffic_100 = df.select("N_VrstaDivljaci", "God", "Vrednost_Saobraćaj").where((col("Vrednost_Saobraćaj") > 100) & (col("God") == 2015))
print("TRAFFIC LOSSES > 100:")
traffic_100.show(truncate = False)

# --------------- Window. --------------- #

# Top 5 divljači sa najvećim ukupnim gubicima po godini
df = df.withColumn("Vrednost_Total", col("Vrednost_Lov") + col("Vrednost_Saobraćaj"))
window_by_year = Window.partitionBy("God").orderBy(col("Vrednost_Total").desc())
df_with_rank = df.withColumn("row_number", row_number().over(window_by_year))
# df.select("God").distinct().show()
print("TOP 5_BY YEAR:")
df_top5_by_year = df_with_rank.filter(col("row_number") <= 5).show(truncate=False)

# Top 5 divljači sa najvećim ukupnim gubicima globalno
# df = df.withColumn("Vrednost_Total", col("Vrednost_Lov") + col("Vrednost_Saobraćaj"))
window_global = Window.orderBy(col("Vrednost_Total").desc())
df_top_global = df.withColumn("ID", row_number().over(window_global))
df_top5_global = df_top_global.filter(col("ID") <= 5)  # pravi novi df sa samo tim redovima
print("TOP 5_GLOBAL:")
df_top5_global.show(truncate=False)

# Divljači sa najvećim gubicima u svakoj godini
#   --> Filtrirati samo red sa row_number = 1, ovo vraća najveći gubitak po godini
df_highest_losses = df_with_rank.filter(col("row_number") == 1).select("N_VrstaDivljaci", "God", "Vrednost_Total")
df_highest_losses.show(truncate=False)


# --------------- pivot() --------------- #

# Pivot tabela gubitaka po godini i tipu gubitka

# priprema za pivotrianje 
df = df.withColumnRenamed("Vrednost_Saobraćaj", "Vrednost_Saobracaj") # expr ne trpi ć, č, đ, š
df_long = df.select(
    "N_VrstaDivljaci", "God",
    expr("stack(2, 'Gub_u_Lovu', CAST(Vrednost_Lov AS double), 'Gub_u_Saobracaju', CAST(Vrednost_Saobracaj AS DOUBLE)) as (Tip_gubitka, Kol_gubitka)")
)
df_long.show(truncate=False)

# napravi novu kolonu koja kombinuje godinu i tip gubitka
df_long = df_long.withColumn("God_Tip", concat_ws("_", col("God"), col("Tip_gubitka")))
df_long.show(truncate=False)

# pivotiranje tabele
df_pivot = df_long.groupBy("N_VrstaDivljaci") \
    .pivot("God_Tip") \
    .agg(expr("first(Kol_gubitka)"))

print("PIVOTED TABLE:")
df_pivot.show(truncate=False)


# --------------- lag() --------------- #

# Divljač sa najvećim skokom u broju gubitaka (u lovu) u odnosu na prethodnu godinu
window = Window.partitionBy("N_VrstaDivljaci").orderBy("God")

df_with_diff = df.withColumn("Prev_Vrednost_lov", lag("Vrednost_lov").over(window)) \
                 .withColumn("Razlika", col("Vrednost_lov") - col("Prev_Vrednost_lov"))

df_with_max = df_with_diff.orderBy(col("Razlika").desc()).limit(1)

print("LARGEST YEAR-OVER-YEAR HUNTING LOSS:")
df_with_max.show(truncate=False)