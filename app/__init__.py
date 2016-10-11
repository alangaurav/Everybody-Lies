import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)
db = SQLAlchemy(app)
admin = Admin(app,name='Everybody_Lies',template_mode='bootstrap3')


from app import views,models
class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_administrator
admin.add_view(MyView(models.User,db.session))
admin.add_view(MyView(models.Level,db.session))
admin.add_view(MyView(models.Mcq,db.session))
admin.add_view(MyView(models.McqAnswers,db.session))
admin.add_view(MyView(models.GkQuestion,db.session))
admin.add_view(MyView(models.GkAnswer,db.session))
admin.add_view(MyView(models.McqResults,db.session))
admin.add_view(MyView(models.Progress,db.session))
admin.add_view(MyView(models.McqHints,db.session))
admin.add_view(MyView(models.Event,db.session))
admin.add_view(MyView(models.LevelEnd,db.session))