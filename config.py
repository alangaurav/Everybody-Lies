import os

WTF_CSRF_TOKEN = True
SECRET_KEY = 'b4bbdd1d71007193efcb3895ac08b5d32736832f7aaa18e6'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'test.db') #postgresql://epsilon:racingiscool@localhost:5432/eldb'    #'mysql+pymysql://epsilon:housemd@localhost/app_db' #sqlite:///'+os.path.join(basedir,'test.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repositrory')

OAUTH_CREDENTIALS = {
	"google":{
		"client_id":'542603804553-qkgq3j3mmifvlgnm4gsrtpl2h8murtf9.apps.googleusercontent.com',
		"client_secret":'ctR05-N2-stHfT7XWiwWuPV6'
	},
	"facebook":{
		"client_id":'blah',
		"client_secret":"blah"
	}
}
