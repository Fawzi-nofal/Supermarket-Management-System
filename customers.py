
from db import customers_coll
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING
from pymongo import ReturnDocument

customers = customers_coll()

def ensure_customers_indexes():
    
    customers.create_index([("name", ASCENDING)], name="name_asc")
    
    customers.create_index([("phone", ASCENDING)], name="phone_asc")

def create_customer( customer_id: str,name: str, phone: str, email: str):
    
    doc = {"_id": customer_id,"name": name, "phone": phone, "email": email}
    try:
        res = customers.insert_one(doc)
        return res.inserted_id  
    except DuplicateKeyError:
        raise ValueError(f"ID already exists: { customer_id}")
    
def update_customer(customer_id: str, name: str = None, phone: str = None, email: str = None):
 
    update_fields = {}
    if name:
        update_fields["name"] = name
    if phone:
        update_fields["phone"] = phone
    if email:
        update_fields["email"] = email

    if not update_fields:
        return None 

    return customers.find_one_and_update(
        {"_id": customer_id},              
        {"$set": update_fields},           
        return_document=ReturnDocument.AFTER 
    )
    
def delete_customer(national_id: str):
    res = customers.delete_one({"_id": national_id})
    return res.deleted_count

def get_all_customers():
    return list(customers.find({}, {"_id": 1, "name": 1, "email": 1, "phone":1}))

def get_customer_by_id(customer_id: str):
    
    return customers.find_one({"_id": customer_id})
