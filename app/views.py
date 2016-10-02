from app import lm,db,app
from flask import render_template,redirect,url_for,flash,request
from flask_login import login_required,current_user,login_user,logout_user
from .models import User
from .oauth import OAuthSignIn
from .forms import LoginForm

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/',methods=['GET','POST'])
def index():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		return redirect(url_for('oauth_authorize',provider=login_form.provider.data))
	return render_template('index.html',login_form=login_form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

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
		user = User(name=username,email=email,level=1)
		db.session.add(user)
		db.session.commit()
	login_user(user,True)
	flash('authentication successful')
	return redirect(url_for('index'))
