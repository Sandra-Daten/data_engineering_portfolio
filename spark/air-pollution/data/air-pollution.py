# --------------------------------------------------------------------------------------------------------- #
#                           Analysis of global air pollution data from 2017 to 2023
# --------------------------------------------------------------------------------------------------------- #



# Function to reduce Spark/Java logs
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType

def quiet_logs(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)

# 1. Create Spark Session
spark=SparkSession.builder.appName("global-airpollution").getOrCreate()

quiet_logs(spark)

# 2. Read CSV file into Spark DataFrame
df = spark.read.csv(
    "/data/air-pollution/air_pollution_new.csv", 
    sep=",", 
    header=True, 
    inferSchema=True
    )



# --------------- PREPARE DATAFRAME FOR ANALYSIS --------------- #



# 3. Print schema
print("Print df Schema:")
df.printSchema()

# 4. Show first 10 rows
print("Show the first 10 rows:")
df.show(10, truncate=False)

# 5. Change the data type for years columns
df=(df
.withColumn("AQI_2017", col("2017").cast(DoubleType()))
.withColumn("AQI_2018", col("2018").cast(DoubleType()))
.withColumn("AQI_2019", col("2019").cast(DoubleType()))
.withColumn("AQI_2020", col("2020").cast(DoubleType()))
.withColumn("AQI_2021", col("2021").cast(DoubleType()))
.withColumn("AQI_2022", col("2022").cast(DoubleType()))
.withColumn("AQI_2023", col("2023").cast(DoubleType()))
)

df = (df
.drop("2017")
.drop("2018")
.drop("2019")
.drop("2020")
.drop("2021")
.drop("2022")
.drop("2023")
)

# df.show()
print("Print Schema with data type changed:")
df.printSchema()

# 6. Add air quality categorization columns for each year
years = ["AQI_2017", "AQI_2018", "AQI_2019", "AQI_2020", "AQI_2021", "AQI_2022", "AQI_2023"]
for y in years:
    df = df.withColumn(
        f"Status_{y}",
        when((col(f"{y}") <= 100), "Moderate")
        .when((col(f"{y}") > 100) & (col(f"{y}") <= 150), "Unhealthy for Sensitive Groups")
        .when((col(f"{y}") > 150) & (col(f"{y}") <= 200), "Unhealthy")
        .when((col(f"{y}") > 200) & (col(f"{y}") <= 300), "Very unhealthy")
        .otherwise("Hazardous")
    )
print("Air quality categorizations columns added:")
df.show(truncate=False)

# 7. Rename Status columns to remove 'AQI' from column names
print(df.columns)
new_columens = ['city', 'country', 'AQI_2017', 'AQI_2018', 'AQI_2019', 'AQI_2020', 'AQI_2021', 'AQI_2022', 'AQI_2023', 'Status_2017', 'Status_2018', 'Status_2019', 'Status_2020', 'Status_2021', 'Status_2022', 'Status_2023']
df = df.toDF(*new_columens)
print("Renamed Status columns:")
df.show()

# # 8. Reorganize columns order --> I quit this idea at the end.
# cols = ["city", "country"]

# for y in range(2017, 2024):
#     cols.append(f"AQI_{y}")
#     cols.append(f"Status_{y}")

# # 9. Apply a new columns' organization
# df = df.select(cols)
# df.show()



# --------------- MAKE SURE WHERE THE DATAFRAME IS --------------- #



# 10. Check where Spark writes the data
print("Default filesystem:", spark._jsc.hadoopConfiguration().get("fs.defaultFS"))

# 11. Save transformed df in Parquet format on HDFS
df.write.mode("overwrite").parquet("/user/sandra/air_pollution/processed") 

df.write.mode("overwrite").parquet("hdfs://namenode:9000/user/sandra/air_pollution/processed") # before this, Spark had written data on local mashine 

print("If data exist in Parquet format on HDFS, show data frame as df2:")
df2 = spark.read.parquet("hdfs://namenode:9000/user/sandra/air_pollution/processed")
df2.show()



# --------------- ANALYTICAL TASKS --------------- #



# 12. Show all unique countries
df_all_countries = df.select("country").distinct()
print("Show all unique countries")
df_all_countries.show(truncate=False)

# 13. Count how many unique countries are in df
num_all_countries = df_all_countries.count()
print("Total Number Of Countries:", num_all_countries)

# 14. Show how many cities per country there are
cities_per_country = df.groupBy("country").count()
cities_per_country = cities_per_country.withColumnRenamed("count", "num_cities")
cities_per_country = cities_per_country.orderBy("country")
print("Number of cities in each country")
cities_per_country.show()

