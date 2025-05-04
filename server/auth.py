# import json
# from pathlib import Path
# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel

# DB_FILE = Path("my_makeup_app/data/database.json")

# auth_router = APIRouter()

# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

# class Database:
#     def __init__(self):
#         self.users = self.load_users()

#     def load_users(self):
#         """ טוען את המשתמשים מהקובץ JSON """
#         if not DB_FILE.exists():
#             return []
#         with open(DB_FILE, "r", encoding="utf-8") as file:
#             return json.load(file)

#     def save_users(self):
#         """ שומר משתמשים לקובץ JSON """
#         with open(DB_FILE, "w", encoding="utf-8") as file:
#             json.dump(self.users, file, indent=4)

#     def add_user(self, user):
#         """ מוסיף משתמש ושומר """
#         self.users.append(user)
#         self.save_users()

#     def find_user_by_email(self, email):
#         return next((user for user in self.users if user["email"] == email), None)

# db = Database()

# @auth_router.post("/register")
# def register(user: UserCreate):
#     existing_user = db.find_user_by_email(user.email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already exists")

#     db.add_user({"username": user.username, "email": user.email, "password": user.password})
#     return {"message": "User created successfully"}

# @auth_router.post("/login")
# def login(user: UserCreate):
#     existing_user = db.find_user_by_email(user.email)
#     if not existing_user or existing_user["password"] != user.password:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     return {"message": "Login successful"}
