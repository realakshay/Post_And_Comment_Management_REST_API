from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from models.comment import CommentModel
from schemas.comment import CommentSchema

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


class Comments(Resource):

    @classmethod
    @jwt_required
    def get(cls, post_id: int):
        comments_data = CommentModel.find_by_post_id(post_id)
        if comments_data:
            return comments_schema.dump(comments_data)
        return {"Message": "Not found"}

    @classmethod
    @jwt_required
    def post(cls, post_id: int):
        comment_json = request.get_json()
        try:
            comment_data = comment_schema.load(comment_json, partial=("post_id", "user_id",))
        except ValidationError as err:
            return {"Message": err.messages}, 401

        user_id = get_jwt_identity()
        comment_data.post_id = post_id
        comment_data.user_id = user_id
        comment_data.insert_comment()
        return comment_schema.dump(comment_data), 201


class EditComment(Resource):

    @classmethod
    @jwt_required
    def put(cls, comment_id: int):
        user_id = get_jwt_identity()
        comment = CommentModel.find_by_comment_id(comment_id)
        comment_json = request.get_json()
        try:
            comment_data = comment_schema.load(comment_json, partial=("user_id", "post_id"))
        except ValidationError as err:
            return err.messages, 401

        if comment:
            if comment.user_id == user_id:
                comment.comment = comment_data.comment
                comment.insert_comment()
                return {"Message": "Comment Updeted.."}
            return {"Message": "You can't delete others comment"}
        return {"Message": "Comment not exist here."}


    @classmethod
    @jwt_required
    def delete(cls, comment_id: int):
        user_id = get_jwt_identity()
        comment = CommentModel.find_by_comment_id(comment_id)
        if comment:
            if comment.user_id == user_id:
                comment.delete_comment()
                return {"Message": "Comment Deleted.."}
            return {"Message": "You can't delete others comment"}
        return {"Message": "Comment not exist here."}