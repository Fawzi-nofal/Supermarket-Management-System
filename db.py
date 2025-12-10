from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os, sys, re

# טען .env מהתיקייה של db.py (לא משנה מאיפה מריצים)
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

MONGODB_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "Market")

def _mask(uri: str) -> str:
    # הסתרת הסיסמה בהדפסה
    return re.sub(r'(?<=://).*?:.*?@', '***:***@', uri) if uri else uri

if not MONGODB_URI:
    print("❌ MONGODB_URI לא מוגדר בקובץ .env (צריך להיות ליד db.py)", file=sys.stderr)
    sys.exit(1)

print("🔗 Using URI:", _mask(MONGODB_URI))
print("🗄️  DB_NAME :", DB_NAME)

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000,
    socketTimeoutMS=5000,
)

try:
    client.admin.command("ping")
    print("✅ MongoDB connected")
except Exception as e:
    print(f"❌ לא ניתן להתחבר ל-MongoDB: {e}", file=sys.stderr)
    sys.exit(1)

db = client[DB_NAME]

def customers_coll(): 
    return db["customers"]
def products_coll():  
    return db["products"]
def orders_coll():    
    return db["orders"]
