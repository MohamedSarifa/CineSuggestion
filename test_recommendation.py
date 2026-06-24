import pandas as pd

movies = pd.read_csv("movies_recommendation_dataset_updated.csv")

movie = movies[
    movies["title"].str.lower() == "le coup de foudre"
]

print(movie["poster"].iloc[0])