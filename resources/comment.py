from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from models.comment import CommentModel
from schemas.comment import CommentSchema

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


class Comments(Resource):

    @classmethod
    @jwt_required
    def post(cls, post_id: int):
        comment_json = request.get_json()
        try:
            comment_data = comment_schema.load(comment_json, partial=("post_id",))
        except ValidationError as err:
            return {"Message": err.messages}, 401

        comment_data.post_id = post_id
        comment_data.insert_comment()
        return comment_schema.dump(comment_data), 201

    @classmethod
    @jwt_required
    def get(cls, post_id: int):
        comments_data = CommentModel.find_by_post_id(post_id)
        if comments_data:
            return comments_schema.dump(comments_data)
        return {"Message": "Not found"}