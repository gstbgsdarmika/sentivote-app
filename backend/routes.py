from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from models import db, User, UserSchema

bcrypt = Bcrypt()
register = Blueprint('register', __name__)
login = Blueprint('login', __name__)

user_schema = UserSchema()

@register.route('/register', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    except IntegrityError:  
        db.session.rollback()
        return jsonify({'message': 'Username or email already exists'}), 400

@login.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
