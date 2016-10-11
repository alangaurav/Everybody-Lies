from app import lm,app,db
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_required,current_user,login_user,logout_user
from random import shuffle
from .models import User,Level,Progress
from .oauth import OAuthSignIn
from .forms import LoginForm,McqForm,SubmitField,GkForm
import re,string


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
    #gk_forms = 
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
        new_progress = Progress(user_id=current_user.id,level_id=patient.id,stage=1)
        db.session.add(new_progress)
        db.session.commit()
    all_level_progress = patient.level_progress
    print all_level_progress
    for progress in all_level_progress:
        if(progress.level_id == patient.id):
            current_progress = progress
    
    return redirect(url_for('treat',patient_name=patient_name,stage=current_progress.stage))

@app.route('/treat/<patient_name>/<stage>',methods=['GET','POST'])
def treat(patient_name,stage):
    print "We'ere back"
    patient = Level.query.filter_by(name=patient_name).first()
    progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()
    gk_form = GkForm()
    options = []
    for mcq in patient.Mcqs:
        if mcq.stage == int(stage):
            options = [(i,option) for i,option in enumerate(mcq.answers)]

    gk_question = None
    for gk in patient.gk_questions:
        if gk.stage == int(stage):
            gk_question = gk
    mcq_form = McqForm()
    mcq_form.options.choices = options

    print mcq_form.is_submitted()
    if mcq_form.validate_on_submit():
        if progress.log is None:
            progress.log = ""
        for mcq in patient.Mcqs:
            if mcq.stage == int(stage):
                for mcq_answer in mcq.answers:
                    if mcq_answer.answer_level == 1:
                        print mcq_answer
                        print mcq_answer.result
                        print mcq_answer.result[0].result
                        progress.log += mcq_answer.result[0].result + "|"
                        if progress.stage == mcq.stage:
                            current_user.score += 2
                        progress.stage += 1
                        db.session.commit()
                        return redirect(url_for('treat',patient_name=patient_name,stage=stage))

                    if mcq_answer.answer_level == 2:
                        progress.log = patient.log + mcq_answer.result[0].result + "|"
                        if progress.stage == mcq.stage:
                            current_user.score += 1
                        progress.stage += 1
                        db.session.commit()
                        return redirect(url_for('treat',patient_name=patient_name,stage=stage))

                    if mcq_answer.answer_level == 3:
                        progress.log += mcq_answer.result[0].result + "|"
                        if progress.stage == mcq.stage:
                            current_user.score -= 1
                        progress.stage += 1
                        db.session.commit()
                        return redirect(url_for('treat',patient_name=patient_name,stage=stage))

    if gk_form.validate_on_submit():
        print "VALIDATING"
        answer = gk_form.answer.data
        correct = gk_question.answers[0].answer
        answer = answer.replace(' ','')
        correct = correct.replace(' ','')
        print answer
        print correct
        if answer.lower() == correct.lower():
            current_user.score += 20
            db.session.commit()
            return redirect(url_for('treat',patient_name=patient_name,stage=str(int(stage)+1)))
        else:
            flash("Incorrect answer")
            return redirect(url_for('treat',patient_name=patient_name,stage=stage))


    for mcq in patient.Mcqs:
        if mcq.stage == int(stage):
            return render_template('mcq.html',mcq=mcq,mcq_form=mcq_form,patient_name=patient_name,stage=stage)

    for gk in patient.gk_questions:
        if gk.stage == int(stage.strip()):
            qk_question = gk
            return render_template('gk.html',gk=gk,gk_form=gk_form)




@app.route('/treat/<patient_name>/<stage>/<answer>')
def post_treat(patient_name,stage,answer):
    patient = Level.query.filter_by(name=patient_name).first()
    progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()
    if progress is None:
        return "ERROR"
    patient = Level.query.filter_by(name=patient_name).first()
    for mcq in patient.Mcqs:
        print stage
        if mcq.stage == -1:
            for mcq_answer in mcq.answers:
                if answer == mcq_answer.answer:
                    if(mcq_answer.answer_level == 1):
                        progress.log += mcq_answer.result[0] + "|"
                        if progress.stage == mcq.stage:
                            current_user.score += 10
                        progress.stage+=1
                        return redirect(url_for('pre_treat',patient_name=patient_name))
                    elif(mcq_answer.answer_level == 2):
                        progress.log += mcq_answer.result[0] + "|"
                        if progress.stage == mcq.stage:
                            current_user.score += 5
                        progress.stage+=1
                        return redirect(url_for('pre_treat',patient_name=patient_name))
                    elif(mcq_answer.answer_level ==3):
                        progress.log += mcq_answer.result[0] + "|"
                        if progress.stage == mcq.stage:
                            current_user.score -= 5
                        progress.stage+=1
                        return redirect(url_for('pre_treat',patient_name=patient_name))

    return redirect(url_for('pre_treat',patient_name=patient_name))


@app.route('/rules')
def rules():
    return render_template('rules.html')


