#!/bin/bash

# Paths
LOCAL_CSV_PATH="/Users/sandra/Downloads/03_DE_Vezbe/portfolio/hive/docker-hive4/foundations.csv"
HDFS_DIR="/user/hive/input"
CSV_FILENAME="foundations.csv"

echo "🔁 Copying CSV file to Hive container..."
docker cp "$LOCAL_CSV_PATH" hive-server:/tmp/$CSV_FILENAME

echo "🚪 Entering Hive container..."
docker-compose exec -T hive-server bash <<EOF

echo "📁 Creating HDFS input directory if not exists..."
hdfs dfs -mkdir -p $HDFS_DIR

echo "⬆️  Uploading CSV file to HDFS..."
hdfs dfs -put -f /tmp/$CSV_FILENAME $HDFS_DIR

echo "🗃️  Creating external table..."
hive -e "
DROP TABLE IF EXISTS FoundationExt;

CREATE EXTERNAL TABLE FoundationExt (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate DATE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  \"separatorChar\" = \",\",
  \"quoteChar\" = \"\\\"\",
  \"escapeChar\" = \"\\\\\"
)
STORED AS TEXTFILE
LOCATION '$HDFS_DIR'
TBLPROPERTIES (\"skip.header.line.count\"=\"1\");
"

echo "📦 Creating partitioned table..."
hive -e "
DROP TABLE IF EXISTS foundations_partitioned;

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
"

echo "⚙️ Enabling dynamic partitioning and loading data..."
hive -e \"
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

INSERT INTO TABLE foundations_partitioned PARTITION (year)
SELECT
  Name,
  IDNumber,
  PlaceCode,
  MunicipalityCode,
  RegistrationDate,
  YEAR(RegistrationDate) AS year
FROM FoundationExt;
\"

echo "✅ All done. Preview partitions:"
hive -e "SHOW PARTITIONS foundations_partitioned;"
EOF
