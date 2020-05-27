import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = os.environ.get('DATABASE_URL')

api = Api(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, port=5555)