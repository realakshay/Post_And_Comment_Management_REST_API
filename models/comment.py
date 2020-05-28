import datetime
from typing import List

from db import db


class CommentModel(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(80), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    comment_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    posts = db.relationship("PostsModel")
    user = db.relationship("UserModel")

    @classmethod
    def find_by_comment_id(cls, comment_id: int) -> "CommentModel":
        return cls.query.filter_by(id=comment_id).first()

    @classmethod
    def find_by_post_id(cls, post_id: int) -> List:
        return cls.query.filter_by(post_id=post_id).all()

    @classmethod
    def find_by_post_and_user_id(cls, post_id: int, user_id: int) -> List:
        return cls.query.filter_by(post_id=post_id, user_id=user_id).all()

    def insert_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        n = cls.query.delete()
        db.session.commit()
        return n