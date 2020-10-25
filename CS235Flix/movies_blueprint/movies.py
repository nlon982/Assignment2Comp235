from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import CS235Flix.movies_blueprint.services as services

import CS235Flix.adapters.repository as repo

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/browse', methods=['GET'])
def browse():
    repo_instance = repo.repo_instance
    movie_dict_list = services.get_movies(repo_instance)
    return render_template('movies/movies.html', movie_dict_list = movie_dict_list)

@movies_blueprint.route('/movie_page', methods=['GET'])
def movie_page():
    movie_title = request.args.get('title')
    return "This is the page for: {}".format(movie_title)

