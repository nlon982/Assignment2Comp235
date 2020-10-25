import csv
import os

from domainmodel.movie import Movie
from domainmodel.actor import Actor
from domainmodel.genre import Genre
from domainmodel.director import Director


def get_list_from_comma_string(a_string):  # I could do this in one line, but decided to be clear instead
    a_list = a_string.split(",")
    a_tidy_list = [item.strip() for item in a_list]  # remove trailing spaces
    return a_tidy_list






class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name

        # None is good because it's indicative of not reading the csv_file yet
        self.__dataset_of_movies = None
        self.__dataset_of_actors = None
        self.__dataset_of_directors = None
        self.__dataset_of_genres = None

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    def check_csv_file(self):
        #----------- Define some function (objects)

        def check_title_validity(a_title):
            return a_title != "" and len(a_title) < 100

        def check_genre_validity(a_genre):
            return a_genre != "" and len(a_genre) < 50

        def check_description_validity(a_description):
            return a_description != "" and len(a_description.split(" ")) < 100

        def check_director_validity(a_director):
            return a_director != "" and len(a_director) < 40

        def check_actor_validity(a_actor):
            return len(a_actor.split(",")) >= 1

        def check_year_validity(a_year):
            try:  # so we don't throw an error if can't be converted to int
                return int(a_year) >= 1900  # as per code runner requirement
            except:
                return False

        def check_runtime_validity(a_runtime):
            try:
                return int(a_runtime) > 0  # ditto to above
            except:
                return False

        def check_rating_validity(a_rating):
            try:
                a_rating_float = float(a_rating)
                return a_rating_float >= 0 and a_rating_float <= 10  # ditto to above
            except:
                return False

        def check_votes_validity(a_vote_count):
            try:
                a_vote_count_int = int(a_vote_count)
                return a_vote_count_int >= 0  # ditto to above
            except:
                return False
            # There's also the check that it the rating (given by votes)
            # if the vote count is 0, has to be N/A. Ignoring

        def check_revenue_validity(a_revenue):
            try:
                return float(a_revenue) > 0  # ditto to above
            except:
                return False

        def check_metascore_validity(a_metascore):
            try:
                a_metascore = int(a_metascore)
                return a_metascore >= 0  # ditto to above
            except:
                return False

        #------------- Setup dictionary mapping Column names to the above validity functions
        valid_input_dict = dict()
        valid_input_dict["Title"] = check_title_validity
        valid_input_dict["Genre"] = check_genre_validity
        valid_input_dict["Description"] = check_description_validity
        valid_input_dict["Director"] = check_director_validity
        valid_input_dict["Actors"] = check_actor_validity
        valid_input_dict["Year"] = check_year_validity
        valid_input_dict["Runtime (Minutes)"] = check_runtime_validity
        valid_input_dict["Rating"] = check_rating_validity
        valid_input_dict["Votes"] = check_votes_validity
        valid_input_dict["Revenue (Millions)"] = check_revenue_validity
        valid_input_dict["Metascore"] = check_metascore_validity


        unclean_dict = dict()
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            row_index = 0
            # note movie_file_reader is a dict of rows (which are dicts)
            for row_dict in movie_file_reader:

                for column_name in row_dict.keys():
                    try: # i.e. if there is no validity function for that particular column, move on
                        validity_function = valid_input_dict[column_name]
                    except:
                        pass
                    else: # I believe this is the correct way to use a try/except/else
                        cell_value = row_dict[column_name]

                        if cell_value == "N/A":
                            validity_bool = True
                        else:
                            validity_bool = validity_function(cell_value)

                        if validity_bool == False:
                            if row_index not in unclean_dict.keys(): # no unclean columns in this row yet
                                unclean_dict[row_index] = [column_name]
                            else:
                                unclean_dict[row_index].append(column_name)
                            #raise ValueError("'{}' does not meet requirements for '{}'".format(cell_value, column_name))

                row_index += 1

        if len(unclean_dict.keys()) > 0:
            return unclean_dict
        else:
            return None


    def clean_csv_file(self, unclean_dict): # unclean_dict retrieved from check_csv_file
        if unclean_dict != None: # i.e. don't go to the effort of writing to a new CSV unless there's something unclean

            old_file_name = self.__file_name # more like, old file path
            base, file_extension = os.path.splitext(old_file_name)
            new_file_name = base + "_clean" + file_extension # more like, new file path

            with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile_old:
                with open(new_file_name, mode='w', encoding='utf-8-sig', newline='') as csvfile_new: # the newline parameter is because it was creating blank lines
                    old_movie_file_reader = csv.DictReader(csvfile_old)
                    fieldnames = old_movie_file_reader.fieldnames
                    new_movie_file_writer = csv.DictWriter(csvfile_new, fieldnames)

                    new_movie_file_writer.writeheader() # have the first row to be the fieldnames (aka column names)

                    row_index = 0
                    for row_dict in old_movie_file_reader:


                        if row_index in unclean_dict.keys():
                            new_row_dict = dict() # construct new row dict that's a mesh of new an old

                            for column_name in row_dict.keys():
                                if column_name in unclean_dict[row_index]:
                                    new_row_dict[column_name] = "N/A"
                                else:
                                    new_row_dict[column_name] = row_dict[column_name]

                            new_movie_file_writer.writerow(new_row_dict)

                        else:
                            new_movie_file_writer.writerow(row_dict)

                        row_index += 1
        return new_file_name



    def read_csv_file(self):
        # this assumes there aren't repeated actors, genres, or movies (i.e. not a entry with same: release year and movie title)

        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            self.__dataset_of_movies = list()
            self.__dataset_of_actors = list()
            self.__dataset_of_directors = list()
            self.__dataset_of_genres = list()

            index = 0
            for row in movie_file_reader:
                title = row['Title'].strip() # stripping to safe
                release_year = int(row['Year'])
                actor_full_name_list = get_list_from_comma_string(row['Actors'])
                director_full_name = row['Director'].strip() # stripping to safe
                genre_name_list =  get_list_from_comma_string(row['Genre'])

                #- other things
                rank = int(row['Rank'])
                description = row['Description']
                runtime_minutes = int(row['Runtime (Minutes)'])
                external_rating = float(row['Rating'])
                external_rating_votes = int(row['Votes'])

                # These require try/except because some values are N/A's (preferably all would but it's SUPER ugly code)
                try:
                    revenue = float(row['Revenue(Millions)'])
                except:
                    revenue = None
                try:
                    metascore = int(row['Metascore'])
                except:
                    metascore = None

                #-------- Make Actor, Director and Genre Objects
                actor_object_list = [Actor(actor_full_name) for actor_full_name in actor_full_name_list]
                # add actor colleagues, who are the actors who are in the movie with them (i.e. add all other actors to colleagues for all actors)
                for actor in actor_object_list:
                    for potential_actor_colleague in actor_object_list: # potential because one of them is them
                        if actor != potential_actor_colleague:
                            actor.add_actor_colleague(potential_actor_colleague)

                director_object = Director(director_full_name)
                genre_object_list = [Genre(genre_name) for genre_name in genre_name_list]

                #-------- Create and set up Movie Object
                movie_object = Movie(title, release_year)
                movie_object.actors = actor_object_list # thanks to my setter implementation
                movie_object.director = director_full_name
                movie_object.genres = genre_object_list # ^ ditto
                movie_object.release_year = release_year

                #- other things
                movie_object.description = description
                movie_object.runtime_minutes = runtime_minutes
                movie_object.external_rating = external_rating
                movie_object.external_rating_votes = external_rating_votes
                if revenue != None:
                    movie_object.revenue = revenue
                if metascore != None:
                    movie_object.metascore = metascore

                #-------- Take all the above information, and add to datasets
                self.__dataset_of_movies.append(movie_object) # the assumption is that each row in the csv is a unique movie

                # I could create a function that adds unique things to lists only, nvm
                for actor_object in actor_object_list:
                    if actor_object not in  self.__dataset_of_actors:
                        self.__dataset_of_actors.append(actor_object)

                if director_object not in self.__dataset_of_directors:
                    self.__dataset_of_directors.append(director_object)

                for genre_object in genre_object_list:
                    if genre_object not in self.__dataset_of_genres:
                        self.__dataset_of_genres.append(genre_object)

                index += 1


# To test my assigmnent, run the following lines of code (I have copy and pasted these in my test_all.py file too)

#movie_file_csv_reader_object = MovieFileCSVReader(r"C:\Users\Nathan Longhurst\OneDrive - The University of Auckland\b Comp235\Assignment\GitHub Clone (Current)\CS235FlixSkeleton\datafiles\Data1000Movies.csv")
#unclean_dict = movie_file_csv_reader_object.check_csv_file()
#movie_file_csv_reader_object.clean_csv_file(unclean_dict)