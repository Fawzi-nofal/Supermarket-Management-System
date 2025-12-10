from pprint import pprint
from customers import ensure_customers_indexes, create_customer, get_all_customers, update_customer, delete_customer, get_customer_by_id
from orders import top_customers

def menu():
    print("\n=== Customers Management ===")
    print("1. Add customer")
    print("2. Show all customers")
    print("3. Find customer by ID")
    print("4. Update customer")
    print("5. Delete customer")
    print("6. Top customers")
    print("7. Exit")
    return input("Choose an option: ")

def main():
    ensure_customers_indexes()
    while True:
        choice = menu()

        if choice == "1":
            cust_id = input("Customer ID: ")
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            try:
                create_customer(customer_id=cust_id, name=name, email=email, phone=phone)
                print("Customer added successfully")
            except Exception as e:
                print(" Error:", e)

        elif choice == "2":
            pprint(get_all_customers())

        elif choice == "3":
            cid = input("Customer ID: ")
            pprint(get_customer_by_id(cid))

        elif choice == "4":
            cid = input("Customer ID: ")
            name = input("New name (or press Enter to skip): ") or None
            email = input("New email (or press Enter to skip): ") or None
            phone = input("New phone (or press Enter to skip): ") or None
            updated = update_customer(cid, name=name, email=email, phone=phone)
            pprint(updated)

        elif choice == "5":
            cid = input("Customer ID: ")
            deleted = delete_customer(cid)
            print(" Deleted" if deleted else " Customer not found")
        
        elif choice == "6":
            try:
                n = int(input("How many top customers? (default 5): ") or "5")
                results = top_customers(limit=n)  # מגיע מתוך orders.py
                print("Top customers by number of orders:")
                for row in results:
                    cid = row["_id"]
                    cnt = row["ordersCount"]
                    cust = get_customer_by_id(cid)  # כדי להציג גם שם
                    name = cust["name"] if cust and "name" in cust else "(no name)"
                    print(f"- {name} [ID: {cid}] — orders: {cnt}")
            except Exception as e:
                print(" Error:", e)

        elif choice == "7":
            print(" Exiting...")
            break
        else:
            print(" Invalid choice")

if __name__ == "__main__":
    main()
