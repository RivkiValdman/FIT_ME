# import json
# from pathlib import Path
# from passlib.context import CryptContext

# DB_FILE = Path("data/database.json")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def load_users():
#     """ טוען את הנתונים מהקובץ JSON """
#     if not DB_FILE.exists():
#         return []
#     with open(DB_FILE, "r", encoding="utf-8") as file:
#         return json.load(file)

# def save_users(users):
#     """ שומר את הנתונים בקובץ JSON """
#     with open(DB_FILE, "w", encoding="utf-8") as file:
#         json.dump(users, file, indent=4)

# def hash_password(password: str):
#     return pwd_context.hash(password)

# def create_user(email: str, password: str):
#     users = load_users()
#     if any(user["email"] == email for user in users):
#         return None  # המשתמש כבר קיים
#     hashed_password = hash_password(password)
#     new_user = {"email": email, "password_hash": hashed_password}
#     users.append(new_user)
#     save_users(users)
#     return new_user

# def authenticate_user(email: str, password: str):
#     users = load_users()
#     user = next((u for u in users if u["email"] == email), None)
#     if user is None or not pwd_context.verify(password, user["password_hash"]):
#         return None
#     return user
