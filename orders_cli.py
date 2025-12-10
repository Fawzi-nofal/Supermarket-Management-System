from pprint import pprint
from orders import ensure_orders_indexes, create_order, get_order_by_id, list_orders, update_order, delete_order ,total_revenue
from products import get_product_by_id

def menu():
    print("\n=== Orders Management ===")
    print("1. Create order")
    print("2. Show all orders for a customer")
    print("3. Find order by ID")
    print("4. Update order status")
    print("5. Delete order")
    print("6. Total revenue")
    print("7. Exit")
    return input("Choose an option: ")

def main():
    ensure_orders_indexes()
    while True:
        choice = menu()

        if choice == "1":
            oid = input("Order ID: ")
            cid = input("Customer ID: ")
            items = []

            while True:
                pid = input("Product ID (or press Enter to finish): ")
                if not pid:
                    break

                product = get_product_by_id(pid)   # שולפים את המוצר ממונגו
                if not product:
                    print(f" Product with ID {pid} not found")
                    continue

                qty = int(input("Quantity: "))
                price = product["price"]  # מחיר נשלף מהמסד, לא מהמשתמש

                items.append({
                    "productId": pid,
                    "name": product["name"],   # שם המוצר מתוך המסד
                    "quantity": qty,
                    "price": price
                })

            try:
                create_order(oid, cid, items)
                print(" Order created successfully")
            except Exception as e:
                print(" Error:", e)
        elif choice == "2":
            cid = input("Customer ID: ")
            pprint(list_orders(cid))

        elif choice == "3":
            oid = input("Order ID: ")
            pprint(get_order_by_id(oid))

        elif choice == "4":
            oid = input("Order ID: ")
            status = input("New status (paid/shipped/cancelled): ")
            updated = update_order(oid, status=status)
            pprint(updated)

        elif choice == "5":
            oid = input("Order ID: ")
            deleted = delete_order(oid)
            print(" Deleted" if deleted else " Order not found")
        elif choice == "6":
            # Total revenue
            try:
                total = total_revenue()
                print(f"Total revenue: {total}")
            except Exception as e:
                print(" Error:", e)

        elif choice == "7":
            print(" Exiting...")
            break
        else:
            print(" Invalid choice")

if __name__ == "__main__":
    main()
