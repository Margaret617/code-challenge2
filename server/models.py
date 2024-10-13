from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
        }

    # add relationship
    # back_populates is somehow the same as backref but it give you more  control
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

    # add serialization rules

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    # to_dict () to convert an object to a dictionary
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients,
        }

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    # add serialization rules

    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    # adding  a foreign key to the restaurant table
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    # adding  a foreign key to the pizza table
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    # add relationships
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    
    # add serialization rules

    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30.")
        return price

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