# citiesNum_in_serbia = cities_per_country.where(col("country") == "Serbia")
# citiesNum_in_serbia.show()

# citiesNum_in_argentina = cities_per_country.where(col("country") == "Argentina")
# citiesNum_in_argentina.show()

# 15. Top 10 cities with the highest values in 2023
top10_cities_2023 = df.select("city", "AQI_2023").orderBy(col("AQI_2023").desc()).limit(10)
print("top10_cities_2023:")
top10_cities_2023.show()

## 16/17/18. Show the AQI values through the years for any city by your choice

# 1st approach - when control over the columns is needed (mainly to select particular columns from the big dataframes) 
Lahore_trend = df.select('city', 'country', 'AQI_2017', 'AQI_2018', 'AQI_2019', 'AQI_2020', 'AQI_2021', 'AQI_2022', 'AQI_2023', 'Status_2017', 'Status_2018', 'Status_2019', 'Status_2020', 'Status_2021', 'Status_2022', 'Status_2023').where(col("city") == "Lahore")
print("LahoreCity_trend: 1st pproach")
Lahore_trend.show(truncate=False)

# 2nd approach - mainly to select all columns for small DF
Lahore_trend_2 = df.filter(col("city") == "Lahore")
print("LahoreCity_trend: 2nd approach")
Lahore_trend_2.show(truncate=False)

western_balkans = df.filter((col("city") == "Novi Sad") | (col("city") == "Belgrade") | (col("city") == "Ljubljana"))
print("western_balkans_3_cities_compared:")
western_balkans.show(truncate=False)

# 19. Show cities in Serbia
cities_in_serbia = df.select("city").where(col("country") == "Serbia")
print("Cities in Serbia:")
cities_in_serbia.show()

# 20. Calculate average AQI for all cities in one country in 2023
avg_pollution_2023 = df.groupBy("country")\
                       .agg(round(avg("AQI_2023"),2).alias("avg_AQI_2023"))\
                       .orderBy(col("avg_AQI_2023").desc())
print("avg_pollution_2023:")
avg_pollution_2023.show(50, truncate=False)


# avg AQI per each city in Serbia
serbia_avg_2023 = df.filter(df.country == "Serbia")\
                    .groupBy("city") \
                    .agg(avg("AQI_2023").alias("avg_srb_2023"))
print("Serbia_avg_2023:")
serbia_avg_2023.show()

## 21. Top 5 the most polluted countries in 2023
top5_countries_2023 = df.select("country", "AQI_2023")\
              .orderBy(col("AQI_2023").desc()).limit(5)
print("top5_countries_2023")
top5_countries_2023.show()

# 22. Show the cities which AQI values are less in 2023 than in 2017: ROUND VS FORMAT_NUMBER
# air_improved = df.select("city", "AQI_2023", "AQI_2017")\
#        .where((col("AQI_2023")) < (col("AQI_2017")))\
#        .withColumn("Improvement", round(abs(col("AQI_2023") - col("AQI_2017")), 2))

# print("air_improved:")
# air_improved.show(truncate=False)

air_improved = df.select("city", "AQI_2023", "AQI_2017")\
       .where((col("AQI_2023")) < (col("AQI_2017")))\
       .withColumn("Improvement", format_number(abs(col("AQI_2023") - col("AQI_2017")), 2))

print("air_improved_2017 vs 2023:")
air_improved.show(truncate=False)



# --------------- TRANSFORMATIONAL TASKS: PIVOT & DIFFERENCE IN VALUES --------------- #



# 23. Unpivot (melt) AQI_YYYY columns in one column

#    * Pretvori kolone `2017–2023` u dve kolone:
#      * `year` (npr. 2017, 2018, ...)
#      * `pollution` (brojčana vrednost)

df_for_pivot = df.select(
    "city",
    "country",
    expr("stack(2, '2017', AQI_2017, '2023', AQI_2023) as (year, AQI)")
)
print("df for pivot:")
df_for_pivot.show()

pivoted_1 = df_for_pivot.groupBy("city").pivot("year").agg(expr("first(AQI)"))
print("pivoted_1:")
pivoted_1.show()

df_Algiers = pivoted_1.where((col("city")=="Algiers"))
print("df_Algiers:")
df_Algiers.show()

pivoted_2 = df_for_pivot.groupBy("country").pivot("year").agg(round(avg("AQI"),2))
print("pivoted_2:")
pivoted_2.show()

# 24. The biggest pollution increase per city

years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]

