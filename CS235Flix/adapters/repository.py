import abc

repo_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_movie(self, a_movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title, release_year):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, a_director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_directors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, a_actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_actors(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, a_genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_genres(self):
        raise NotImplementedError

# todo, account for users, reviews, etc.