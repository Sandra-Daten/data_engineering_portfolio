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

SELECT * FROM Movie_rating LIMIT 5;

INSERT OVERWRITE LOCAL DIRECTORY '/tmp/movie_ratings_exported'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT * FROM Movie_rating LIMIT 5;

