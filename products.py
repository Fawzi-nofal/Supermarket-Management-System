from db import products_coll
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING
from pymongo import ReturnDocument


products = products_coll()
def ensure_products_indexes():
    products.create_index([("name", ASCENDING)], name="name_asc")
    products.create_index([("category", ASCENDING)], name="category_asc")

def create_product( product_id: str,name: str, category: str, price: float):
    doc = {
        "_id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    try:
        products.insert_one(doc)
        return product_id
    except DuplicateKeyError:
        raise ValueError(f"Product with id {product_id} already exists")
    
def update_product(product_id: str, name: str = None, category: str = None, price: float = None):
    
    update_fields = {}
    if name is not None:
        update_fields["name"] = name
    if category is not None:
        update_fields["category"] = category
    if price is not None:
        update_fields["price"] = price

    if not update_fields:
        return get_product_by_id(product_id)  # אם לא נשלחו שדות לעדכון, נחזיר את המוצר

    update_fields["updatedAt"] = datetime.utcnow()
    try:
        return products.find_one_and_update(
            {"_id": product_id},               # חיפוש לפי מזהה
            {"$set": update_fields},           # עדכון רק של השדות שנשלחו
            return_document=ReturnDocument.AFTER
            )
    except DuplicateKeyError:
        raise ValueError("Update violates uniqueness constraint (name, category)")
        
def delete_product(product_id: str) -> int:
   
    res = products.delete_one({"_id": product_id})
    return res.deleted_count


        
def get_product_by_id(product_id: str):
    
    return products.find_one({"_id": product_id})

def get_all_products():
    
    return list(products.find({}, {"_id": 1, "name": 1, "category": 1, "price": 1}))
