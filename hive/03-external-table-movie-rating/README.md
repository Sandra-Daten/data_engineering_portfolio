# Hive - task 3:Movie Ratings

This example demonstrates how to work with the **MovieLens 100k dataset** in Hive.  
The dataset contains **100,000 records** with user ratings for movies.  

- The MovieLens 100k dataset contains 100,000 items with user ratings for movies  
- Create a table whose content will be stored on HDFS as a text file  
- Within Hive SQL statements, it is possible to include execution of Python scripts that implement more complex data processing  
- More details about this example: https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-SimpleExampleUseCases

---

## Steps

### 1. About the dataset
- The **MovieLens 100k** dataset contains 100k entries of user ratings for various movies.
- The table data will be stored in **HDFS** as a plain text file.
- Hive SQL queries can include **Python scripts** to perform more complex data processing.
- More details can be found in the Hive documentation:  
  [Hive – Simple Example Use Cases](https://cwiki.apache.org/confluence/display/Hive/GettingStarted#GettingStarted-SimpleExampleUseCases)

---

### 2. Create the external table

```sql
CREATE EXTERNAL TABLE Movie_rating (
    user_id INT,
    movie_id INT,
    rating INT,
    rating_timestamp BIGINT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/user/hive/movielens/';
```

**Explanation:**
- **EXTERNAL TABLE** → The data is not managed by Hive but stored at the specified HDFS location.
- **FIELDS TERMINATED BY '\t'** → The dataset is tab-delimited.
- **LOCATION** → Path in HDFS where the dataset is stored.

---

### 3. Query sample data

```sql
SELECT * FROM Movie_rating LIMIT 5;
```

This displays the first 5 rows from the dataset.

---

### 4. Export query results to a local directory

```sql
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/movie_ratings_exported'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT * FROM Movie_rating LIMIT 5;


EOF
