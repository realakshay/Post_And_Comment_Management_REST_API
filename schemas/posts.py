from marshmallow import pre_dump

from ma import ma
from models.posts import PostsModel
from schemas.comment import CommentSchema


class PostsSchema(ma.ModelSchema):

    comments = ma.Nested(CommentSchema, many=True)

    class Meta:
        model = PostsModel
        dump_only = ("id", "created_at",)
        load_only = ("user",)
        include_fk =True

