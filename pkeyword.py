import pandas as pd

movies = pd.read_csv(
    "movies_recommendation_dataset_updated.csv"
)

# Create columns if not present
for col in ["themes", "universe"]:
    if col not in movies.columns:
        movies[col] = ""

# LCU movies
lcu = ["Leo", "Vikram", "Kaithi"]

movies.loc[
    movies["title"].isin(lcu),
    "universe"
] = "LCU"

# MCU movies
mcu = [
    "Avengers: Endgame",
    "Loki",
    "WandaVision",
    "Doctor Strange"
]

movies.loc[
    movies["title"].isin(mcu),
    "universe"
] = "MCU"

# Themes
movies.loc[
    movies["title"] == "Amaran",
    "themes"
] = "military,patriotism,biography"

movies.loc[
    movies["title"] == "Major",
    "themes"
] = "military,patriotism,biography"

movies.loc[
    movies["title"] == "Leo",
    "themes"
] = "crime,action,revenge"

movies.loc[
    movies["title"] == "Vikram",
    "themes"
] = "crime,spy,action"

movies.to_csv(
    "movies_recommendation_dataset_updated.csv",
    index=False
)

print("Dataset Updated")