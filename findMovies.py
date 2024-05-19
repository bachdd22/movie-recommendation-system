import requests
from helpers import cache
import random
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
    if response["movie_results"][0]["poster_path"]:
        link = base_url + response["movie_results"][0]["poster_path"]
    return link, str(response["movie_results"][0]["id"])


@cache.memoize(timeout=60)
def findPopular(page=1):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=" + str(page)
    response = requests.get(url, headers=headers).json()["results"]
    base_url = "https://image.tmdb.org/t/p/original"
    for movie in response:
        if movie["backdrop_path"]:
            movie["backdrop_path"] = base_url + movie["backdrop_path"]
        if movie["poster_path"]:
            movie["poster_path"] = base_url + movie["poster_path"]
    random.shuffle(response)
    return response

@cache.memoize(timeout=60)
def findNowPlaying(page=1):
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=" + str(page)
    response = requests.get(url, headers=headers).json()["results"]
    base_url = "https://image.tmdb.org/t/p/original"
    for movie in response:
        if movie["backdrop_path"]:
            movie["backdrop_path"] = base_url + movie["backdrop_path"]
        if movie["poster_path"]:
            movie["poster_path"] = base_url + movie["poster_path"]
    random.shuffle(response)
    return response

@cache.memoize(timeout=60)
def findTopRated(page=1):
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=" + str(page)
    response = requests.get(url, headers=headers).json()["results"]
    base_url = "https://image.tmdb.org/t/p/original"
    for movie in response:
        if movie["backdrop_path"]:
            movie["backdrop_path"] = base_url + movie["backdrop_path"]
        if movie["poster_path"]:
            movie["poster_path"] = base_url + movie["poster_path"]
    random.shuffle(response)
    for i in [1, 7]:
        url = "https://api.themoviedb.org/3/movie/" + str(response[i]["id"]) +  "/images?language=en"
        images = requests.get(url, headers=headers).json()
        response[i]["logo_path"] = base_url + images["logos"][0]["file_path"] 
    return response

@cache.memoize(timeout=60)
def findUpcoming(page=1):
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=" + str(page)
    response = requests.get(url, headers=headers).json()["results"]
    base_url = "https://image.tmdb.org/t/p/original"
    for movie in response:
        if movie["backdrop_path"]:
            movie["backdrop_path"] = base_url + movie["backdrop_path"]
        if movie["poster_path"]:
            movie["poster_path"] = base_url + movie["poster_path"]
    random.shuffle(response)
    return response

@cache.memoize(timeout=60)
def getMovieDetails(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + movie_id + "?language=en-US"
    base_url = "https://image.tmdb.org/t/p/original"
    response = requests.get(url, headers=headers).json()
    if response["imdb_id"]:
        imdb_id = response["imdb_id"]
        url = "https://api.themoviedb.org/3/find/"+ imdb_id +"?external_source=imdb_id"
        response_1 = requests.get(url, headers=headers).json()
        response["overview"] = response_1["movie_results"][0]["overview"]
        response["release_date"] = response_1["movie_results"][0]["release_date"]
        
    if response["backdrop_path"]:
        response["backdrop_path"] = base_url + response["backdrop_path"]
    if response["poster_path"]:
        response["poster_path"] = base_url + response["poster_path"]
    
    return response

@cache.memoize(timeout=60)
def getMoviePicture(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/images?include_image_language=en"
    base_url = "https://image.tmdb.org/t/p/original"
    types = ["backdrops", "posters", "logos"]
    response = requests.get(url, headers=headers).json()
    images = dict()
    for type in types:
        images[type] = [i["file_path"] for i in response[type]]
        for index in range(len(images[type])):
            images[type][index] = base_url + images[type][index]
    return images["backdrops"] + images["posters"]

@cache.memoize(timeout=60)
def getMovieClips(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/videos?language=en-US"
    response = requests.get(url, headers=headers).json()
    videos = response["results"]
    return videos
