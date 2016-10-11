import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)
db = SQLAlchemy(app)
admin = Admin(app,name='Everybody_Lies',template_mode='bootstrap3')


from app import views,models
admin.add_view(ModelView(models.User,db.session))
admin.add_view(ModelView(models.Level,db.session))
admin.add_view(ModelView(models.Mcq,db.session))
admin.add_view(ModelView(models.McqAnswers,db.session))
admin.add_view(ModelView(models.GkQuestion,db.session))
admin.add_view(ModelView(models.GkAnswer,db.session))
admin.add_view(ModelView(models.McqResults,db.session))
admin.add_view(ModelView(models.Progress,db.session))
admin.add_view(ModelView(models.McqHints,db.session))