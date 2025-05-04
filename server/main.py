# from fastapi import FastAPI
# from pydantic import BaseModel
# import json
# from typing import List

# app = FastAPI()

# class User(BaseModel):
#     name: str
#     email: str
#     password: str

# # נתיב לשמירת נתונים
# @app.post("/register")
# async def register_user(user: User):
#     # קריאת קובץ JSON
#     try:
#         with open('data/database.json', 'r') as f:
#             data = json.load(f)
#     except FileNotFoundError:
#         data = []  # אם הקובץ לא קיים, ניצור רשימה חדשה

#     # הוספת הנתונים החדשים
#     data.append(user.dict())

#     # שמירת הנתונים בקובץ JSON
#     with open('data/database.json', 'w') as f:
#         json.dump(data, f, indent=4)

#     return {"message": "User successfully registered", "user": user}

