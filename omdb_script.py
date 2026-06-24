import requests
import pandas as pd
import time

API_KEY = "e1b4a396"

# Read titles
with open("titles.txt", "r", encoding="utf-8") as f:
    titles = [line.strip() for line in f if line.strip()]

movies = []
failed_titles = []

# Reuse the same connection
session = requests.Session()

print(f"Found {len(titles)} titles\n")

for i, title in enumerate(titles, start=1):
    print(f"[{i}/{len(titles)}] Processing: {title}")

    try:
        # Try exact title search first
        url = f"https://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        response = session.get(url, timeout=10)
        data = response.json()

        # If exact title fails, try keyword search
        if data.get("Response") != "True":

            search_url = (
                f"https://www.omdbapi.com/?s={title}&apikey={API_KEY}"
            )

            search = session.get(
                search_url,
                timeout=10
            ).json()

            if search.get("Response") == "True":

                imdb_id = search["Search"][0]["imdbID"]

                detail_url = (
                    f"https://www.omdbapi.com/?i={imdb_id}"
                    f"&apikey={API_KEY}"
                )

                data = session.get(
                    detail_url,
                    timeout=10
                ).json()

        # Save movie details
        if data.get("Response") == "True":

            movies.append({
                "title": data.get("Title"),
                "year": data.get("Year"),
                "type": data.get("Type"),
                "genre": data.get("Genre"),
                "director": data.get("Director"),
                "actors": data.get("Actors"),
                "language": data.get("Language"),
                "country": data.get("Country"),
                "runtime": data.get("Runtime"),
                "overview": data.get("Plot"),
                "awards": data.get("Awards"),
                "imdb_rating": data.get("imdbRating"),
                "imdb_votes": data.get("imdbVotes"),
                "poster": data.get("Poster"),
                "imdb_id": data.get("imdbID")
            })

            print(f"✓ Added: {data.get('Title')}")

        else:
            failed_titles.append(title)
            print(f"✗ Not Found: {title}")

        time.sleep(0.25)

    except requests.exceptions.Timeout:
        failed_titles.append(title)
        print(f"⌛ Timeout: {title}")
        continue

    except requests.exceptions.ConnectionError:
        failed_titles.append(title)
        print(f"🌐 Connection Error: {title}")
        time.sleep(2)
        continue

    except Exception as e:
        failed_titles.append(title)
        print(f"❌ Error: {title}")
        print(e)
        continue

# Save dataset
df = pd.DataFrame(movies)

df.to_csv(
    "movie_recommendation_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

# Save failed titles
with open(
    "failed_titles.txt",
    "w",
    encoding="utf-8"
) as f:
    for title in failed_titles:
        f.write(title + "\n")

print("\n========================")
print("DATASET CREATED")
print("========================")
print(f"Total Titles : {len(titles)}")
print(f"Success      : {len(df)}")
print(f"Failed       : {len(failed_titles)}")
print("Saved: movie_recommendation_dataset.csv")
print("Saved: failed_titles.txt")