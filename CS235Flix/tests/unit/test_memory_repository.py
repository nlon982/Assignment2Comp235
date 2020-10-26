import pytest

from CS235Flix.adapters.memory_repository import MemoryRepository, populate
from CS235Flix.domain.user import User
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.director import Director
from CS235Flix.domain.genre import Genre

from CS235Flix.domain.review import Review, make_review


@pytest.fixture
def memory_repository_with_data():
    csv_path = r"C:\Users\Nathan Longhurst\OneDrive - The University of Auckland\b Comp235\Assignment 2\GitHub\Assignment2Comp235\CS235Flix\adapters\data"
    memory_repository = MemoryRepository()
    populate(csv_path, memory_repository)
    return memory_repository

@pytest.fixture
def blank_memory_repository():
    memory_repository = MemoryRepository()
    return memory_repository

class TestMemoryRepositoryWithData: # this inherently tests getters and setters for movies, directors, actors and genres
    def test_movie_dict(self, memory_repository_with_data):
        movie_object = memory_repository_with_data.get_movie("Guardians of the Galaxy", 2014)
        assert movie_object.title == "Guardians of the Galaxy"
        assert movie_object.release_year == 2014
        assert movie_object.runtime_minutes == 121
        assert movie_object.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
        assert movie_object.external_rating == 8.1
        assert movie_object.external_rating_votes == 757074
        assert movie_object.revenue == 333.13
        assert movie_object.metascore == 76

        assert isinstance(movie_object.director, Director)
        assert isinstance(movie_object.actors[0], Actor)
        assert isinstance(movie_object.genres[0], Genre)


    def test_director_dict(self, memory_repository_with_data):
        assert isinstance(memory_repository_with_data.get_director("James Gunn"), Director)

    def test_actor_dict(self, memory_repository_with_data):
        assert isinstance(memory_repository_with_data.get_actor("Chris Pratt"), Actor)

    def test_genre_dict(self, memory_repository_with_data):
        assert isinstance(memory_repository_with_data.get_genre("Action"), Genre)

    def test_get_all(self, memory_repository_with_data):
        assert len(memory_repository_with_data.get_all_movies()) == 1000
        assert len(memory_repository_with_data.get_all_directors()) == 644
        assert len(memory_repository_with_data.get_all_actors()) == 1985
        assert len(memory_repository_with_data.get_all_genres()) == 20

    def test_user_list(self, memory_repository_with_data):
        assert isinstance(memory_repository_with_data.get_user("thorke"), User)

    def test_get_movies_with_actor(self, memory_repository_with_data): # (inherently means get_movie works). This is a helper funciton to the below, it isn't a Abstract Method
        assert memory_repository_with_data.get_movie("Guardians of the Galaxy", 2014) in memory_repository_with_data.get_movies_with_actor("Chris Pratt")

    def test_get_movies_with_director(self, memory_repository_with_data): # ditto
        assert memory_repository_with_data.get_movie("Guardians of the Galaxy", 2014) in memory_repository_with_data.get_movies_with_director("James Gunn")

    def test_get_movies_with_genre(self, memory_repository_with_data): # ditto
        assert memory_repository_with_data.get_movie("Guardians of the Galaxy", 2014) in memory_repository_with_data.get_movies_with_genre("Action")

    def test_get_movies_with_actor_director_and_genre(self, memory_repository_with_data):
        assert memory_repository_with_data.get_movie("Guardians of the Galaxy", 2014) in memory_repository_with_data.get_movies_with_actor_director_or_genre("Chris Pratt", "James Gunn", "Action")



class TestBlankMemoryRepository:
    def test_add_and_get_user(self, blank_memory_repository):
        a_user = User("oldmanjenkins", "Elephant12")
        blank_memory_repository.add_user(a_user)

        assert blank_memory_repository.get_user("oldmanjenkins") == a_user


