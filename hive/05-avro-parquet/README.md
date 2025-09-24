# Hive - tsk5: Avro and Parquet Table Creation and Data Loading

This project demonstrates how to:

- Create an external Hive table over CSV data.
- Create Hive tables in Avro and Parquet formats.
- Load data from the external CSV table into Avro and Parquet tables.
- Verify the data and files stored on HDFS.

---

## Steps

1. Copy the CSV file to the Hive server container and upload it to HDFS.
2. Create an external Hive table on the CSV data.
3. Create a Hive table stored as Avro with Avro SerDe and schema.
4. Insert data from the external CSV table into the Avro table.
5. Create a Hive table stored as Parquet format.
6. Set Parquet compression to Snappy.
7. Insert data from the external CSV table into the Parquet table.
8. Verify the data in Hive and check the stored files on HDFS.

---

## Hive Table Schemas

- **External CSV table (FoundationExt)**
- **Avro table (FoundationAvro)** with Avro schema
- **Parquet table (FoundationParquet)** with Snappy compression

---

## How to run

Use the provided `run.sh` script to execute all necessary commands automatically.

---

## HDFS paths

- Input CSV: `/user/hive/input/foundations.csv`
- Avro table location: default Hive warehouse directory
- Parquet table location: default Hive warehouse directory

EOF