from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import Form, BooleanField, StringField, SubmitField, PasswordField, RadioField, TextAreaField
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
#   user = RadioField('Choice?', validators=[DataRequired()], choices=[('employee','Employee'), ('employer', 'Employer')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    business = StringField('Busines Name', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data.lower()).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')


class RequestForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Request', validators=[DataRequired()])
    submit = SubmitField('Submit')
