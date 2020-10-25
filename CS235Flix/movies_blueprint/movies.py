from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


import CS235Flix.movies_blueprint.services as services

import CS235Flix.adapters.repository as repo
from CS235Flix.authentication_blueprint.authentication import login_required
from CS235Flix.domain.movie import Movie, get_movie_hash

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/browse', methods=['GET'])
def browse():
    repo_instance = repo.repo_instance
    movie_dict_list = services.get_movies(repo_instance)

    for a_movie_dict in movie_dict_list:
        a_movie_dict['add_review_url'] = url_for('movies_bp.review_movie', title = a_movie_dict["title"], release_year = a_movie_dict["release_year"])

    return render_template('movies/movies.html', movie_dict_list = movie_dict_list)

@movies_blueprint.route('/movie_page', methods=['GET'])
def movie_page():
    movie_title = request.args.get('title')
    return "This is the page for: {}".format(movie_title)



@movies_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def review_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie_title = form.movie_title.data
        movie_release_year = form.movie_release_year.data

        # Use the service layer to store the new comment.
        services.add_movie(movie_title, movie_release_year, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        a_movie_dict = services.get_movie(movie_title, movie_release_year, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movies_bp.articles_by_date', date=article['date'], view_comments_for=movie_hash))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_title = request.args.get('title')
        movie_release_year = int(request.args.get('release_year'))

        # Store the article id in the form.
        form.movie_title.data = movie_title
        form.movie_release_year.data = movie_release_year
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_title = form.movie_title.data
        movie_release_year = form.movie_release_year.data

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    a_movie_dict = services.get_movie(movie_title, movie_release_year, repo.repo_instance)
    return render_template(
        'movies/review_movie.html',
        title='Edit article',
        a_movie_dict = a_movie_dict,
        form=form,
        handler_url=url_for('movies_bp.comment_on_article')
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_title = HiddenField("Movie title")
    movie_release_year = HiddenField("Movie release year")
    submit = SubmitField('Submit')