#!/bin/bash

# Copy CSV file into hive-server container
docker cp /Users/sandra/Downloads/03_DE_Vezbe/portfolio/hive/docker-hive5/foundations.csv hive-server:/tmp

# Start docker containers
docker-compose up -d

# Access hive-server container bash
docker-compose exec -it hive-server bash 

# Create HDFS directory and upload CSV

hdfs dfs -mkdir -p /user/hive/input
hdfs dfs -put /tmp/foundations.csv /user/hive/input
hdfs dfs -ls /user/hive/input

# Start Beeline and run Hive commands
beeline -u jdbc:hive2://localhost:10000/default 

CREATE EXTERNAL TABLE IF NOT EXISTS FoundationExt (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/hive/input/'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS FoundationAvro (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS AVRO
TBLPROPERTIES (
  'avro.schema.literal'=
  '{
    "namespace": "com.howdy",
    "name": "some_schema",
    "type": "record",
    "fields": [
      {"name":"Name","type":"string"},
      {"name":"IDNumber","type":"long"},
      {"name":"PlaceCode","type":"int"},
      {"name":"MunicipalityCode","type":"int"},
      {"name":"RegistrationDate","type":"string"}
    ]
  }'
);

INSERT INTO TABLE FoundationAvro
SELECT Name, IDNumber, PlaceCode, MunicipalityCode, RegistrationDate
FROM FoundationExt
WHERE Name IS NOT NULL
  AND IDNumber IS NOT NULL
  AND PlaceCode IS NOT NULL
  AND MunicipalityCode IS NOT NULL
  AND RegistrationDate IS NOT NULL;

CREATE TABLE IF NOT EXISTS FoundationParquet (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate STRING
)
STORED AS PARQUET;

SET parquet.compression=SNAPPY;

INSERT INTO TABLE FoundationParquet
SELECT Name, IDNumber, PlaceCode, MunicipalityCode, RegistrationDate
FROM FoundationExt
WHERE Name IS NOT NULL
  AND IDNumber IS NOT NULL
  AND PlaceCode IS NOT NULL
  AND MunicipalityCode IS NOT NULL
  AND RegistrationDate IS NOT NULL;


# Check HDFS files for Avro table
echo "Avro table files in HDFS:"
hdfs dfs -ls /user/hive/warehouse/foundationavro/

# Check HDFS files for Parquet table
echo "Parquet table files in HDFS:"
hdfs dfs -ls /user/hive/warehouse/foundationparquet/

EOF
