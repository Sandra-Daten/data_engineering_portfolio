# Hive - Task 1

* Create a table `Emp` with the columns: `id`, `name`, `age`, `gender`
* Manually create a test `data.csv` file with the specified columns and at least 5 rows
* Copy the `data.csv` file to HDFS
* Load the contents of `data.csv` into the `Emp` table
* Use an HQL query to verify that the data has been loaded
* Store employees older than 30 years into a separate CSV file with a `;` delimiter, in any chosen HDFS location

---

### Run docker-compose.yml file

## Steps

### 1. Create the `Emp` table
Access the `hive-server` container and start the Beeline client:

```sql
CREATE TABLE Emp (
  id INT,
  name STRING,
  age INT,
  gender STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

2. Create data.csv
Using a text editor or terminal, create data.csv:

1,Ana,25,F
2,Marko,35,M
3,Jelena,28,F
4,Nikola,40,M
5,Sanja,32,F

3. Upload data.csv to HDFS
From the hive-server container:

hdfs dfs -mkdir -p /user/hive/input
hdfs dfs -put data.csv /user/hive/input/

4. Load data into Emp
From Beeline:

LOAD DATA INPATH '/user/hive/input/data.csv' INTO TABLE Emp;

5. Verify data

SELECT * FROM Emp;

6. Create Emp_over30 table

CREATE TABLE Emp_over30 (
  id INT,
  name STRING,
  age INT,
  gender STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE;

7. Insert employees over 30

INSERT INTO Emp_over30
SELECT * FROM Emp WHERE age > 30;

8. Export filtered data

hdfs dfs -mkdir -p /user/hive/output
hdfs dfs -cp /user/hive/warehouse/emp_over30/000000_0 /user/hive/output/over30.csv
