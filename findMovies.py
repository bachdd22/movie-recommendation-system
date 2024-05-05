import requests
from helpers import cache
from key import tmdb_api_key
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + tmdb_api_key
}

@cache.memoize(timeout=60)
def findPosters(movie_id):
    if len(movie_id) < 8:
        movie_id = movie_id.zfill(7)
    url = "https://api.themoviedb.org/3/find/"+ "tt" + movie_id +"?external_source=imdb_id"
    response = requests.get(url, headers=headers).json()
    base_url = "https://image.tmdb.org/t/p/original"
    if len(response["movie_results"]) < 1:
        return None
    link = base_url + response["movie_results"][0]["poster_path"]
    return link


@cache.memoize(timeout=60)
def findPopular(page=1):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=" + str(page)
    response = requests.get(url, headers=headers).json()["results"]
    base_url = "https://image.tmdb.org/t/p/original"
    for movie in response:
        movie["backdrop_path"] = base_url + movie["backdrop_path"]
        movie["poster_path"] = base_url + movie["poster_path"]
    return response
