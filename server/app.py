#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurants = [restaurant.to_dict(rules = ("-restaurant_pizzas",)) for restaurant in Restaurant.query.all()]

    response = make_response(
        jsonify(restaurants),
        200
    )
    return response

@app.route("/restaurants/<int:id>", methods = ["GET", "DELETE"])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if not restaurant:
        response_dict = {
            "error": "Restaurant not found"
        }
        response = make_response(
            jsonify(response_dict),
            404
        )
        return response
    
    if request.method == "GET":
        rest_dict = restaurant.to_dict(rules = ("pizzas", "-restaurant_pizzas", "-pizzas.restaurant_pizzas"))
        
        response = make_response(
            jsonify(rest_dict),
            200
        )
    elif request.method == "DELETE":
        db.session.delete(restaurant)
        db.session.commit()

        return make_response("", 200)

    return response

@app.route("/restaurant_pizzas", methods = ["POST"])
def restaurant_pizzas():
    if request.method == "POST":
        print(request.values["price"])
        
        if int(request.values["price"]) < 1 or int(request.values["price"]) > 30:
            error_msg = {
                "error": "Invalid input"
            }

            response = make_response(jsonify(error_msg), 400)
            return response

        new_restaurant_pizza = RestaurantPizza(
            price = request.values["price"],
            pizza_id = request.values["pizza_id"],
            restaurant_id = request.values["restaurant_id"],
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        new_pizza_dict = new_restaurant_pizza.to_dict()

        response = make_response(
            jsonify(new_pizza_dict),
            201
        )

        return response
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)
