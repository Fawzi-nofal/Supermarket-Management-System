from pprint import pprint
from products import ensure_products_indexes, create_product, get_all_products, get_product_by_id, update_product, delete_product
from orders import top_products
def menu():
    print("\n=== Products Management ===")
    print("1. Add product")
    print("2. Show all products")
    print("3. Find product by ID")
    print("4. Update product")
    print("5. Delete product")
    print("6. Top selling products")
    print("7. Exit")
    return input("Choose an option: ")

def main():
    ensure_products_indexes()
    while True:
        choice = menu()

        if choice == "1":
            pid = input("Product ID: ")
            name = input("Name: ")
            category = input("Category: ")
            price = float(input("Price: "))
            try:
                create_product(pid, name, category, price)
                print(" Product added successfully")
            except Exception as e:
                print(" Error:", e)

        elif choice == "2":
            pprint(get_all_products())

        elif choice == "3":
            pid = input("Product ID: ")
            pprint(get_product_by_id(pid))

        elif choice == "4":
            pid = input("Product ID: ")
            name = input("New name (or press Enter to skip): ") or None
            category = input("New category (or press Enter to skip): ") or None
            price_in = input("New price (or press Enter to skip): ")
            price = float(price_in) if price_in else None
            updated = update_product(pid, name=name, category=category, price=price)
            pprint(updated)

        elif choice == "5":
            pid = input("Product ID: ")
            deleted = delete_product(pid)
            print(" Deleted" if deleted else " Product not found")
            
        elif choice == "6":
            try:
                result = top_products()  # מחזיר את המוצר היחיד הכי נמכר
                if not result:
                    print(" No data.")
                else:
                    pid = result["_id"]
                    qty = result["totalSold"]
                    prod = get_product_by_id(pid)  # כדי להציג גם שם
                    name = prod["name"] if prod and "name" in prod else "(no name)"
                    cat = prod.get("category") if prod else None
                    print(f"Top selling product: {name} [ID: {pid}] — units sold: {qty}" + (f", category: {cat}" if cat else ""))
            except Exception as e:
                print(" Error:", e)

        elif choice == "7":
            print(" Exiting...")
            break

        elif choice == "7":
            print(" Exiting...")
            break
        else:
            print(" Invalid choice")

if __name__ == "__main__":
    main()
