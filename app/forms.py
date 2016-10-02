from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Required



class LoginForm(Form):
	provider = StringField('Enter the provider',validators=[DataRequired()])
	submit = SubmitField('Submit')