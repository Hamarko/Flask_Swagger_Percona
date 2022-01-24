import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DATABASE = os.getenv('DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')
connect_string = 'mysql+pymysql://{}:{}@{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = connect_string
app.config['SECRET_KEY'] = SECRET_KEY

# flask swagger configs
SWAGGER_URL = os.getenv('SWAGGER_URL')
API_URL = os.getenv('API_URL')
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




from db.models import User

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return db.session.query(User).filter(User.id == int(user_id)).first()


from views import  products, admin

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")