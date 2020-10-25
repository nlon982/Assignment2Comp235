from CS235Flix.adapters.movie_file_csv_reader import MovieFileCSVReader

class TestMovieFileCSVReader:
    def test_read_csv_file(self):
        movie_file_csv_reader_object = MovieFileCSVReader(r"C:\Users\Nathan Longhurst\OneDrive - The University of Auckland\b Comp235\Assignment\GitHub Clone (Current)\CS235FlixSkeleton\datafiles\Data1000Movies.csv")
        movie_file_csv_reader_object.read_csv_file()

        dataset_of_movies = movie_file_csv_reader_object.dataset_of_movies
        dataset_of_actors = movie_file_csv_reader_object.dataset_of_actors
        dataset_of_directors = movie_file_csv_reader_object.dataset_of_directors
        dataset_of_genres = movie_file_csv_reader_object.dataset_of_genres

        assert len(dataset_of_movies) == 1000
        assert len(set(dataset_of_actors)) == len(dataset_of_actors) # check unique items only
        assert len(set(dataset_of_directors)) == len(dataset_of_directors)  # ^ ditto
        assert len(set(dataset_of_genres)) == len(dataset_of_genres)  # ^ ditto
