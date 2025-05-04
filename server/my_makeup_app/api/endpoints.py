# import json
# from pathlib import Path
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import bcrypt  # ניתן להסיר אם אינך רוצה הצפנה

# DB_FILE = Path("data/database.json")

# auth_router = APIRouter()

# class UserCreate(BaseModel):
#     username: str
#     password: str

# class Database:
#     def __init__(self):
#         self.users = self.load_users()

#     def load_users(self):
#         """ Load users from the JSON file """
#         if not DB_FILE.exists():
#             return []
#         with open(DB_FILE, "r", encoding="utf-8") as file:
#             return json.load(file)

#     def save_users(self):
#         """ Save users to the JSON file """
#         with open(DB_FILE, "w", encoding="utf-8") as file:
#             json.dump(self.users, file, indent=4)

#     def add_user(self, user):
#         """ Add user and save to JSON """
#         self.users.append(user)
#         self.save_users()

#     def find_user_by_username(self, username):
#         """ Find user by username """
#         return next((user for user in self.users if user['username'] == username), None)

#     def verify_password(self, user, password):
#         """ Verify password (without bcrypt encryption for now) """
#         return user and user['password'] == password


# db = Database()


# @auth_router.post("/register")
# def register(user: UserCreate):
#     """ Register a new user """
#     # Check if the username already exists
#     existing_user = db.find_user_by_username(user.username)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
    
#     # Save the new user (no password encryption here)
#     db.add_user({"username": user.username, "password": user.password})
#     return {"message": "User created successfully", "username": user.username}


# @auth_router.post("/login")
# def login(user: UserCreate):
#     """ Log in the user """
#     # Find the user by username
#     existing_user = db.find_user_by_username(user.username)
#     if not existing_user or not db.verify_password(existing_user, user.password):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     return {"message": "Login successful", "username": user.username}
