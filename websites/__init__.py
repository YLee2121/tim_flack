from flask import Flask
from pymongo import MongoClient
from flask_mail import Mail




# global parameter
SRC_TO_PIC_PATH = 'static/product_pic/'
APP_TO_PIC_PATH = './websites/static/product_pic/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MONGO_URI = "mongodb+srv://ylee21:0000@cluster0.bnf6h1k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.BU_MarketPlace_DB



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():

    # app configuration
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "secret_key"
    app.config['MONGO_URI'] = MONGO_URI

    # for mail
    # app.config['MAIL_SERVER']='smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = 'bumarketplace488@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'grihtpchplddgqkv'
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True

    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '2ee351b9b8c730'
    app.config['MAIL_PASSWORD'] = 'b3ccbb47fdb95d'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    global mail_server
    mail_server = Mail(app)

    # register the blueprint
    from .views import views 
    from .auth import auth  
    from .user import user 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')


    return app 
