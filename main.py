from customers_cli import main as customers_menu
from products_cli import main as products_menu
from orders_cli import main as orders_menu


def menu():
    print("\n=== Shop Management System (Main Menu) ===")
    print("1. Customers")
    print("2. Products")
    print("3. Orders")
    print("4. Exit")
    return input("Choose an option: ")


def main():
    while True:
        choice = menu()

        if choice == "1":
            customers_menu()
        elif choice == "2":    
            products_menu()
        elif choice == "3":
            orders_menu()
        elif choice == "4":
            print(" Exiting...")
            break
        else:
            print(" Invalid choice, please try again.")


if __name__ == "__main__":
    main() 