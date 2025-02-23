from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# מודל נתונים למשתמש
class User(BaseModel):
    name: str
    email: str

# דימוי של מסד נתונים
fake_db_users = []

# פונקציה להוספת משתמש
@app.post("/users/")
def add_user(user: User):
    fake_db_users.append(user)
    return user

# פונקציה להחזיר את כל המשתמשים
@app.get("/users")
def get_users():
    return fake_db_users

# פונקציה להחזיר פריטים
@app.get("/items")
def get_items():
    # דוגמה של פריטים להחזיר
    items = [
        {"name": "item1", "price": 10},
        {"name": "item2", "price": 20}
    ]
    return items
