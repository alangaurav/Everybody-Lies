import os

WTF_CSRF_TOKEN = True
SECRET_KEY = 'b4bbdd1d71007193efcb3895ac08b5d32736832f7aaa18e6'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://epsilon:housemd@localhost/app_db' #'sqlite:///'+os.path.join(basedir,'test.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repositrory')

OAUTH_CREDENTIALS = {
	"google":{
		"client_id":'542603804553-k8ivsqbsbk5ji24epr0mng8849j1732r.apps.googleusercontent.com',
		"client_secret":'dVSTYwRgih_Vhedhv10ltz-p'
	},
	"facebook":{
		"client_id":'blah',
		"client_secret":"blah"
	}
}
