import datetime
from typing import List

from db import db


class PostsModel(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel")

    @classmethod
    def find_by_id(cls, post_id: int) -> "PostsModel":
        return cls.query.filter_by(id=post_id).first()

    @classmethod
    def find_by_tile(cls, title: str) -> List:
        return cls.query.filter_by(title=title).all()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> List:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_desc(cls, desc: str) -> List:
        return cls.query.filter(cls.description.like(f"%{desc}%")).all()

    def insert_post(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_post(self) -> None:
        db.session.delete(self)
        db.session.commit()