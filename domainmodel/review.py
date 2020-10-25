from datetime import datetime

from domainmodel.movie import Movie

class Review:
    def __init__(self, movie, review_text, rating):
        self.__movie = movie # assuming movie object

        if type(review_text) == str: # assuming they want that
            self.__review_text = review_text
        else:
            self.__review_text = ""


        if rating >= 1 and rating <= 10:
            self.__rating = rating
        else:
            self.__rating = None

        self.__timestamp = datetime.today() # a datatime object contains the data and the time

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        timestamp = self.__timestamp
        return "<Review {} {}, {}, {} ({}-{}-{})>".format(self.__movie.title, self.__movie.release_year, self.__review_text, self.__rating, timestamp.day, timestamp.month, timestamp.year)

    def __eq__(self, other):
        return (self.__movie == other.movie) and (self.__review_text == other.review_text) and (self.__rating == other.rating) and (self.__timestamp == other.timestamp)
