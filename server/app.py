#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


"""
jsonify is used to covert python data structures like dictionaries into a JSON (javascript Object Notation ) response
"""


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants]), 200
# to_dict() is used to covert an object to a python dictionary 


@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify({
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'restaurant_pizzas': [pizza.to_dict() for pizza in restaurant.restaurant_pizzas]
        })
    return jsonify({'error': 'Restaurant not found'}), 404

# int:id is the placeholder URL for an integer value .This is how flask makes sure you are providing valid data


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return make_response({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204
# 204 error means there is no content ,it is used to indicate that the request was successful but there was no content provided


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    } for pizza in pizzas]), 200


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    if 'price' not in data or not (1 <= data['price'] <= 30):
        return jsonify({'errors': ['Price must be between 1 and 30']}), 400

    pizza = Pizza.query.get(data['pizza_id'])
    restaurant = Restaurant.query.get(data['restaurant_id'])

    if not pizza or not restaurant:
        return jsonify({'errors': ['Pizza or Restaurant not found']}), 404

    restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=pizza.id, restaurant_id=restaurant.id)
    db.session.add(restaurant_pizza)  # used to add an object to the database
    db.session.commit()  # finalizes  the changes to the database

    return jsonify({
        'id': restaurant_pizza.id,
        'price': restaurant_pizza.price,
        'pizza_id': restaurant_pizza.pizza_id,
        'restaurant_id': restaurant_pizza.restaurant_id,
        'pizza': {'id': pizza.id, 'name': pizza.name},
        'restaurant': {'id': restaurant.id, 'name': restaurant.name}
    }), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
