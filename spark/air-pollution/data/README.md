# Air Pollution Analysis (2017--2023)

This project analyzes worldwide air pollution data for the period
between 2017--2023 using PySpark.\
The dataset contains information about Air Quality Index (AQI) values
for different countries and cities.

---

## Dataset
   **Worldwide City Air Pollution Trends**  
   [Link]( https://www.opendatabay.com/data/ai-ml/184ba6aa-e16c-4246-ac53-3b8e987e5423)

**The source:** Opendaybay Platform (as a Free Dataset Library; opendatabay.com) 

---

## Project Structure

    spark/
    ├── air-pollution/
    │   ├── data/                # Dataset (CSV files) & air-pollution.py file
    │   |── README.md            # Project documentation
    │   |__ images               # Screenshots/Visualization
    │
    ├── wildlife/                # (Another project, mounted separately)
    |__ docker-compose.yml       # Container setup
    
---

## Features

-   Data preprocessing with PySpark\
-   Filtering of highly polluted cities\
-   Aggregation of yearly AQI values\

---

## Requirements

-   Python 3
-   Apache Spark & PySpark
-   HDFS
-   Docker & Docker Compose (optional for containerized execution)

---

## How to Run

1.  Run PySpark script locally:

``` bash
python3 scripts/air_pollution.py
```

2.  Or run inside Docker:

``` bash
docker-compose up -d
```

---

## Example Output

![Initial Dataframe](images/1-initial-dataframe.png)
![Initial Schema](images/2-initial-schema.png)
![Schema Changed](images/3-changed-schema.png)
![New Columns Added](images/4-new-columns-added.png)
!["Status" Columns Renamed](images/5-status-columns-renamed.png)
![Dataframe With Parquet Format](images/6-dataframe-parquer-format-data.png)
![Unique Countries](images/7-unique-countries.png)
![Number Of Cities Per Country](images/8-number-of-cities-per-country.png)
![Top 10 Polluted Cities In 2023](images/9-top10-polluted-cities-2023)
![Western Balkans Cities Compared](images/10-wb-cities-compared.png)
![Average Pollution In 2023](images/11-avg-pollution-2023)
![Serbia Average Pollution In 2023](images/12-serbia-avg-pollution-2023.png)
![Top 5 Polluted Countries In 2023](images/13-top5-polluted-countries-2023.png)
![AQI - 2017 vs 2023](images/14-aqi-2017-vs-2023.png)
![Dataframe Prepared For Pivot Transformation](images/15-df-for-pivot.png)
![Table Pivoted_1](images/16-pivoted-table-1.png)
![Table Pivoted_2](images/17-pivoted-table-2.png)
![Year-Over-Year Difference](images/18-df-with-diff.png)
![City With Max Quality Increase & Max Quality Decrease](images/19-df-with-max-min-values.png)
![Top 3 Cities In 2017](images/20-top3-cities-2017.png)
![Cities Ranked Per Country For 2023](images/21-cities-rank-per-country-2023.png)
![Dataframe's buckets](images/22-dataframe-buckets.png)

