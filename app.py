import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from ma import ma
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.posts import PostsTitle, MakePosts, MyPosts, PostDescription, ChangeOrDeletePost, AllPost
from resources.comment import Comments
from blacklist import BLACKLIST

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'description': "Token has been revoked."})


api.add_resource(UserRegister, '/register')
api.add_resource(Confirmation, '/confirm/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/confirm_by/user/<int:user_id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(PostsTitle, '/posts/title/<string:title>')
api.add_resource(MakePosts, '/create_post')
api.add_resource(MyPosts, '/myposts')
api.add_resource(PostDescription, '/post_desc/<string:desc>')
api.add_resource(ChangeOrDeletePost, '/edit/<int:post_id>')
api.add_resource(AllPost, '/allposts')
api.add_resource(Comments, '/comment/<int:post_id>')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True, port=5555)
