
beeline -u jdbc:hive2://localhost:10000/default 


CREATE EXTERNAL TABLE star2000_ext (
  charge FLOAT,
  clus INT,
  dst INT,
  hist INT,
  enumber INT,
  etime DOUBLE,
  rnumber INT,
  nlb INT,
  qxb FLOAT,
  tracks INT,
  vertex FLOAT,
  zdc INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/input/';


CREATE TABLE star2000_csv (
  charge FLOAT,
  clus INT,
  dst INT,
  hist INT,
  enumber INT,
  etime DOUBLE,
  rnumber INT,
  nlb INT,
  qxb FLOAT,
  tracks INT,
  vertex FLOAT,
  zdc INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;


LOAD DATA INPATH '/user/hive/input/star2000.csv' INTO TABLE star2000_csv; - koristila sam ovo, podaci su iz input foldera nestali i presli u warehouse/star2000.csv/star2000.csv
ili
LOAD DATA INPATH '/user/hive/input/star2000.csv'
OVERWRITE INTO TABLE star2000_csv;

INSERT INTO TABLE star2000_ext
SELECT * FROM star2000_csv; - pukao je hive-server jer je csv prevelik

LOAD DATA INPATH '/user/hive/input/star2000.csv' INTO TABLE star2000_ext; 

CREATE TABLE star2000_avro
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.avro.AvroSerDe'
STORED AS AVRO
TBLPROPERTIES (
  'avro.schema.literal'='{
     "namespace":"example.star",
     "type":"record",
     "name":"Star2000",
     "fields":[
       {"name":"charge","type":"float"},
       {"name":"clus","type":"int"},
       {"name":"dst","type":"int"},
       {"name":"hist","type":"int"},
       {"name":"enumber","type":"int"},
       {"name":"etime","type":"double"},
       {"name":"rnumber","type":"int"},
       {"name":"nlb","type":"int"},
       {"name":"qxb","type":"float"},
       {"name":"tracks","type":"int"},
       {"name":"vertex","type":"float"},
       {"name":"zdc","type":"int"}
     ]
  }'
);

///
INSERT INTO star2000_avro
SELECT * FROM star2000_csv;
///


CREATE TABLE star2000_parquet
LIKE star2000_csv
STORED AS PARQUET;

///
INSERT INTO star2000_parquet
SELECT * FROM star2000_csv; 
///

CREATE TABLE star2000_csv_part (
  charge FLOAT,
  clus INT,
  dst INT,
  hist INT,
  enumber INT,
  etime DOUBLE,
  rnumber INT,
  nlb INT,
  qxb FLOAT,
  tracks INT,
  vertex FLOAT,
  zdc INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA INPATH '/user/hive/input/star2000_parts/star2000_part_aa'
INTO TABLE star2000_csv_part;
INSERT INTO star2000_avro SELECT * FROM star2000_csv_part;
INSERT INTO star2000_parquet SELECT * FROM star2000_csv_part;

LOAD DATA INPATH '/user/hive/input/star2000_parts/star2000_part_ab'
OVERWRITE INTO TABLE star2000_csv_part;
INSERT INTO star2000_avro SELECT * FROM star2000_csv_part;
INSERT INTO star2000_parquet SELECT * FROM star2000_csv_part;

...

///

DESCRIBE star2000_csv_part;
DESCRIBE star2000_avro;

CREATE TABLE IF NOT EXISTS star2000_avro (
  charge DOUBLE,
  clus STRING,
  dst STRING,
  hist STRING,
  enumber STRING,
  etime DOUBLE,
  rnumber STRING,
  nlb STRING,
  qxb DOUBLE,
  tracks STRING,
  vertex DOUBLE,
  zdc STRING
)
STORED AS AVRO;

TRUNCATE TABLE star2000_avro; - ako tabela postoji, ovako obrisati sve iz nje

CREATE EXTERNAL TABLE IF NOT EXISTS star2000_csv_ext (
  charge STRING,
  clus STRING,
  dst STRING,
  hist STRING,
  enumber STRING,
  etime STRING,
  rnumber STRING,
  nlb STRING,
  qxb STRING,
  tracks STRING,
  vertex STRING,
  zdc STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
STORED AS TEXTFILE
LOCATION '/user/hive/input/star2000_parts/';

INSERT INTO star2000_avro
SELECT
  CAST(charge AS DOUBLE),
  clus,
  dst,
  hist,
  enumber,
  CAST(etime AS DOUBLE),
  rnumber,
  nlb,
  CAST(qxb AS DOUBLE),
  tracks,
  CAST(vertex AS DOUBLE),
  zdc
FROM star2000_csv_ext;


INSERT INTO star2000_avro
SELECT
  CAST(charge AS DOUBLE),
  clus,
  dst,
  hist,
  enumber,
  CAST(etime AS DOUBLE),
  rnumber,
  nlb,
  CAST(qxb AS DOUBLE),
  tracks,
  CAST(vertex AS DOUBLE),
  zdc
FROM star2000_csv_ext
LIMIT 1000;


SELECT COUNT(*) FROM star2000_avro;
SELECT * FROM star2000_avro LIMIT 10;











INSERT INTO star2000_avro
SELECT
  CAST(charge AS DOUBLE),
  clus,
  dst,
  hist,
  enumber,
  CAST(etime AS DOUBLE),
  rnumber,
  nlb,
  CAST(qxb AS DOUBLE),
  tracks,
  CAST(vertex AS DOUBLE),
  zdc
FROM star2000_csv_ext
LIMIT 10;


