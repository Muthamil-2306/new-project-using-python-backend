from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=BASE_DIR)  # look in root

store = {}

@app.get("/")
def get_store():
    return {"store": store}

@app.post("/inserting")
def insert(key: str, value: str):
    store[key] = value
    return {"store": store}

@app.put("/updating")
def update(key: str, value: str):
    if key in store:
        store[key] = value
        return {"store": store}
    return {"error": "Key not found"}

@app.delete("/deleting")
def delete(key: str):
    if key in store:
        store.pop(key)
        return {"store": store}
    return {"error": "Key not found"}

@app.get("/ui")
def ui(request: Request):
    return templates.TemplateResponse("ui.html", {"request": request})
