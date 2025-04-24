from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

class Post(db.Model):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post") 

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "author_id": self.author_id,
            "post_id": self.post_id
        }

class Follower(db.Model):
    __tablename__ = "followers"
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id
        }

class Media(db.Model):
    __tablename__ = "medias"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=True)  
    post: Mapped["Post"] = relationship("Post", back_populates="media")  

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "post_id": self.post_id
        }