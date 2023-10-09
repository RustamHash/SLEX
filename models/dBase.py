from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.username

    def add_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def get_user_name(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_user_id(user_id):
        return User.query.filter_by(user_id=user_id).first()
