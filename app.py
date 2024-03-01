from flask import Flask, request
from flask_restful import Resource, Api
import sys
import os
from dotenv import load_dotenv
from backend.database import inventoryDB


load_dotenv()  # take environment variables from .env.
port = os.getenv("PORT", 5100)
host = os.getenv("HOST", "0.0.0.0")
database = f"sqlite:///{os.getenv('DATABASE', 'db.sqlite')}"

app = Flask(__name__)
api = Api(app)

db = inventoryDB(database)

class Products(Resource):
    def get(self):
        search_query = request.args.get('s', '')
        limit = request.args.get('limit', 10)
        products = db.get_products(filter=search_query, limit=limit)
        return {'products': [product.name for product in products]}, 200
        # This is where you would add logic to fetch and return products

    def post(self):
        product_data = request.get_json()
        name = product_data.get('name')
        description = product_data.get('description')
        inventory = product_data.get('inventory', 0)
        db.insert_product(name, description, inventory)
        return {'message': 'Product created successfully'}, 201
    

api.add_resource(Products, '/api/products')


if __name__ == '__main__':
    app.run(host=host, port=port) 
