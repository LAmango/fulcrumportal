from flask import render_template, url_for, flash, redirect
from fulcrumportal.forms import WeekDayAvail, RegistrationForm, LoginForm
from fulcrumportal.models import User, Requests
from fulcrumportal import app, db, bcrypt
from flask_login import login_user, current_user

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', Title='Home')

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login = LoginForm()
    if login.validate_on_submit():
        user = User.query.filter_by(email=login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash(f'Something went wrong, please check email or password', 'danger')
    return render_template('login.html', Title='Login', form=login)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    register = RegistrationForm()
    if register.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
        user = User(fullname=register.fullName.data, email=register.email.data, password=hashed_pw, business_name=register.business.data, role='admin')
        db.session.add(user)
        db.session.commit()
        flash(f'name: {register.fullName.data}, your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', Title='Register', form=register)

@app.route("/avail", methods=["GET", "POST"])
def avail():
    form = WeekDayAvail()
    if form.validate_on_submit():
        flash(f'Thank you, {form.name.data} for submitting your availability!', 'success')
        return redirect(url_for('home'))
    return render_template('avail.html', Title='Availablility', form=form)