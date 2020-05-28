from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from libs.string import gettext
from models.posts import PostsModel
from schemas.posts import PostsSchema

post_schema = PostsSchema()
posts_schemas = PostsSchema(many=True)


class Posts(Resource):

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
        return post_schema.dump(post_data)


class MyPosts(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        posts = PostsModel.find_by_user_id(user_id)
        if not posts:
            return {"Message": "You have not made any post yet."}
        return posts_schemas.dump(posts), 201