# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# # מודל נתונים לבקשות POST
# class Item(BaseModel):
#     name: str
#     price: float

# # בקשת GET - מחזירה הודעה
# @app.get("/")
# def read_root():
#     return {"message": "השרת עובד! ברוכה הבאה ל-FIT_ME 🎉"}

# # בקשת GET עם פרמטר דינמי
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id, "message": "קיבלת פריט"}

# # בקשת POST - מקבלת נתונים ומחזירה אותם
# @app.post("/items/")
# def create_item(item: Item):
#     return {"message": "פריט נוצר בהצלחה!", "item": item}



from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
