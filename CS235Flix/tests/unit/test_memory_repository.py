import pytest

from CS235Flix.adapters.memory_repository import MemoryRepository, populate
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.director import Director
from CS235Flix.domain.genre import Genre


@pytest.fixture
def memory_repository_with_data():
    csv_path = r"C:\Users\Nathan Longhurst\OneDrive - The University of Auckland\b Comp235\Assignment 2\GitHub\Assignment2Comp235\CS235Flix\adapters\data\Data1000Movies.csv"
    memory_repository = MemoryRepository()
    populate(csv_path, memory_repository)
    return memory_repository

class TestMemoryRepositoryWithData:
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
