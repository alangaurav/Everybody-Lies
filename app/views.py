from app import lm,app,db
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_required,current_user,login_user,logout_user
from random import shuffle
from .models import User,Level,Progress
from .oauth import OAuthSignIn
from .forms import LoginForm

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        return redirect(url_for('oauth_authorize',provider=login_form.provider.data))

    return render_template('login.html',login_form=login_form)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username,email = oauth.callback()
    if username is None:
        flash('authentication failed')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=username,email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user,True)
    flash('authentication successful')
    return redirect(url_for('index'))


@app.route('/index',methods=['GET','POST'])
def index():
    patients = Level.query.all()
    return render_template('index.html',patients=patients)

@app.route('/treat/<patient_name>/')
def pre_treat(patient_name):
    print patient_name
    patient = Level.query.filter_by(name=patient_name).first()
    print patient
    all_level_progress = patient.level_progress
    current_progress = None
    print 'Done'
    if all_level_progress == []:
        print 'In Functions'
        new_progress = Progress(user_id=current_user.id,level_id=patient.id,stage=1)
        db.session.add(new_progress)
        db.session.commit()
    all_level_progress = patient.level_progress
    print all_level_progress
    for progress in all_level_progress:
        if(progress.level_id == patient.id):
            current_progress = progress
    
    return redirect(url_for('treat',patient_name=patient_name,stage=current_progress.stage))

@app.route('/treat/<patient_name>/<stage>')
def treat(patient_name,stage):
    patient = Level.query.filter_by(name=patient_name).first()
    for mcq in patient.Mcqs:
        if mcq.stage == int(stage):
            return render_template('tests.html',mcq=mcq)

