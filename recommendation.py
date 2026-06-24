import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ================= LOAD DATASET =================

movies = pd.read_csv(
    "movies_recommendation_dataset_updated.csv"
)

movies.drop_duplicates(
    subset="title",
    inplace=True
)

movies.reset_index(
    drop=True,
    inplace=True
)


# ================= CLEAN DATA =================

text_columns = [
    "genre",
    "keywords",
    "overview",
    "language",
    "category",
    "themes",
    "universe",
    "actors",
    "director",
    "type"
]

for col in text_columns:

    if col in movies.columns:

        movies[col] = (
            movies[col]
            .fillna("")
            .astype(str)
            .str.strip()
        )


# ================= CREATE TAGS =================

movies["tags"] = (

    movies["genre"] + " " +
    movies["genre"] + " " +

    movies["keywords"] + " " +
    movies["keywords"] + " " +

    movies["themes"] + " " +
    movies["themes"] + " " +
    movies["themes"] + " " +

    movies["actors"] + " " +
    movies["director"] + " " +

    movies["category"] + " " +
    movies["language"] + " " +

    movies["overview"]

)


# ================= TF-IDF =================

tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=10000
)

vectors = tfidf.fit_transform(
    movies["tags"]
)

similarity = cosine_similarity(
    vectors
)


# ================= RECOMMENDATION FUNCTION =================

def get_recommendations(movie_name):

    movie_name = movie_name.lower().strip()

    match = movies[
        movies["title"]
        .str.lower()
        .str.strip()
        ==
        movie_name
    ]

    if match.empty:
        return []

    index = match.index[0]

    current_movie = movies.iloc[index]

    distances = list(
        enumerate(
            similarity[index]
        )
    )

    distances = sorted(
        distances,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i, score in distances:

        if i == index:
            continue

        movie = movies.iloc[i]

        bonus = 0

        # ================= SAME TYPE =================

        if (
            movie["type"].lower()
            !=
            current_movie["type"].lower()
              ):
              continue
        
        # ================= LANGUAGE =================

        if (
            movie["language"].lower()
            ==
            current_movie["language"].lower()
        ):
            bonus += 0.05

        # ================= CATEGORY =================

        if (
            movie["category"].lower()
            ==
            current_movie["category"].lower()
        ):
            bonus += 0.08

        # ================= GENRE =================

        genres1 = set(
            x.strip()
            for x in str(
                current_movie["genre"]
            ).lower().split(",")
            if x.strip()
        )

        genres2 = set(
            x.strip()
            for x in str(
                movie["genre"]
            ).lower().split(",")
            if x.strip()
        )

        common_genres = len(
            genres1.intersection(
                genres2
            )
        )

        bonus += common_genres * 0.05

        # ================= THEMES =================

        themes1 = set(
            x.strip()
            for x in str(
                current_movie["themes"]
            ).lower().split(",")
            if x.strip()
        )

        themes2 = set(
            x.strip()
            for x in str(
                movie["themes"]
            ).lower().split(",")
            if x.strip()
        )

        common_themes = len(
            themes1.intersection(
                themes2
            )
        )

        bonus += common_themes * 0.10

        # ================= ACTORS =================

        actors1 = set(
            x.strip()
            for x in str(
                current_movie["actors"]
            ).lower().split(",")
            if x.strip()
        )

        actors2 = set(
            x.strip()
            for x in str(
                movie["actors"]
            ).lower().split(",")
            if x.strip()
        )

        common_actors = len(
            actors1.intersection(
                actors2
            )
        )

        bonus += common_actors * 0.08

        # ================= DIRECTOR =================

        if (
            movie["director"].lower()
            ==
            current_movie["director"].lower()
            and
            movie["director"] != ""
        ):
            bonus += 0.08

        # ================= UNIVERSE =================

        if (
            movie["universe"].lower()
            ==
            current_movie["universe"].lower()
            and
            movie["universe"] != ""
        ):
            bonus += 0.15

        # ================= FINAL SCORE =================

        final_score = min(
            round(
                (score + bonus) * 100,
                1
            ),
            100
        )

        recommendations.append(
            (
                movie["title"],
                final_score
            )
        )

    # ================= REMOVE DUPLICATES =================

    seen = set()
    final_recommendations = []

    for title, score in recommendations:

        if title not in seen:

            seen.add(title)

            final_recommendations.append(
                (
                    title,
                    score
                )
            )

    final_recommendations = sorted(
        final_recommendations,
        key=lambda x: x[1],
        reverse=True
    )

    return final_recommendations[:20]
def get_movie_details(title):

    movie = movies[
        movies["title"].str.lower().str.strip()
        ==
        title.lower().strip()
    ]

    if movie.empty:
        return None

    row = movie.iloc[0]

    return {
        "title": row.get("title", ""),
        "year": row.get("year", ""),
        "genre": row.get("genre", ""),
        "poster": row.get("poster", ""),
        "plot": row.get("overview", ""),
        "rating": row.get("imdb_rating", ""),
        "type": row.get("type", "")
    }