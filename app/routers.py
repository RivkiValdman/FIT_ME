from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# יצירת רוטר
router = APIRouter()

# נתונים זמניים (לדוגמה)
fake_database = []

# מודל לקבלת נתונים דרך POST
class Item(BaseModel):
    name: str
    description: str
    price: float

# בקשת GET - מחזירה את כל הנתונים
@router.get("/items")
def get_items():
    return {"items": fake_database}

# בקשת POST - מוסיפה נתון לרשימה
@router.post("/items")
def create_item(item: Item):
    fake_database.append(item)
    return {"message": "Item added successfully!", "item": item}
