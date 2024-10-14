from flask import Flask
from flask_restful import  Api
from flask_migrate import Migrate
from db import db
#from decouple import config

from resources.auth import UserRegisterResource, UserLoginResource

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig') #to do env

with app.app_context():
    db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')


if __name__ == '__main__':
    app.run(debug=True)