
from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from werkzeug.security import generate_password_hash,  check_password_hash
import json

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date_created = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(DateTime(timezone=True), default=func.now(),  onupdate=func.now())
    email = db.Column(String(128), unique=True)
    name = db.Column(String(128), unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    image = db.Column(String(256))
    product = db.relationship("Product")

    def to_dict(self):
        d = {
            "id": self.id,
            "date_created": str(self.date_created),
            "updated_on": str(self.updated_on) if self.updated_on else None,
            "email": self.email,
            "image": self.image,
        }
        return d
     
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
	    return "<{} - {}:{}>".format(self.updated_on, self.id, self.name)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id =  db.Column(Integer, db.ForeignKey('user.id'))
    asin = db.Column(String(128))
    name = db.Column(String(128))
    image = db.Column(String(256))
    currency= db.Column( db.JSON, nullable=True )
    UniqueConstraint('user_id','asin')

    def to_dict(self):
        d = {
            "id": self.id,
            "user_id": self.user_id,
            "asin": self.asin,
            "image": self.image,
            "name": self.name,
            "currency": json.loads(self.currency)
        }
        return d