# A beginner approach :)
# diff_by_years = df.withColumn("diff_17/18", round(abs(col(f"AQI_{years[0]}") - col(f"AQI_{years[1]}")), 2))\
#                   .withColumn("diff_18/19", round(abs(col(f"AQI_{years[1]}") - col(f"AQI_{years[2]}")), 2))\
#                   .withColumn("diff_19/20", round(abs(col(f"AQI_{years[2]}") - col(f"AQI_{years[3]}")), 2))\
#                   .withColumn("diff_20/21", round(abs(col(f"AQI_{years[3]}") - col(f"AQI_{years[4]}")), 2))\
#                   .withColumn("diff_21/22", round(abs(col(f"AQI_{years[4]}") - col(f"AQI_{years[5]}")), 2))\
#                   .withColumn("diff_22/23", round(abs(col(f"AQI_{years[5]}") - col(f"AQI_{years[6]}")), 2))\
    
# diff_by_years.show()   

## 25. A more curious beginner approach :D
df_with_diffs = df # a copy of a df
columns_to_fix = ["AQI_2017", "AQI_2018", "AQI_2019", "AQI_2020", "AQI_2021", "AQI_2022", "AQI_2023"]
df_with_diffs = df_with_diffs.na.replace(0, None, subset=columns_to_fix)
print("df_with_diffs")
df_with_diffs.show()

for i in range(len(years)-1):
    y1 = years[i]
    y2 = years[i+1]

    df_with_diffs = df_with_diffs.withColumn(f"diff_{y1}_{y2}", round(col(f"AQI_{y2}") - col(f"AQI_{y1}"),2))

print("df_with_diffs:")
df_with_diffs.show()

# 26. Find a city with the highest increase and decrease in the period 2017-2023
# Select the columns to compare
columns_to_compare = ["diff_2017_2018", "diff_2018_2019", "diff_2019_2020", "diff_2020_2021", "diff_2021_2022", "diff_2022_2023"]

# Greatest deterioration (max_increase) and improvement (max_decrease)
df_with_max_min = df_with_diffs.withColumn("max_increase", greatest(*columns_to_compare))\
                               .withColumn("max_decrease", least(*columns_to_compare))
print("df_with_max_min:")                               
df_with_max_min.show()



# --------------- TRANSFORMATIONAL TASKS: WINDOW FUNCTIONING, VALUE DISTRIBUTION --------------- #



# 27. Top 3 cities with the highest pollution value per year
window_2017 = Window.orderBy(col("AQI_2017").desc())
df_top_global = df.select("city", "country", "AQI_2017").withColumn("ID", row_number().over(window_2017))
print("top3_cities_2017_A:") 
top3_cities_2017 = df_top_global.filter(col("ID") <= 3).show()

years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
## A beginner approach :)
# for y in years:
#     window_year = Window.orderBy(col(f"AQI_{y}").desc())
#     df_top_global = df.select("city", "country", f"AQI_{y}").withColumn("ID", row_number().over(window_year))
#     top3_cities = df_top_global.filter(col("ID") <= 3).show()


# 28. A more curious beginner approach :D
top3_cities_per_year = {}

for y in years:
    window_year = Window.orderBy(col(f"AQI_{y}").desc())
    df_top = df.select("city", "country", f"AQI_{y}")\
               .withColumn("rank", rank().over(window_year))\
               .filter(col("rank") <= 3)
    top3_cities_per_year[y] = df_top

# A result for 2017
print("top3_cities_2017_B:")
top3_cities_per_year[2017].show()

##     * The second approach is better because the rank() transformation will include all cities with the same AQI value, not just the first one in the DataFrame.

# 29. For each country, rank the cities by their AQI value in 2023
window_2023 = Window.partitionBy("country").orderBy(col("AQI_2023").desc())
top_AQI_per_cities_2023 = df.select("city", "country", "AQI_2023").withColumn("ID", row_number().over(window_2023))
print("cities_rank_per_country_2023:")
top_AQI_per_cities_2023.show(30, truncate=False)

# 30. Value Distribution -> group the 2023 values into “buckets”, e.g.:

#       * 0–10 (clean air),
#       * 10–20 (moderate),
#       * 20–50 (polluted),
#       * 50+ (heavily polluted)
#     * Count how many cities fall into each bucket.

print("df_bucket:")
df_bucket = df.select("city", "AQI_2023")\
              .withColumn("bucket", when(col("AQI_2023") <= 10, "clean air")
              .when((col("AQI_2023") > 10) & (col("AQI_2023") <= 20), "moderate")
              .when((col("AQI_2023") > 20) & (col("AQI_2023") <= 50), "polluted")
              .otherwise("heavily polluted")
              ).groupBy("bucket").count().show()      

