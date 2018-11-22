from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fulcrumportal.models import User 

class WeekDayAvail(FlaskForm):
    name = StringField('Enter name here...', validators=[DataRequired()])
    sunday = BooleanField('Sunday')
    monday = BooleanField('Monday')
    tuesday = BooleanField('Tuesday')
    wednesday = BooleanField('Wednesday')
    thursday = BooleanField('Thrusday')
    friday = BooleanField('Friday')
    saturday = BooleanField('Saturday')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    business = StringField('Busines Name', validators=[DataRequired()])
    #user = RadioField('Choice?', validators=[DataRequired()], choices=[('employee','Employee'), ('employer', 'Employer')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign Up')