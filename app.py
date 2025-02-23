


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# הגדרת CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # מאפשר לכל הדומיינים לשלוח בקשות
    allow_credentials=True,
    allow_methods=["*"],  # מאפשר את כל סוגי הבקשות (GET, POST, וכו')
    allow_headers=["*"],  # מאפשר את כל הכותרות
)

# הנתונים הדוגמתיים
items = [
    {"name": "Product 1", "price": 25},
    {"name": "Product 2", "price": 30},
]

class Item(BaseModel):
    name: str
    price: float

@app.get("/items")
def get_items():
    return items

@app.post("/items")
def add_item(item: Item):
    items.append(item.dict())
    return item
