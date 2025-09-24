import pandas as pd

df = pd.read_csv('/Users/sandra/Downloads/03_DE_Vezbe/portfolio/hive/docker-hive3/000000_0', names=['user_id', 'movie_id', 'rating', 'rating_timestamp'])

avg_ratings = df.groupby('user_id')['rating'].mean().reset_index()
avg_ratings = avg_ratings.sort_values(by='rating', ascending=False)
avg_ratings = avg_ratings.sort_values(by='rating', ascending=False).reset_index(drop=True)


print(avg_ratings.head(10))
