# Wildlife Losses Analysis

## Project Description
This project analyzes wildlife losses caused by **hunting** and **traffic accidents**.  
The analysis is performed using **Apache Spark** and **Python** to process and explore the datasets.

The goal is to identify trends, compare data sources, and visualize results that can help in understanding the scale of wildlife losses.

---

## Dataset
1. **Wildlife losses in hunnting**  
   [Link](https://data.gov.rs/sr/datasets/izvrsheni-odstrel-divljachi/)

2. **Wildlife losses in traffic**  
   [Link](not active any more)

**The source:** Portal otvorenih podataka Republike Srbije (data.gov.rs)

---

## Project Structure

```
wildlife/
│── wildlife_hunting_losses.csv      # Dataset with hunting-related wildlife losses
│── wildlife_traffic_losses.csv      # Dataset with traffic-related wildlife losses
│── wildlife_losses.py               # Python script with Spark transformations & analysis
│── README.md                        # Project documentation       
│── images                            # Screenshots/Visulaization                 
```

---

## Requirements
- Python 3
- Apache Spark
- HDFS
- Docker & Docker Compose (if running inside containers)

---

## Usage

### 1. Running locally
```bash
python3 wildlife_losses.py
```

### 2. Running with Docker + Spark

1. Start the Docker containers with Hadoop and Spark services (docker-compose up).
2. Place the CSV files in the mapped folder inside the Spark container.
3. Run the script using spark-submit:

```bash
docker exec -it spark-master bash
./spark-submit /opt/wildlife/wildlife_losses.py
```

---

## Results
The script generates insights and visualizations such as:
- Number of wildlife losses by year
- Comparison between hunting and traffic
- Trends in different time periods

---

## Screenshots

```markdown
![Initial DataFrame](images/1-initial-dataframe.png)
![Hunting Losses > 1000](images/2-hunting-losses-above-1000.png)
![Traffic Losses > 100](images/3-traffic-losses-above-100.png)
![Top 5 Losses Per Year](images/4-top5-losses-per-year.png)
![Top 5 Losses Global](images/5-top5-losses-global.png)
![Highest Loss By Species Per Year](images/6-highest-loss-by-species-per-year.png)
![DataFrame Preparation For Pivot](images/7-dataframe-preparation-for-pivot.png)
![Pivoted Table](images/8-pivoted-table.png)
![Largest YoY Hunting Loss](images/9-largest-yoy-hunting-loss.png)
```






