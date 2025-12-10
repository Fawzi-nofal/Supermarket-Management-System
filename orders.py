from datetime import datetime, timezone
from db import orders_coll
from pymongo import ReturnDocument ,ASCENDING,DESCENDING
from pymongo.errors import DuplicateKeyError

orders = orders_coll()
def ensure_orders_indexes():
    orders.create_index([("customerId", ASCENDING)], name="customerId_asc")
    orders.create_index([("createdAt", DESCENDING)], name="createdAt_desc")
    orders.create_index([("status", ASCENDING), ("createdAt", DESCENDING)], name="status_createdAt")

def create_order(order_id: str, customer_id: str, items: list):
    
    for item in items:
        if "productId" not in item or "price" not in item:
            raise ValueError("Each item must have productId and price")
        if item.get("quantity", 1) < 0 or item["price"] < 0:
            raise ValueError("Price and quantity must be non-negative")
    
    total = sum(item["price"] * item.get("quantity", 1) for item in items)

    doc = {
        "_id": order_id,
        "customerId": customer_id,
        "items": items,
        "totalAmount": total,
        "status": "paid",   # ברירת מחדל
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc)
    }
    try:
        orders.insert_one(doc)
        return order_id
    except DuplicateKeyError:
        raise ValueError(f"Order with id {order_id} already exists")

def update_order(order_id: str, status: str = None, items: list = None):
    update_fields = {}
    if status is not None:
        update_fields["status"] = status
    if items is not None:
        total = sum(item["price"] * item.get("quantity", 1) for item in items)
        update_fields["items"] = items
        update_fields["totalAmount"] = total

    if not update_fields:
        return get_order_by_id(order_id)

    update_fields["updatedAt"] = datetime.utcnow()

    return orders.find_one_and_update(
        {"_id": order_id},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )
def delete_order(order_id: str) -> int:
    res = orders.delete_one({"_id": order_id})
    return res.deleted_count

def total_revenue():
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$totalAmount"}}}
    ]
    result = list(orders.aggregate(pipeline))
    return result[0]["total"] if result else 0

def top_customers(limit=1):
    pipeline = [
        {"$group": {"_id": "$customerId", "ordersCount": {"$sum": 1}}},
        {"$sort": {"ordersCount": -1}},
        {"$limit": limit}
    ]
    return list(orders.aggregate(pipeline))

def top_products():
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {"_id": "$items.productId", "totalSold": {"$sum": "$items.quantity"}}},
        {"$sort": {"totalSold": -1}},
        {"$limit": 1}
    ]
    result = list(orders.aggregate(pipeline))
    return result[0] if result else None



def get_order_by_id(order_id: str):
    return orders.find_one({"_id": order_id})

def list_orders(customer_id: str = None, limit: int = 100, skip: int = 0):
    query = {"customerId": customer_id} if customer_id else {}
    return list(orders.find(query).skip(skip).limit(limit))
