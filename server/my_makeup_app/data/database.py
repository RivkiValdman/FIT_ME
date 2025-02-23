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