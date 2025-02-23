import os

# Define the directory structure and files
structure = {
    'data': ['__init__.py', 'models.py', 'database.py'],
    'business': ['__init__.py', 'services.py'],
    'presentation/api': ['__init__.py', 'endpoints.py'],
    'presentation/ui': ['__init__.py', 'views.py']
}

# Create the directories and files
for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        with open(os.path.join(folder, file), 'w') as f:
            pass

# Scaffold basic content for each file
data_models_content = """# data/models.py
class User:
    def __init__(self, user_id, name, skin_tone):
        self.user_id = user_id
        self.name = name
        self.skin_tone = skin_tone

class MakeupProduct:
    def __init__(self, product_id, name, shade):
        self.product_id = product_id
        self.name = name
        self.shade = shade
"""

data_database_content = """# data/database.py
class Database:
    def __init__(self):
        self.users = []
        self.makeup_products = []

    def add_user(self, user):
        self.users.append(user)

    def add_makeup_product(self, product):
        self.makeup_products.append(product)

    def find_makeup_for_skin_tone(self, skin_tone):
        return [product for product in self.makeup_products if product.shade == skin_tone]
"""

business_services_content = """# business/services.py
from data.database import Database

class MakeupService:
    def __init__(self, db):
        self.db = db

    def match_makeup(self, user):
        return self.db.find_makeup_for_skin_tone(user.skin_tone)
"""

presentation_api_endpoints_content = """# presentation/api/endpoints.py
from flask import Flask, request, jsonify
from data.models import User, MakeupProduct
from data.database import Database
from business.services import MakeupService

app = Flask(__name__)
db = Database()
service = MakeupService(db)

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

@app.route('/my_makeup_app', methods=['GET'])
def my_makeup_app():
    return "Welcome to My Makeup App!"

if __name__ == '__main__':
    app.run(debug=True)
"""

presentation_ui_views_content = """# presentation/ui/views.py
# This file can be used to define the user interface views if needed.
"""

# Write content to the files
files_content = {
    'data/models.py': data_models_content,
    'data/database.py': data_database_content,
    'business/services.py': business_services_content,
    'presentation/api/endpoints.py': presentation_api_endpoints_content,
    'presentation/ui/views.py': presentation_ui_views_content,
    'app.py': "# This file can be used to define the Flask app if needed."
}

for file_path, content in files_content.items():
    with open(file_path, 'w') as f:
        f.write(content)

print("Directories and files created successfully.")