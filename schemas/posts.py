from ma import ma
from models.posts import PostsModel


class PostsSchema(ma.ModelSchema):
    class Meta:
        model = PostsModel
        dump_only = ("id", "created_at",)
        load_only = ("user",)
        include_fk =True