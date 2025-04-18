from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    posts = relationship('Post', backref='author')
    comments = relationship('Comment', backref='author')
    followers = relationship('Follower', backref='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250))
    caption = db.Column(db.String(500))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    comments = relationship('Comment', backref='post')

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "user_id": self.user_id
        }

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    post_id = db.Column(db.Integer, ForeignKey('post.id'))

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id,
            "post_id": self.post_id
        }

class Follower(db.Model):
    __tablename__ = 'follower'

    id = db.Column(db.Integer, primary_key=True)
    user_from_id = db.Column(db.Integer, ForeignKey('user.id'))
    user_to_id = db.Column(db.Integer, ForeignKey('user.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }
