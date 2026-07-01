import os
import requests
import pandas as pd

movies = pd.read_csv("movies.csv")
links = pd.read_csv("links.csv")

movies_links = movies.merge(links, on="movieId", how="left")

movies_links = movies_links[movies_links["tmdbId"].notna()]

movies_links["tmdbId"] = movies_links["tmdbId"].astype(int)

movies10 = movies_links.head(10).copy()

def fetch_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"

    params = {
        "api_key": os.getenv("TMDB_API_KEY")
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "overview": "",
            "homepage": ""
        }

    data = response.json()

    return {
        "overview": data.get("overview") or "",
        "homepage": data.get("homepage") or ""
    }


movies10["overview"] = ""
movies10["homepage"] = ""

for idx, row in movies10.iterrows():
    details = fetch_movie_details(row["tmdbId"])

    movies10.at[idx, "overview"] = details["overview"]
    movies10.at[idx, "homepage"] = details["homepage"]

movies10[[
    "movieId",
    "title",
    "tmdbId",
    "overview",
    "homepage"
]]