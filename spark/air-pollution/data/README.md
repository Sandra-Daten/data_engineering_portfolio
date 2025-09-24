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

![Example Screenshot](images/example.png)

