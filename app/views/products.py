from flask import  request, jsonify
from sqlalchemy import  and_, or_
from flask_login import  login_required, current_user
from app import app, db
from db.models import Product
import json




@app.route('/products', methods=['GET', "POST"])
@login_required
def products():
    user_id = current_user.id
    if request.method == 'POST':
        asin_list = None
        name_list = None        
        if request.data:
            info = json.loads(request.data)
            asin_list = info.get('asin')
            name_list = info.get('name')   
        if asin_list and name_list is None:
            product_objects = db.session.query(Product).filter(and_(Product.user_id == user_id, Product.asin.in_(asin_list)))        
            product_list = [i.to_dict() for i in product_objects] if product_objects else []
            return jsonify({'product_list': product_list}), 200, {'ContentType': 'application/json'}
        if name_list and asin_list is None:
            product_objects = db.session.query(Product).filter(and_(Product.user_id == user_id, Product.name.in_(name_list)))        
            product_list = [i.to_dict() for i in product_objects] if product_objects else []
            return jsonify({'product_list': product_list}), 200, {'ContentType': 'application/json'}
        if name_list and asin_list:
            product_objects = db.session.query(Product).filter(and_(Product.user_id == user_id, 
                                                                    or_(Product.name.in_(name_list), Product.asin.in_(asin_list))))        
            product_list = [i.to_dict() for i in product_objects] if product_objects else []
            return jsonify({'product_list': product_list}), 200, {'ContentType': 'application/json'}
        product_objects = db.session.query(Product).filter(Product.user_id == user_id)        
        product_list = [i.to_dict() for i in product_objects] if product_objects else []
        return jsonify({'product_list': product_list}), 200, {'ContentType': 'application/json'}
    else:
        product_objects = db.session.query(Product).filter(Product.user_id == user_id)        
        product_list = [i.to_dict() for i in product_objects] if product_objects else []
        return jsonify({'product_list': product_list}), 200, {'ContentType': 'application/json'}

@app.route('/products/add', methods=['POST'])
@login_required
def add_products():    
    info = json.loads(request.data)
    list_products = info.get('products')
    if list_products :
        if len(list_products) <= 0:
            return  jsonify({'error': 'Bad Request'}), 400, {'ContentType': 'application/json'}
        asin_list = [i.get('asin') for i in list_products if i.get('asin')]
        check_asin = db.session.query(Product).filter(and_(Product.user_id == current_user.id, Product.asin.in_(asin_list)))
        incorrect_products = [i.to_dict() for i in check_asin] 
        if len(incorrect_products) > 0:
            response_json = {'error': 'Bad Request', 'incorrect_products': incorrect_products}             
            return  jsonify(response_json), 400, {'ContentType': 'application/json'}
        for i in list_products:
            product=Product(user_id = current_user.id, asin = i.get('asin'), name = i.get('name'),
                            image = i.get('image'), currency = json.dumps(i.get('currency')))
            db.session.add(product)
            db.session.commit()
        return jsonify({'text': 'Ok'}), 200, {'ContentType': 'application/json'}
    return jsonify({'error': 'Bad Request'}), 400, {'ContentType': 'application/json'}
    

@app.route('/product/<int:id>/update', methods=['POST'])
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