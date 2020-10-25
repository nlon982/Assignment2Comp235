import os

from flask import Flask, render_template

import CS235Flix.adapters.repository as repo
from CS235Flix.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config = None):

	app = Flask(__name__)

	app.config.from_object('config.Config') # config is the module name, Config is the class name whose static variables and their values are to be Flask's configuration variables and values
	data_path = os.path.join('CS235Flix', 'adapters', 'data', 'Data1000Movies.csv')

	if test_config is not None:
		app.config.from_mapping(test_config) # override any configuration variables with these (test_config should be a dictionary)
		data_path = app.config['TEST_DATA_PATH']


	repo.repo_instance = MemoryRepository()
	populate(data_path, repo.repo_instance)

	with app.app_context():
		from .home_blueprint import home
		app.register_blueprint(home.home_blueprint)

		from .movies_blueprint import movies
		app.register_blueprint(movies.movies_blueprint)

	return app