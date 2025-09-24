# Hive – Task 2

* Download the provided CSV file
* Copy it to HDFS
* Create the `Zipcode` table
* Load the data from the file into the table
* Display all records for ZIP codes from Florida
* Store the results in a new table `ZipcodeFL` (CTAS)

This task demonstrates how to import a CSV file into Hive, filter data for a specific state, and store the results in a new table using CTAS (Create Table As Select).

---

## Steps

### 1. Download the CSV file

Obtain the provided `zipcode.csv` file.

---

### 2. Copy the file to HDFS

Enter the **namenode-hive2** container and run:

```bash
hdfs dfs -mkdir /user/hive/input
hdfs dfs -put zipcode.csv /user/hive/input/zipcode.csv
```

---

### 3. Create the `Zipcode` table

Enter the **hive-server-hive2** container and start the **Beeline** client.

Run the following DDL to create the table:

```sql
CREATE TABLE Zipcode (
    RecordNumber INT,
    Zipcode STRING,
    ZipCodeType STRING,
    City STRING,
    State STRING,
    LocationType STRING,
    Lat DOUBLE,
    Long DOUBLE,
    Xaxis DOUBLE,
    Yaxis DOUBLE,
    Zaxis DOUBLE,
    WorldRegion STRING,
    Country STRING,
    LocationText STRING,
    Location STRING,
    Decommisioned STRING,
    TaxReturnsFiled STRING,
    EstimatedPopulation STRING,
    TotalWages STRING,
    Notes STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");
```

---

### 4. Load data from the CSV into the table

```sql
LOAD DATA INPATH '/user/hive/input/zipcode.csv' INTO TABLE Zipcode;
```

---

### 5. Display all records for Florida

```sql
SELECT * FROM Zipcode WHERE State = "FL" LIMIT 5;
```

---

### 6. Save results into a new table (`ZipcodeFL`)

Hive supports **CTAS** (Create Table As Select), which creates a new table and populates it in one step.

Option 1 — Create and populate in one command:

```sql
CREATE TABLE ZipcodeFL AS
SELECT * FROM Zipcode WHERE State = "FL";
```

Option 2 — Create an empty table first, then insert:

```sql
CREATE TABLE ZipcodeFL LIKE Zipcode;

INSERT INTO ZipcodeFL
SELECT * FROM Zipcode WHERE State = "FL";
```

EOF
