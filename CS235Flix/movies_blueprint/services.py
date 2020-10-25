def get_movies(a_repo_instance):
    movie_list = a_repo_instance.get_all_movies()[:5] # cropping to 5 for now
    movie_dict_list = movies_to_dict(movie_list)
    return movie_dict_list

def get_movie(title, release_year, a_repo_instance):
    a_movie = a_repo_instance.get_movie(title, release_year)
    a_movie_dict = movie_to_dict(a_movie)
    return a_movie_dict

##########################################
# Domain Model objects ->  Dictionaries
##########################################

def movie_to_dict(a_movie):
    a_movie_dict = {
        'title': a_movie.title,
        'release_year': a_movie.release_year,
        'runtime_minutes': a_movie.runtime_minutes,
        'description': a_movie.description,
        'director': a_movie.director,
        'actors': a_movie.actors,
        'genres': a_movie.genres,
        'external_rating': a_movie.external_rating,
        'external_rating_votes': a_movie.external_rating_votes,
        'revenue': a_movie.revenue,
        'metascore': a_movie.metascore,
        'review_list': a_movie.review_list
    }
    return a_movie_dict

def movies_to_dict(movie_list):
    movie_dict_list = [movie_to_dict(a_movie) for a_movie in movie_list]
    return movie_dict_list

def director_to_dict(a_director):
    a_director_dict = {
        'director_full_name': a_director.director_full_name
    }
    return a_director_dict

def directors_to_dict(director_list):
    director_dict_list = [director_to_dict(a_director) for a_director in director_list]
    return director_dict_list

def actor_to_dict(a_actor):
    a_actor_dict = {
        'actor_full_name': a_actor.actor_full_name,
        'colleague_list': a_actor.colleague_list
    }
    return a_actor_dict

def actors_to_dict(actor_list):
    actor_dict_list = [actor_to_dict(a_actor) for a_actor in actor_list]
    return actor_dict_list

def genre_to_dict(a_genre):
    a_genre_dict = {
        'genre_name': a_genre.genre_name
    }
    return a_genre_dict

def genres_to_dict(genre_list):
    genre_dict_list = [genre_to_dict(a_genre) for a_genre in genre_list]
    return genre_dict_list