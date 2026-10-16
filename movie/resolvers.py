import json

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def add_movie(_,info,movie):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for m in movies['movies']:
            if m['id'] == movie['id']:
                return None
    movies['movies'].append(movie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(movies, wfile)
    return movie

def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def delete_movie(_,info,_id):
    deleted_movie = None
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                deleted_movie = movie
                movies['movies'].remove(movie)
                break
    if deleted_movie is not None:
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            json.dump(movies, wfile)
    return deleted_movie

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result