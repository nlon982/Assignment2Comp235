from os import environ

from dotenv import load_dotenv

load_dotenv() # store configuration variables named in the '.env' ile (which it is very good at finding in to the os's environment)

class Config():
	# store configuration variables (under the same name static variables), getting them from the os's environment
	FLASK_APP = environ.get('FLASK_APP')
	FLASK_ENV = environ.get('FLASK_ENV')

	SECRET_KEY = environ.get("SECRET_KEY")
	TESTING = environ.get("TESTING")