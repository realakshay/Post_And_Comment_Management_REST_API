from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from libs.string import gettext
from models.posts import PostsModel
from schemas.posts import PostsSchema

post_schema = PostsSchema()
posts_schemas = PostsSchema(many=True)


class PostsTitle(Resource):

    @classmethod
    def get(cls, title: str):
        posts_data = PostsModel.find_by_tile(title)
        if not posts_data:
            return {"Message": gettext("post_not_found").format(title)}, 401
        return posts_schemas.dump(posts_data), 201


class MakePosts(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        post_json = request.get_json()
        try:
            post_data = post_schema.load(post_json, partial=("user_id",))
        except ValidationError as err:
            return {"Message": err.messages}, 401
        user_id = get_jwt_identity()
        post_data.user_id = user_id
        post_data.insert_post()
        return {"Message": gettext("post_created_successful")}


class MyPosts(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        posts = PostsModel.find_by_user_id(user_id)
        if not posts:
            return {"Message": gettext("post_not_created_yet")}, 401
        return posts_schemas.dump(posts), 201


class PostDescription(Resource):

    @classmethod
    def get(cls, desc: str):
        posts = PostsModel.find_by_desc(desc)
        if not posts:
            return {"Message": gettext("post_desc_not_found").format(desc)}, 401
        return posts_schemas.dump(posts), 201


class ChangeOrDeletePost(Resource):

    @classmethod
    @jwt_required
    def delete(cls, post_id: int):
        user_id = get_jwt_identity()
        posts = PostsModel.find_by_id(post_id)
        if posts:
            if posts.user_id == user_id:
                posts.delete_post()
                return {"Message": gettext("post_deleted_successful")}, 201
            return {"Message": gettext("post_cannot_deleted")}, 401
        return {"Message": gettext("post_id_not_found").format(post_id)}, 401

    @classmethod
    @jwt_required
    def put(cls, post_id: int):
        user_id = get_jwt_identity()
        post_json = request.get_json()
        try:
            post_data = post_schema.load(post_json, partial=("user_id","title",))
        except ValidationError as err:
            return {"Message": err.messages}, 401

        posts = PostsModel.find_by_id(post_id)
        if posts:
            if posts.user_id == user_id:
                posts.description = post_data.description
                posts.insert_post()
                return {"Message": "post updated successfully"}, 201
            return {"Message": gettext("post_cannot_deleted")}, 401
        return {"Message": gettext("post_id_not_found").format(post_id)}


class AllPost(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        return posts_schemas.dump(PostsModel.find_all())