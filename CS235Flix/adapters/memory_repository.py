import csv

from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.adapters.repository import AbstractRepository

from CS235Flix.domain.movie import Movie, get_movie_hash
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.person import get_person_hash
from CS235Flix.domain.genre import Genre, get_genre_hash

class MemoryRepository(AbstractRepository):
	def __init__(self):
		self.__movie_dict = dict()
		self.__director_dict = dict()
		self.__actor_dict = dict()
		self.__genre_dict = dict()

	def add_movie(self, a_movie):
		self.__movie_dict[hash(a_movie)] = a_movie

	def get_movie(self, title, release_year):
		the_hash = get_movie_hash(title, release_year)
		return self.__movie_dict[the_hash]

	def get_all_movies(self):
		return list(self.__movie_dict.values())

	def add_director(self, a_director):
		self.__director_dict[hash(a_director)] = a_director

	def get_director(self, director_full_name):
		the_hash = get_person_hash(director_full_name)
		return self.__director_dict[the_hash]

	def get_all_directors(self):
		return list(self.__director_dict.values())

	def add_actor(self, a_actor):
		self.__actor_dict[hash(a_actor)] = a_actor

	def get_actor(self, actor_full_name):
		the_hash = get_person_hash(actor_full_name)
		return self.__actor_dict[the_hash]

	def get_all_actors(self):
		return list(self.__actor_dict.values())

	def add_genre(self, a_genre):
		self.__genre_dict[hash(a_genre)] = a_genre

	def get_genre(self, genre_name):
		the_hash = get_genre_hash(genre_name)
		return self.__genre_dict[the_hash]

	def get_all_genres(self):
		return list(self.__genre_dict.values())

def add_movies(a_repo_instance, movie_list):
	for a_movie in movie_list:
		a_repo_instance.add_movie(a_movie)

def add_directors(a_repo_instance, director_list):
	for a_director in director_list:
		a_repo_instance.add_director(a_director)

def add_actors(a_repo_instance, actor_list):
	for a_actor in actor_list:
		a_repo_instance.add_actor(a_actor)

def add_genres(a_repo_instance, genre_list):
	for a_genre in genre_list:
		a_repo_instance.add_genre(a_genre)


def populate(csv_path, a_repo_instance):
	movie_file_csv_reader_object = MovieFileCSVReader(csv_path)
	movie_file_csv_reader_object.read_csv_file()

	movie_list = movie_file_csv_reader_object.dataset_of_movies
	director_list = movie_file_csv_reader_object.dataset_of_directors
	actor_list = movie_file_csv_reader_object.dataset_of_actors
	genre_list = movie_file_csv_reader_object.dataset_of_genres

	add_movies(a_repo_instance, movie_list)
	add_directors(a_repo_instance, director_list)
	add_actors(a_repo_instance, actor_list)
	add_genres(a_repo_instance, genre_list)


