from datetime import datetime
from fulcrumportal import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(120), unique=True, nullable=False)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(60), nullable=False)

    # User fields
    fullname = db.Column(db.String(40), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    business_name = db.Column(db.String(80), nullable=False)
    requests = db.relationship('Requests', backref='business', lazy=True)
    active = db.Column(db.Boolean(), default=True)

    roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}', '{self.image_file}')"


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_fullname = db.Column(db.String(40), nullable=False)
    user_business = db.Column(db.String(80), db.ForeignKey('user.business_name'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    request_title = db.Column(db.String(30), nullable=False, default='Request')
    request_body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Request('{self.user_fullname}', '{self.user_business}'," \
            f"'{self.request_title}', '{self.request_body}', '{self.date_posted}')"
