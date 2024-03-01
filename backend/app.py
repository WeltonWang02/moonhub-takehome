from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS  # Import CORS
import sys
import os
from dotenv import load_dotenv
from database import InventoryDB


load_dotenv()  # take environment variables from .env.
port = os.getenv("PORT", 5100)
host = os.getenv("HOST", "0.0.0.0")
database = f"sqlite:///{os.getenv('DATABASE', 'db.sqlite')}"
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:80")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": [frontend_url, "http://localhost"]}})  # Enable CORS for the Flask app with specific origins
api = Api(app)

db = InventoryDB(database)

class Products(Resource):
    def get(self):
        search_query = request.args.get('s', '')
        limit = request.args.get('limit', 10)
        sort = request.args.get('sort', 'name')
        order = request.args.get('order', 'asc')
        products = db.get_products(filter=search_query, limit=limit, sort=sort, order=order)
        return {'products': [{'id': product['id'], 'name': product['name'], 'description': product['description'], 'inventory': product['inventory'], 'last_modified': product['last_modified']} for product in products]}, 200

    def post(self):
        product_data = request.get_json()
        name = product_data.get('name')
        description = product_data.get('description')
        inventory = product_data.get('inventory', 0)
        if not db.insert_product(name, description, inventory):
            return {'error': 'Failed to create product due to invalid input'}, 400
        return {'message': 'Product created successfully'}, 201
    

api.add_resource(Products, '/api/products')


if __name__ == '__main__':
    app.run(host=host, port=port) 
