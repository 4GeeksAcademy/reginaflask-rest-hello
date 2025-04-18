from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts = relationship("Post", back_populates="user")
    media = relationship("Media", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user_id": self.user_id
        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "post_id": self.post_id
        }

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    follower = relationship("User", foreign_keys=[follower_id], backref="followed_by")
    following = relationship("User", foreign_keys=[following_id], backref="follows")

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    media_type: Mapped[str] = mapped_column(String(50), nullable=False)  
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=True)  
    user = relationship("User", back_populates="media")
    post = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "media_type": self.media_type,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
