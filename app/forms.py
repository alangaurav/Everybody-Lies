from flask_wtf import Form
from wtforms import StringField,SubmitField,RadioField,SelectField
from wtforms.validators import DataRequired

class LoginForm(Form):
    provider = StringField('Enter the provider',validators=[DataRequired()])
    submit = SubmitField('Submit')


class GkForm(Form):
    answer = StringField('Enter your answer',validators=[DataRequired()])
    submit = SubmitField('Submit')

class GkSkipForm(Form):
    submit = SubmitField('Skip')

class McqForm(Form):
    options = RadioField(choices=[],coerce=int)
    skip = SubmitField('Skip')
    submit = SubmitField('Submit')

class EndForm(Form):
    diagnosis = StringField('Enter',validators=[DataRequired()])
    submit = SubmitField('Submit')

class EventForm(Form):
    hid = StringField()
    submit = SubmitField('Next')

class DetailsForm(Form):
    registration_number = StringField('Enter your registration number',validators=[DataRequired()])
    college_name = StringField('Enter College Name',validators=[DataRequired()])