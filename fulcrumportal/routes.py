import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from fulcrumportal.forms import WeekDayAvail, RegistrationForm, LoginForm, UpdateAccountForm, RequestForm
from fulcrumportal.models import User, Requests
from fulcrumportal import app, db, bcrypt
from flask_login import login_user, current_user, login_required, logout_user


@app.route("/")
@app.route("/home")
@login_required
def home():
    requests = Requests.query.all()
    return render_template('home.html', Title='Home', requests=requests)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash(f'Something went wrong, please check email or password', 'danger')
    return render_template('login.html', Title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullName.data, email=form.email.data.lower(), password=hashed_pw,
                    business_name=form.business.data, role='admin')
        db.session.add(user)
        db.session.commit()
        flash(f'name: {form.fullName.data}, your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', Title='Register', form=form)


@app.route("/avail", methods=["GET", "POST"])
def avail():
    form = WeekDayAvail()
    if form.validate_on_submit():
        flash(f'Thank you, {form.name.data} for submitting your availability!', 'success')
        return redirect(url_for('home'))
    return render_template('avail.html', Title='Availablility', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profilePics', picture_filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.fullname = form.fullName.data
        current_user.email = form.email.data
        current_user.business_name = form.business.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.fullName.data = current_user.fullname
        form.email.data = current_user.email
        form.business.data = current_user.business_name
    image_file = url_for('static', filename='profilePics/' + current_user.image_file)
    return render_template('account.html', Title='Account', image_file=image_file, form=form)


@app.route("/request/new", methods=["GET", "POST"])
@login_required
def new_request():
    form = RequestForm()
    if form.validate_on_submit():
        flash(f'You request has been sent!', 'success')
        request1 = Requests(user_fullname=current_user.fullname, business=current_user, request_title=form.title.data,
                            request_body=form.content.data)
        db.session.add(request1)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_request.html', Title='New Request',
                           form=form, legend='New Request')


@app.route("/request/<int:request_id>")
def requests(request_id):
    request2 = Requests.query.get_or_404(request_id)
    return render_template('request.html', title=request2.request_title, request=request2)


@app.route("/request/<int:request_id>/update", methods=["GET", "POST"])
@login_required
def update_request(request_id):
    request3 = Requests.query.get_or_404(request_id)
    if request3.business != current_user:
        abort(403)
    form = RequestForm()
    if form.validate_on_submit():
        request3.request_title = form.title.data
        request3.request_body = form.content.data
        db.session.commit()
        flash(f'Your post has been updated', 'success')
        return redirect(url_for('requests', request_id=request3.id))
    elif request.method == 'GET':
        form.title.data = request3.request_title
        form.content.data = request3.request_body
    return render_template('create_request.html', Title='Update Request',
                           form=form, legend='Update Request')


@app.route("/request/<int:request_id>/delete", methods=["POST"])
@login_required
def delete_request(request_id):
    request4 = Requests.query.get_or_404(request_id)
    if request4.business != current_user:
        abort(403)
    db.session.delete(request4)
    db.session.commit()
    flash(f'The request has been deleted!', 'success')
    return redirect(url_for('home'))
