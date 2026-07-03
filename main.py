import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from supabase import create_client, Client

# ✅ Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials are missing. Check environment variables.")

# ✅ Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory=".")

# Example in‑memory store
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

# ✅ Test Supabase connection
@app.get("/test-supabase")
def test_supabase():
    try:
        data = supabase.table("your_table_name").select("*").limit(1).execute()
        return JSONResponse(content={"success": True, "data": data.data})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)})
