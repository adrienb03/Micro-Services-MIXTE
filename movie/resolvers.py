from pymongo import ReturnDocument
from database import movies_collection, actors_collection


# query { get_movies { id title rating } }
def get_movies(_, info):
    movies = list(movies_collection.find({}, {"_id": 0}))
    return movies

# query { movie_with_id(_id: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6") { id title rating } }
def movie_with_id(_, info, _id):
    movie = movies_collection.find_one({"id": _id}, {"_id": 0})
    return movie

# mutation { add_movie(movie: { id: "123", title: "Inception", director: "Christopher Nolan", rating: 8.8 }) { id title director rating } }
def add_movie(_, info, movie):
    movies_collection.insert_one(movie.copy())
    return movie

# mutation { update_movie_rate(_id: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6", _rate: 9.5) { id title director rating } }
def update_movie_rate(_, info, _id, _rate):
    updated_movie = movies_collection.find_one_and_update(
        {"id": _id},
        {"$set": {"rating": _rate}},
        return_document=ReturnDocument.AFTER,
        projection={"_id": 0}
    )
    return updated_movie

# mutation { delete_movie(_id: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6") { id title director rating } }
def delete_movie(_, info, _id):
    deleted_movie = movies_collection.find_one_and_delete(
        {"id": _id},
        projection={"_id": 0}
    )
    return deleted_movie

# query { movie_with_id(_id: "a8034f44-aee4-44cf-b32c-74cf452aaaae") { title actors { firstname lastname birthyear } } }
def resolve_actors_in_movie(movie, info):
    actors = list(actors_collection.find(
        {"films": movie["id"]},
        {"_id": 0}
    ))
    return actors
