from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
	__tablename__='users'
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(64),nullable=False,unique=True)
	name = db.Column(db.String(64),nullable=False)
	level = db.Column(db.Integer)
	stage = db.Column(db.Integer)


class Level(db.Model):
	id = db.Column(db.Integer,primary_key=True)




class Mcq(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
	level = db.relationship(Level,backref='mcqs')
	stage = db.Column(db.Integer,nullable=False)
	question = db.Column(db.String)
	good_option = db.Column(db.String,nullable=False)
	moderate_option = db.Column(db.String,nullable=False)
	bad_option = db.Column(db.String,nullable=False)




class GkQuestion(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
	level = db.relationship(Level,backref='gk_questions')
	stage = db.Column(db.Integer,nullable=False)
	question = db.Column(db.String,nullable=False)
	answer = db.Column(db.String,nullable=False)


class Event(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
	level = db.relationship(Level,backref='events')
	stage = db.Column(db.Integer,nullable=False)
	question = db.Column(db.String,nullable=False)
	option_1 = db.Column(db.String,nullable=False)
