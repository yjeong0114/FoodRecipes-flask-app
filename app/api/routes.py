from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Food, food_schema, foods_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yeeeeeee': 'nawwwwwwww'}

@api.route('/foodlist', methods = ['POST'])
@token_required
def create_food(current_user_token):
    meals = request.json['meals']
    foodname = request.json['foodname']
    calories = request.json['calories']
    day = request.json['day']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    food = Food(meals, foodname, calories, day, user_token = user_token )

    db.session.add(food)
    db.session.commit()

    response = food_schema.dump(food)
    return jsonify(response)

@api.route('/foodlist', methods = ['GET'])
@token_required
def get_food(current_user_token):
    a_user = current_user_token.token
    foods = Food.query.filter_by(user_token = a_user).all()
    response = foods_schema.dump(foods)
    return jsonify(response)

@api.route('/foodlist/<id>', methods = ['GET'])
@token_required
def get_single_food(current_user_token, id):
    food = Food.query.get(id)
    response = food_schema.dump(food)
    return jsonify(response)

@api.route('/foodlist/<id>', methods = ['POST','PUT'])
@token_required
def update_food(current_user_token,id):
    contact = Food.query.get(id) 
    contact.meals = request.json['meals']
    contact.foodname = request.json['foodname']
    contact.calories = request.json['calories']
    contact.day = request.json['day']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = food_schema.dump(contact)
    return jsonify(response)

@api.route('/foodlist/<id>', methods = ['DELETE'])
@token_required
def delete_food(current_user_token, id):
    food = Food.query.get(id)
    db.session.delete(food)
    db.session.commit()
    response = food_schema.dump(food)
    return jsonify(response)