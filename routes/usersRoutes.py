from flask import Blueprint,request,jsonify
from database.db import db

from models.users import Users

from security import secur

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

user_route=Blueprint('auth',__name__,url_prefix='/api/auth')

# Get users
@user_route.route("/users",methods=['GET'])
def get_Users():
    myUsers = Users.query.all()
    user_list = [user.to_json() for user in myUsers]
    return {'result': user_list},200

@user_route.route('/register',methods=['POST'])
def create_user():
        data = request.json

        name = data['name']
        email = data['email']
        password = data['password']
        new_user = Users(name=name ,password=secur.get_password_hash(password),email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"msg":"User created"},201
        except Exception as e:
            # print(f'error : = {e}')
            return {e}



@user_route.route('/login',methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = Users.query.filter_by(email=email).first()
    # print(user)
    if not user:
        return jsonify({'message': 'Invalid email'}), 401
    try:
        user_hashed_pass = user.to_json()["password"]

        user_password = secur.verify_password(password,user_hashed_pass)

        if not user_password:
            return jsonify({'message': 'Wrong password'}), 401

        access_token = create_access_token(identity=password)
        return jsonify(access_token=access_token)
    except Exception as e:
        # Log the exception for debugging (optional)
        # print(f"An error occurred during login: {e}")
        return jsonify({'message': 'An error occurred during login'}), 500


def current_token(user_list):
     current_user= get_jwt_identity()

     for user in user_list:
          userjson = user.to_json()
          user_password = secur.verify_password(current_user,userjson["password"])
          if user_password:
              return {"email":userjson['email'],"name":userjson['name'],"is_user":True}
          else:
              return {"email":'not exist',"name":'not exist',"is_user":False}

@user_route.route('/check-user',methods=['GET'])
@jwt_required()
def check_user():
    try:
        myusers = Users.query.all()
        user_Info = current_token(myusers)

        return jsonify(current_user=user_Info)
    except Exception as e:
        print(f"error in check user token {e}")
        return jsonify(current_user=e)
         