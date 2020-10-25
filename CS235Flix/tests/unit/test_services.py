import pytest

from CS235Flix.movies_blueprint.services import movie_to_dict, movies_to_dict

from CS235Flix.domain.movie import Movie
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.genre import Genre

@pytest.fixture
def a_movie(): # these values are half made up
    a_movie = Movie("Guardians", 2014)
    a_movie.runtime_minutes = 100
    a_movie.description = "descriptiongoeshere"
    a_movie.director = Director("James Gunn")
    a_movie.actors = [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper")]
    a_movie.genres = [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
    a_movie.external_rating = 8.1
    a_movie.external_rating_votes = 31204
    a_movie.revenue = 301
    a_movie.metascore = 74
    return a_movie

class TestMovieService:
    def test_movie_to_dict(self, a_movie):
        a_movie_dict = movie_to_dict(a_movie)
        assert a_movie_dict["title"] == "Guardians"
        assert a_movie_dict["release_year"] == 2014
        assert a_movie_dict["description"] == "descriptiongoeshere"
        assert a_movie_dict["director"] == Director("James Gunn")
        assert a_movie_dict["actors"] == [Actor("Chris Pratt"), Actor("Vin Diesel"), Actor("Bradley Cooper")]
        assert a_movie_dict["genres"] == [Genre("Action"), Genre("Adventure"), Genre("Sci-Fi")]
        assert a_movie_dict["external_rating"] == 8.1
        assert a_movie_dict["external_rating_votes"] == 31204
        assert a_movie_dict["revenue"] == 301
        assert a_movie_dict["metascore"] == 74


    def test_movies_to_dict(self, a_movie):
        a_movie_dict = movie_to_dict(a_movie) # to compare to

        movie_list = [a_movie, a_movie]
        movie_dict_list = movies_to_dict(movie_list)

        assert movie_dict_list[0] == a_movie_dict
        assert movie_dict_list[1] == a_movie_dict

# presumably the rest work as it just copy and pasted the aboves code and changed where relevant
