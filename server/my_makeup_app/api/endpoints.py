import sys
import os
from flask import Flask, request, jsonify

# Adjust the sys.path to include the root directory of the project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from data.database import Database
from data.models import User, MakeupProduct
from business.services import MakeupService

app = Flask(__name__)
db = Database()
service = MakeupService(db)
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
	return jsonify({'message': 'Hello World!'})

@app.route('/add_user', methods=['POST'])
def add_user():
	data = request.json
	user = User(data['user_id'], data['name'], data['skin_tone'])
	db.add_user(user)
	return jsonify({'message': 'User added successfully'})



@app.route('/add_makeup_product', methods=['POST'])
def add_makeup_product():
	data = request.json
	product = MakeupProduct(data['product_id'], data['name'], data['shade'])
	db.add_makeup_product(product)
	return jsonify({'message': 'Makeup product added successfully'})

@app.route('/match_makeup', methods=['POST'])
def match_makeup():
	data = request.json
	user = User(data['user_id'], data['name'], data['skin_tone'])
	matched_products = service.match_makeup(user)
	return jsonify({'matched_products': [product.__dict__ for product in matched_products]})

if __name__ == '__main__':
	app.run(debug=True)

