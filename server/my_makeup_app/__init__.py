# my_makeup_app/__init__.py

if __name__ == "__main__":
	from api.endpoints import app
	app.run(debug=True)