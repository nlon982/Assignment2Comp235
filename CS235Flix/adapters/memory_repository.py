import csv

import os
from datetime import datetime

from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader
from CS235Flix.adapters.repository import AbstractRepository

from CS235Flix.domain.movie import Movie, get_movie_hash
from CS235Flix.domain.director import Director
from CS235Flix.domain.actor import Actor
from CS235Flix.domain.person import get_person_hash
from CS235Flix.domain.genre import Genre, get_genre_hash

from CS235Flix.domain.user import User
from CS235Flix.domain.review import Review, make_review

from werkzeug.security import generate_password_hash

class MemoryRepository(AbstractRepository):
	def __init__(self):
		self.__movie_dict = dict()
		self.__director_dict = dict()
		self.__actor_dict = dict()
		self.__genre_dict = dict()
		self.__user_list = list()

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

	def add_user(self, user):
		self.__user_list.append(user)

	def get_user(self, user_name):
		return next((user for user in self.__user_list if user.user_name == user_name), None)

	def get_all_users(self):
		return self.__user_list


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


def read_csv_file(csv_path): # a bit of magic
	with open(csv_path, encoding='utf-8-sig') as infile:
		reader = csv.reader(infile)

		# Read first line of the the CSV file.
		headers = next(reader)

		# Read remaining rows from the CSV file.
		for row in reader:
			# Strip any leading/trailing white space from data read.
			row = [item.strip() for item in row]
			yield row


def add_users_to_memory_repository(user_csv_path, a_repo_instance):
	for data_row in read_csv_file(user_csv_path):
		user_name = data_row[1]
		password = data_row[2]
		hashed_password = generate_password_hash(password)
		a_user = User(user_name, hashed_password)
		a_repo_instance.add_user(a_user)


def add_reviews_to_memory_repository(review_csv_path, a_repo_instance): # this assumes movies and users are already loaded in to the repository
	# also note, reviews don't exist standalone in the repostitory (they are stored with the user who made the review, and the movie)
	for data_row in read_csv_file(review_csv_path):
		user_name = data_row[0]
		movie_title = data_row[1]
		movie_release_year = data_row[2]
		a_user = a_repo_instance.get_user(user_name)
		if a_user is None:
			raise Exception("User: {} does not exist in the repository for a review to be made".format(user_name))
		a_movie = a_repo_instance.get_movie(movie_title, movie_release_year)
		if a_movie is None:
			raise Exception("The movie: {} ({}) does not exist in the repository for a review to be made".format(movie_title, movie_release_year))

		review_text = data_row[3]
		rating = float(data_row[4])
		timestamp = datetime.fromisoformat(data_row[5])

		make_review(a_user, a_movie, review_text, rating, timestamp) # this function is always called to store the review in both the user and movie


def populate(data_path, a_repo_instance):
	movie_csv_path = os.path.join(data_path, 'Data1000Movies.csv')
	user_csv_path = os.path.join(data_path, 'users.csv')
	review_csv_path = os.path.join(data_path, 'reviews.csv')

	movie_file_csv_reader_object = MovieFileCSVReader(movie_csv_path)
	movie_file_csv_reader_object.read_csv_file()

	movie_list = movie_file_csv_reader_object.dataset_of_movies
	director_list = movie_file_csv_reader_object.dataset_of_directors
	actor_list = movie_file_csv_reader_object.dataset_of_actors
	genre_list = movie_file_csv_reader_object.dataset_of_genres

	add_movies(a_repo_instance, movie_list)
	add_directors(a_repo_instance, director_list)
	add_actors(a_repo_instance, actor_list)
	add_genres(a_repo_instance, genre_list)

	add_users_to_memory_repository(user_csv_path, a_repo_instance)

	add_reviews_to_memory_repository(review_csv_path, a_repo_instance)