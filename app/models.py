from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),nullable=False,unique=True)
    name = db.Column(db.String(64),nullable=False)
    registration_number = db.Column(db.String(15))
    college_name = db.Column(db.String(50))
    is_administrator = db.Column(db.Boolean,default=False)
    is_banned = db.Column(db.Boolean,default=False)
    score = db.Column(db.Integer,default=0)

    def __str__(self):
        return self.name

class Level(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.String(10))
    is_male = db.Column(db.Boolean,default=True)
    occupation = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    history = db.Column(db.String(2000))
    reward = db.Column(db.Integer)
    is_active = db.Column(db.Boolean,default=False)

    def __str__(self):
        return self.name

class Mcq(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(500))
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='Mcqs')
    stage = db.Column(db.Integer)
    is_unlocking = db.Column(db.Boolean)
    is_end = db.Column(db.Boolean)
    def __str__(self):
        return self.question


class GkQuestion(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(500))
    image_uri = db.Column(db.String(1000))
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='gk_questions')
    stage = db.Column(db.Integer)
    is_unlocking = db.Column(db.Boolean)
    def __str__(self):
        return self.question


class McqAnswers(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer = db.Column(db.String(100))
    mcq_id = db.Column(db.Integer,db.ForeignKey('mcq.id'))
    question = db.relationship(Mcq,backref='answers')
    answer_level = db.Column(db.Integer)

    def __str__(self):
        return self.answer  #+ " --Question:" +self.question.question

class GkAnswer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    answer = db.Column(db.String(500))
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
    log = db.Column(db.String(5000))
    completed = db.Column(db.Boolean,default=False)
    is_dead = db.Column(db.Boolean,default=False)


class McqResults(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    result = db.Column(db.String(500))
    mcq_id = db.Column(db.Integer,db.ForeignKey('mcq.id'))
    question = db.relationship(Mcq,backref='results')
    mcq_answer_id = db.Column(db.Integer,db.ForeignKey('mcq_answers.id'))
    mcq_answer = db.relationship(McqAnswers,backref='result')
    result_level = db.Column(db.Integer)
    is_fatal = db.Column(db.Boolean,default=False)
    fatality_text = db.Column(db.String(500))

    def __str__(self):
        return self.result

class McqHints(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    hint = db.Column(db.String(500))
    mcq_id = db.Column(db.Integer,db.ForeignKey('mcq.id'))
    question = db.relationship(Mcq,backref='hints')

    def __str__(self):
        return self.hint

class Conversations(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    conversation = db.Column(db.String(500))
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='conversations')
    stage = db.Column(db.Integer)
    def __str__(self):
        return self.result

class LevelEnd(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    diagnosis = db.Column(db.String(500))
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='diagnosis')
    stage = db.Column(db.Integer)

class Event(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(1000))
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    level = db.relationship(Level,backref='events')
    stage = db.Column(db.Integer)

class FirstTry(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    db.relationship(User,backref='firstries')
    level_id = db.Column(db.Integer,db.ForeignKey('level.id'))
    db.relationship(Level,backref='firstriess')
    stage = db.Column(db.Integer)
    is_first_try = db.Column(db.Boolean,default=True)