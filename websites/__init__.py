from ast import ImportFrom
from flask import Flask, jsonify
from pymongo import MongoClient

mongo_uri = "mongodb+srv://ylee21:0000@cluster0.bnf6h1k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client.BU_MarketPlace_DB

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret_key"
    app.config['MONGO_URI'] = mongo_uri

    # register the blueprint
    from .views import views 
    from .auth import auth  
    from .user import user 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')

    return app 
