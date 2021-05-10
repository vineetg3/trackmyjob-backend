from database import db
from security import bcrypt
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email=db.Column(db.String,unique=True)
    password = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, nullable=False)
    jobs = db.relationship('UserJobsModel',backref='UserModel',lazy='dynamic')

    def __init__(self, username,email, password,created_at):
        self.username = username
        self.email=email
        self.password = password
        self.created_at=created_at

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)
    
    def hash_password(self):
        """Check password."""
        self.password = bcrypt.generate_password_hash(self.password).decode('UTF-8')

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
