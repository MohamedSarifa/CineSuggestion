import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")


def search_movie(movie_name):

    url = "https://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": movie_name
    }

    response = requests.get(
    url,
    params=params,
    timeout=10)

    data = response.json()

    if data.get("Response") == "True":

        return {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "genre": data.get("Genre"),
            "rating": data.get("imdbRating"),
            "plot": data.get("Plot"),
            "poster": data.get("Poster")
        }

    return None