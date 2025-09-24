# Hive - task4: Partitioned Table Task

This project demonstrates how to work with external and partitioned tables in Apache Hive using CSV data. The source data contains a list of all registered foundations in Serbia, and the task involves uploading it to HDFS, creating Hive tables, and performing dynamic partitioning by year.

## Dataset

- **Source**: [data.gov.rs](https://data.gov.rs/)
- **Format**: CSV
- **Description**: List of all registered foundations in Serbia, including fields like name, registration number, municipality code, and registration date.

---

## Task Overview

1. Upload the CSV file to HDFS
2. Create an external Hive table using OpenCSVSerde
3. Inspect and verify the data
4. Create a new partitioned Hive table (partitioned by year)
5. Load data from the external table using dynamic partitioning
6. Verify partitions and resulting HDFS files

---

## Step-by-Step Guide

### 1. Upload CSV to HDFS

```bash
docker cp /local/path/foundations.csv hive-server:/tmp
docker-compose exec -it hive-server bash

hdfs dfs -mkdir -p /user/hive/input
hdfs dfs -put /tmp/foundations.csv /user/hive/input
hdfs dfs -ls /user/hive/input

# 2. Create External Table in Hive

CREATE EXTERNAL TABLE FoundationExt (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate DATE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/input/'
TBLPROPERTIES ("skip.header.line.count"="1");

# Preview the Data

SELECT * FROM FoundationExt LIMIT 10;

# 4. Create Partitioned Table by Year

CREATE TABLE foundations_partitioned (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate DATE
)
PARTITIONED BY (year INT)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE;

# 5. Enable Dynamic Partitioning

SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

# 6. Load Data into Partitioned Table

INSERT INTO TABLE foundations_partitioned PARTITION (year)
SELECT
  Name,
  IDNumber,
  PlaceCode,
  MunicipalityCode,
  RegistrationDate,
  YEAR(RegistrationDate) AS year
FROM FoundationExt;

# 7. Verify Partitions and Output

SHOW PARTITIONS foundations_partitioned;

hdfs dfs -ls /user/hive/warehouse/foundations_partitioned

EOF


