from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from libs.string import gettext
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
            return comments_schema.dump(comments_data), 201
        return {"Message": gettext("comment_post_not_found").format(post_id)}, 401

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
                return {"Message": gettext("comment_update_successful")}, 201
            return {"Message": gettext("comment_not_authorized_to_change_others_comment")}, 401
        return {"Message": gettext("comment_not_exist")}, 401


    @classmethod
    @jwt_required
    def delete(cls, comment_id: int):
        user_id = get_jwt_identity()
        comment = CommentModel.find_by_comment_id(comment_id)
        if comment:
            if comment.user_id == user_id:
                comment.delete_comment()
                return {"Message": gettext("comment_delete_successful")}, 201
            return {"Message": gettext("comment_not_authorized_to_change_others_comment")}, 401
        return {"Message": gettext("comment_not_exist")}, 401


class TruncateCommentTable(Resource):

    @classmethod
    def get(cls):
        n = CommentModel.delete_all()
        print(n)
        return {"Message": gettext("comments_deleted_successful")}, 201