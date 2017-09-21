from flask_bcrypt import generate_password_hash, check_password_hash

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from app import db, app


class User(db.Model):
    """
    Defines attributes for a user
    """
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.BINARY(60))
    date_created = db.Column(db.DATETIME, default=db.func.current_timestamp())

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.token = self.generate_auth_token()

    def verify_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        serializer = Serializer(
            app.config['SECRET_KEY'], expires_in=expiration)
        return serializer.dumps({'username': self.username})

    def save(self):
        db.session.add(self)
        db.session.commit()

    def refresh_from_db(self):
        return db.session.query(User).filter_by(id=str(self.id))
