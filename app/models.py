from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),nullable=False,unique=True)
    name = db.Column(db.String,nullable=False)
    is_administrator = db.Column(db.Boolean,default=False)
    is_banned = db.Column(db.Boolean,default=False)
    score = db.Column(db.Integer,default=0)

    def __str__(self):
        return self.name

class Level(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    history = db.Column(db.String)
    age = db.Column(db.String)
    is_male = db.Column(db.Boolean,default=True)
    description = db.Column(db.String)
    history = db.Column(db.String)
    reward = db.Column(db.Integer)
    release_time = db.Column(db.DateTime)

    def __str__(self):
        return self.name

class Mcq(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String)
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='Mcqs')
    stage = db.Column(db.Integer)
    is_unlocking = db.Column(db.Boolean)
    def __str__(self):
        return self.question


class GkQuestion(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String)
    image_uri = db.Column(db.String)
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='gk_questions')
    stage = db.Column(db.Integer)

    def __str__(self):
        return self.question


class McqAnswers(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer = db.Column(db.String)
    mcq_id = db.Column(db.Integer,db.ForeignKey('mcq.id'))
    question = db.relationship(Mcq,backref='answers')
    answer_level = db.Column(db.Integer)

    def __str__(self):
        return self.answer  #+ " --Question:" +self.question.question

class GkAnswer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer = db.Column(db.String)
    gk_id = db.Column(db.Integer,db.ForeignKey('gk_question.id'))
    question = db.relationship(GkQuestion,backref='answers')

    def __str__(self):
        return self.answer

class Progress(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    users = db.relationship(User,backref='progress')
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='level_progress')
    stage = db.Column(db.Integer)
    log = db.Column(db.String)
    completed = db.Column(db.Boolean,default=False)
    is_dead = db.Column(db.Boolean,default=False)


class McqResults(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    result = db.Column(db.String)
    mcq_id = db.Column(db.Integer,db.ForeignKey('mcq.id'))
    question = db.relationship(Mcq,backref='results')
    mcq_answer_id = db.Column(db.Integer,db.ForeignKey('mcq_answers.id'))
    mcq_answer = db.relationship(McqAnswers,backref='result')
    result_level = db.Column(db.Integer)
    is_fatal = db.Column(db.Boolean,default=False)
    fatality_text = db.Column(db.String)

    def __str__(self):
        return self.result

class McqHints(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    hint = db.Column(db.String)
    mcq_id = db.Column(db.Integer,db.ForeignKey('mcq.id'))
    question = db.relationship(Mcq,backref='hints')

    def __str__(self):
        return self.hint

class Conversations(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    conversation = db.Column(db.String)
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='conversations')
    stage = db.Column(db.Integer)

    def __str__(self):
        return self.result

