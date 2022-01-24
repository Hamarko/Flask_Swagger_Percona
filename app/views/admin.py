from flask import  request, jsonify, redirect, url_for
from flask_login import  login_required, current_user, login_user
from app import app, db
from db.models import User
import json

@app.route('/signup', methods=['post'])
def signup():    
    print (request.data)
    info = json.loads(request.data)
    email = info.get('email')
    password = info.get('password') 
    name = info.get('name')
    image = info.get('image')
    if email is None or password is None:
        return jsonify({'error': 'Bad Request'}), 400, {'ContentType': 'application/json'}
    user = db.session.query(User).filter(User.email == email).first()
    if user:
        return jsonify({'error': 'Bad Request'}), 400, {'ContentType': 'application/json'}
    user = User(name=name, email=email, image=image)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'text': 'Ok'}), 200, {'ContentType': 'application/json'}

@app.route('/user/update', methods=['PATCH'])
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