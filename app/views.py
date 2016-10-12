from app import lm,app,db
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_required,current_user,login_user,logout_user
from random import shuffle
from .models import User,Level,Progress,FirstTry
from .oauth import OAuthSignIn
from .forms import LoginForm,McqForm,SubmitField,GkForm,GkSkipForm,EventForm,EndForm,DetailsForm
import re,string


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        return redirect(url_for('oauth_authorize',provider=login_form.provider.data))

    return render_template('comingsoon.html',login_form=login_form)

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
    if current_user.registration_number is None:
        return redirect(url_for('details'))
    return redirect(url_for('index'))

@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    patients = Level.query.all()
    return render_template('index.html',patients=patients)


@app.route('/treat/<patient_name>/')
@login_required
def pre_treat(patient_name):
    patient = Level.query.filter_by(name=patient_name).first()
    progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()
    if progress is None:
        new_progress = Progress(user_id=current_user.id,level_id=patient.id,stage=1,log="Begin Consultations|")
        db.session.add(new_progress)
        db.session.commit()
        progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()

    return redirect(url_for('treat',patient_name=patient_name,stage=progress.stage))


@app.route('/treat/<patient_name>/<stage>',methods=['GET','POST'])
@login_required
def treat(patient_name,stage):

    print "We'ere back"
    event_form = EventForm()
    patient = Level.query.filter_by(name=patient_name).first()
    progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()
    if progress is None:
        return redirect(url_for('pre_treat',patient_name=patient_name))

    progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()
    if progress.completed:
        return redirect(url_for('success'))
    first_try = FirstTry.query.filter_by(user_id=current_user.id,level_id=patient.id,stage=stage).first()
    if first_try is None:
        first_try = FirstTry(user_id=current_user.id,level_id=patient.id,stage=stage)
        db.session.add(first_try)
        db.session.commit()

    first_try = FirstTry.query.filter_by(user_id=current_user.id,level_id=patient.id,stage=stage).first()
    logs = progress.log
    if logs is not None:
        logs = logs.split('|')
    if progress.is_dead:
        return render_template('dead.html',logs=logs)
    if progress.stage < int(stage):
        return redirect(url_for('treat',patient_name=patient_name,stage=progress.stage))
    gk_form = GkForm()
    gk_skip_form = GkSkipForm()
    end_form = EndForm()
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

   

    if end_form.validate_on_submit():
        print "END VALIDATING"
        correct = patient.diagnosis[0].diagnosis
        answer = end_form.diagnosis.data
        answer = answer.replace(' ','')
        correct = correct.replace(' ','')
        if answer.lower() == correct.lower():
            current_user.score += patient.reward
            progress.completed = True
            db.session.commit()
            return redirect(url_for('success'))
        else:
            flash("Incorrect Diagnosis")
            return redirect(url_for('pre_treat',patient_name=patient_name))
    print "MCQ FORM"
    print mcq_form.is_submitted()
    if mcq_form.validate_on_submit():
        print "IN MCQ FORM"
        for mcq in patient.Mcqs:
            if mcq.stage == int(stage):
                for mcq_answer in mcq.answers:
                    print "NAME"
                    correct = dict(options).get(mcq_form.options.data)
                    if correct == mcq_answer:
                        if mcq_answer.answer_level == 1:
                            progress.log += str(mcq_answer.result[0].result) + "|"
                            db.session.commit()
                            if progress.stage == mcq.stage:
                                if first_try.is_first_try:
                                    current_user.score += 20
                                    db.session.commit()
                                progress.stage += 1
                                db.session.commit()
                            return redirect(url_for('pre_treat',patient_name=patient_name,stage=progress.stage))

                        if mcq_answer.answer_level == 2:
                            progress.log = str(patient.log + mcq_answer.result[0].result) + "|"
                            if mcq_answer.result[0].is_fatal:
                                progress.is_dead = True
                                progress.log = progress.log + mcq_answer.result[0].fatality_text + "|"
                                db.session.commit()
                            db.session.commit()
                            if progress.stage == mcq.stage:
                                if first_try.is_first_try:
                                    current_user.score += 10
                                    first_try.is_first_try = False
                                    db.session.commit()
                            return redirect(url_for('treat',patient_name=patient_name,stage=stage))

                        if mcq_answer.answer_level == 3:
                            progress.log += str(mcq_answer.result[0].result) + "|"
                            if mcq_answer.result[0].is_fatal:
                                progress.is_dead = True
                                progress.log = progress.log + mcq_answer.result[0].fatality_text + "|"
                                db.session.commit()
                            db.session.commit()
                            if progress.stage == mcq.stage:
                                if first_try.is_first_try:
                                    current_user.score -= 10
                                    first_try.is_first_try = False
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
            if progress.stage == int(stage):
                current_user.score += 20
                progress.stage += 1
                db.session.commit()
            return redirect(url_for('treat',patient_name=patient_name,stage=str(int(stage)+1)))
        else:
            flash("Incorrect answer")
            return redirect(url_for('treat',patient_name=patient_name,stage=stage))

    print "GK SKIP FORM"
    print gk_skip_form.is_submitted()
    if gk_skip_form.validate_on_submit():
        if progress.stage == int(stage):
            progress.stage += 1
            db.session.commit()
        return redirect(url_for('pre_treat',patient_name=patient_name))


    for mcq in patient.Mcqs:
        if mcq.stage == int(stage):
            return render_template('mcq.html',mcq=mcq,mcq_form=mcq_form,patient_name=patient_name,stage=stage,progress=progress,logs=logs,patient=patient)

    for gk in patient.gk_questions:
        if gk.stage == int(stage.strip()):
            qk_question = gk
            return render_template('gk.html',gk=gk,gk_form=gk_form,gk_skip_form=gk_skip_form,progress=progress,stage=stage,patient_name=patient_name,patient=patient)

    for event in patient.events:
        if event.stage == int(stage):
            return render_template('event.html',event=event,event_form=event_form,patient_name=patient_name,stage=stage,progress=progress,logs=logs,patient=patient)

    for diagnosis in patient.diagnosis:
        if diagnosis.stage == int(stage):
            return render_template('end.html',end_form=end_form)

@app.route('/submit/event/<patient_name>/<stage>')
def cont_stage(patient_name,stage):
    patient = Level.query.filter_by(name=patient_name).first()
    progress = Progress.query.filter_by(user_id=current_user.id,level_id=patient.id).first()
    for event in patient.events:
        if event.stage == int(stage):
            progress.stage += 1
            db.session.commit()
            return redirect(url_for('pre_treat',patient_name=patient_name))

    return redirect(url_for('pre_treat',patient_name=patient_name))

@app.route('/details',methods=['GET','POST'])
@login_required
def details():
    details_form = DetailsForm()
    if details_form.validate_on_submit():
        current_user.registration_number = details_form.registration_number.data
        current_user.college_name = details_form.college_name.data
        db.session.commit()
        return redirect(url_for('index'))
    return(render_template('details.html',details_form=details_form))


@app.route('/rules')
@login_required
def rules():
    return render_template('rules.html')

@app.route('/completed')
@login_required
def success():
    return render_template('success.html')

@app.route('/dead')
@login_required
def dead():
    return render_template('dead.html')

@app.route('/leaders')
@login_required
def leaderboard():
    users = User.query.order_by(User.score.desc()).limit(50)
    return render_template('leaderboard.html',users=users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

