from flask import  request, jsonify
from sqlalchemy import  and_, or_
from flask_login import  login_required, current_user
from app import app, db
from db.models import Product




@app.route('/products', methods=['GET'])
@login_required
def products():
    asin_list = None
    name_list = None
    user_id = current_user.id
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