from flask_wtf import Form
from wtforms import StringField,SubmitField,RadioField,SelectField
from wtforms.validators import DataRequired

class LoginForm(Form):
    provider = StringField('Enter the provider',validators=[DataRequired()])
    submit = SubmitField('Submit')


class GkForm(Form):
    answer = StringField('Enter your answer',validators=[DataRequired()])
    submit = SubmitField('Submit')

class McqForm(Form):
    options = RadioField(choices=[],coerce=int)
    submit = SubmitField('Submit')