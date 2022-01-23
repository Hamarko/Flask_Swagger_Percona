import json
from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  and_, or_
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, login_user, current_user
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


DB_USER = "root"
DB_PASS = "root"
DB_HOST = "localhost"
DB_PORT = "81"
DATABASE = "percona-server/main"
connect_string = 'mysql+pymysql://{}:{}@{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DATABASE)
old_mysql = 'mysql://root:root@db/main'
app.config['SQLALCHEMY_DATABASE_URI'] = old_mysql
app.config['SECRET_KEY'] = '13qwfwegerg'

# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
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




from db.models import User, Product

@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return db.session.query(User).filter(User.id == int(user_id)).first()


from views import  products   



@app.route('/', methods=['GET'])
@login_required
def index():
    return "Hi!"



@app.route('/signup', methods=['post'])
def signup():
    
    print (request.data)
    info = json.loads(request.data)
    email = info.get('email')
    password = info.get('password') 
    name = info.get('name')
    image = info.get('image')
    if email is None or password is None:
        return jsonify({'error': 'Email and password fields are required'}), 400, {'ContentType': 'application/json'}
    user = db.session.query(User).filter(User.email == email).first()
    if user:
        return jsonify({'error': 'This email already exists'}), 400, {'ContentType': 'application/json'}
    user = User(name=name, email=email, image=image)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'text': 'Ok'}), 200, {'ContentType': 'application/json'}

@app.route('/update/user', methods=['POST'])
@login_required
def update_user():
    info = json.loads(request.data)
    name = info.get('name')
    image = info.get('image')
    user =  db.session.query(User).get(current_user.id)
    if name: user.name = name
    if image: user.image = image
    db.session.commit()
    return jsonify({'text': 'Ok'}), 200, {'ContentType': 'application/json'}


@app.route('/add_products', methods=['POST'])
@login_required
def add_products():
    info = json.loads(request.data)
    list_products = info.get('products')
    if list_products : 
        asin_list = [i.get('asin') for i in list_products if i.get('asin')]
        check_asin = db.session.query(Product).filter(and_(Product.user_id == current_user.id, Product.asin.in_(asin_list)))
        incorrect_products = [i.to_dict() for i in check_asin] 
        if len(incorrect_products) > 0:
            response_json = {'error': 'asin this asins already exists', 'incorrect_products': incorrect_products}             
            return  jsonify(response_json), 400, {'ContentType': 'application/json'}
        for i in list_products:
            product=Product(user_id = current_user.id, asin = i.get('asin'), name = i.get('name'),
                            image = i.get('image'), currency = json.dumps(i.get('currency')))
            db.session.add(product)
            db.session.commit()
        return jsonify({'text': 'Ok'}), 200, {'ContentType': 'application/json'}
    return jsonify({'text': 'No products'}), 200, {'ContentType': 'application/json'}




@app.route('/update_product/<int:id>', methods=['POST'])
@login_required
def update_product(id):
    info = json.loads(request.data)
    name = info.get('name')
    image = info.get('image')
    currency = info.get('currency')
    product =  db.session.query(Product).get(id)
    if product:
        if name: product.name = name
        if image: product.image = image
        if currency: product.currency = json.dumps(currency)
        db.session.commit()
        return jsonify({'text': 'Ok'}), 200, {'ContentType': 'application/json'}
    return jsonify({'error': 'Not found'}), 404, {'ContentType': 'application/json'}

@app.route('/login', methods=['post'])
def login():
    info = json.loads(request.data)
    email = info.get('email')
    password = info.get('password') 
    user = db.session.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('products'))
    return jsonify({'error': 'Bad email or password'}), 404, {'ContentType': 'application/json'} 



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")