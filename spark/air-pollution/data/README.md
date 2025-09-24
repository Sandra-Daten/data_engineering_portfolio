# Air Pollution Analysis (2017--2023)

This project analyzes worldwide air pollution data for the period
between 2017--2023 using PySpark.\
The dataset contains information about Air Quality Index (AQI) values
for different countries and cities.

## Project Structure

    .
    ├── air-pollution/
    │   ├── data/                # Dataset (CSV files)
    │   ├── scripts/             # PySpark scripts
    │   └── README.md            # Project documentation
    ├── wildlife/                # (Another project, mounted separately)
    └── docker-compose.yml       # Container setup

## Features

-   Data preprocessing with PySpark\
-   Filtering of highly polluted cities\
-   Aggregation of yearly AQI values\
-   Visualization-ready outputs

## Requirements

-   Python 3.8+\
-   Apache Spark & PySpark\
-   Docker & Docker Compose (optional for containerized execution)

## How to Run

1.  Clone the repository:

``` bash
git clone https://github.com/your-username/air-pollution.git
cd air-pollution
```

2.  Run PySpark script locally:

``` bash
python3 scripts/air_pollution.py
```

3.  Or run inside Docker:

``` bash
docker-compose up
```

## Example Output

Screenshot examples of Spark DataFrame filtering and analysis results
can be added in this section:

![Example Screenshot](images/example.png)

## Author

Sandra Ćirković\
GitHub: [your-username](https://github.com/your-username)
