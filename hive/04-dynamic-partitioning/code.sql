## DODATI FAJL NA hdfs
docker cp /Users/sandra/Downloads/03_DE_Vezbe/portfolio/hive/docker-hive4/foundations.csv hive-server:/tmp
docker-compose exec -it hive-server bash
hdfs dfs -mkdir -p /user/hive/input
hdfs dfs -put /tmp/foundations.csv /user/hive/input
hdfs dfs -ls /user/hive/input

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

## PROVERITI PODATKE

SELECT * FROM FoundationExt LIMIT 10;

## KREIRATI TABELU PARTICIONISANU PO GODINAMA

CREATE TABLE foundations_partitioned (
  Name STRING,
  IDNumber BIGINT,
  PlaceCode INT,
  MunicipalityCode INT,
  RegistrationDate DATE
)
PARTITIONED BY (year INT)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
;

## UCITATI PODATKE IZ EKSTERNE TABELU POMOCU DINAMICKOG PARTICIONISANJA

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

SHOW PARTITIONS foundations_partitioned;




