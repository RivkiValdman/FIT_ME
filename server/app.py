from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import cv2
import numpy as np
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route("/Sign_Up", methods=["POST"])
def Sign_Up():
    data = request.json
    username = data.get("username")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    gmail = data.get("gmail")
    password = data.get("password")

    if not username or not firstname or not lastname or not password or not gmail:
        return jsonify({"error": "Missing details"}), 400

    users = load_users()

    for user in users:
        if user["gmail"] == gmail:
            return jsonify({"error": "User gmail exists"}), 400

    users.append({
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "password": password,
        "gmail": gmail
    })
    save_users(users)

    return jsonify({"message": "Registration successful!"}), 201

@app.route("/Login", methods=["POST"])
def Login():
    data = request.json
    firstname = data.get("firstname")
    password = data.get("password")

    if not firstname or not password:
        return jsonify({"error": "Missing details"}), 400

    users = load_users()

    for user in users:
        if user["firstname"] == firstname and user["password"] == password:
            return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/upload_image", methods=["POST"])
def upload_image():
    data = request.json
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image data received"}), 400

    try:
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Failed to decode the image."}), 500

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return jsonify({"error": "לא זוהו פנים בתמונה. אנא נסי שוב עם תמונה אחרת"}), 400

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imwrite("captured_image.jpg", img)

        return jsonify({"message": "התמונה נשמרה בהצלחה ועברה לעיבוד אנא המתיני..."}), 200

    except Exception as e:
        return jsonify({"error": "Failed to save image", "details": str(e)}), 500

@app.route("/VideoStudent", methods=["POST"])
def VideoStudent():
    return '', 200

@app.route("/VideoTeacher", methods=["POST"])
def VideoTeacher():
    return '', 200

@app.route("/feedback", methods=["GET"])
def feedback():
    return '', 200

@app.route("/SlowVideo", methods=["POST"])
def SlowVideo():
    return '', 200

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)


