import datetime
from typing import List

from db import db


class CommentModel(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(80), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    comment_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    posts = db.relationship("PostsModel")

    @classmethod
    def find_by_post_id(cls, post_id: int) -> List:
        return cls.query.filter_by(post_id=post_id).all()

    def insert_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()