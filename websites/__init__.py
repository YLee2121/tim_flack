from flask import Flask
from pymongo import MongoClient

# global parameter
UPLOAD_FOLDER = './websites/static/product_pic/'

MONGO_URI = "mongodb+srv://ylee21:0000@cluster0.bnf6h1k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.BU_MarketPlace_DB



def create_app():

    # app configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret_key"
    app.config['MONGO_URI'] = MONGO_URI
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # register the blueprint
    from .views import views 
    from .auth import auth  
    from .user import user 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')


    return app 
