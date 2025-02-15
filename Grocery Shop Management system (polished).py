import mysql.connector
import time
import sys

class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

class ElectronicShop:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="coffee",
            database="trial_code"
        )
        self.cursor = self.db_connection.cursor()

    def add_product(self, product):
        sql = "CREATE TABLE IF NOT EXISTS products (id INT PRIMARY KEY, name VARCHAR(255), price INT, quantity INT)"
        check_sql = "SELECT id FROM products WHERE id = %s"
        check_values = (product.id,)
        self.cursor.execute(check_sql, check_values)
        existing_product = self.cursor.fetchone()

        if existing_product:
            print_typing_effect("A product with the same ID already exists. Please choose a different ID.\n")

            
        else:
            insert_sql = "INSERT INTO products (id, name, price, quantity) VALUES (%s, %s, %s, %s)"
            insert_values = (product.id, product.name, product.price, product.quantity)
            self.cursor.execute(insert_sql, insert_values)
            self.db_connection.commit()
            print_typing_effect("\nProduct added successfully.\n")

    def update_product(self, product_id, new_quantity):
        sql_select = "SELECT quantity FROM products WHERE id = %s"
        select_values = (product_id,)
        self.cursor.execute(sql_select, select_values)
        existing_quantity = self.cursor.fetchone()

        if existing_quantity and existing_quantity[0] == new_quantity:
            print_typing_effect("Product quantity remains unchanged.")
        else:
            sql_update = "UPDATE products SET quantity = %s WHERE id = %s"
            update_values = (new_quantity, product_id)
            self.cursor.execute(sql_update, update_values)
            self.db_connection.commit()

            if self.cursor.rowcount == 0:
                print_typing_effect("Product not found!")
            else:
                print_typing_effect("Product quantity updated successfully.\n")
                
    def delete_product(self, product_id):
        sql = "DELETE FROM products WHERE id = %s"
        values = (product_id,)
        self.cursor.execute(sql, values)
        self.db_connection.commit()
        if self.cursor.rowcount == 0:
            print_typing_effect("Product not found!")
        else:
            print_typing_effect("Product deleted successfully.")

    def display_inventory(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('')
        print_typing_effect("INVENTORY --->\n")
        for row in result:
            print_typing_effect(f"ID: {row[0]}, Name: {row[1]},\t Price: {row[2]},\t Quantity: {row[3]}\n")
        print('')

    def display_products(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('')
        print_typing_effect("PRODUCTS --->\n")
        for row in result:
            print_typing_effect(f"ID: {row[0]}, Name: {row[1]},\t Price: {row[2]},\t Quantity: {row[3]}\n")
        print('')

class Customer:
    def __init__(self, customer_number, customer_name, customer_email):
        self.customer_number = customer_number
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="coffee",
            database="trial_code"
        )
        self.cursor = self.db_connection.cursor()

        self.create_customer_table()

    def create_customer_table(self):
        sql = "CREATE TABLE IF NOT EXISTS customers (number BIGINT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))"
        self.cursor.execute(sql)
        self.db_connection.commit()

        sql = "INSERT INTO customers (number, name, email) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name), email = VALUES(email)"
        values = (self.customer_number, self.customer_name, self.customer_email)
        self.cursor.execute(sql, values)
        self.db_connection.commit()

    def view_inventory(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print('')
        print_typing_effect("Inventory --->\n")
        for row in result:
            print_typing_effect(f"ID: {row[0]},       Name: {row[1]},       Price: {row[2]},       Quantity: {row[3]}")
        print('')

    def buy_products(self):
        products = []

        while True:
            try:
             product_id = int(input_with_typing("Enter the product ID you want to buy (0 to stop): "))
            except ValueError:
                print("Invalid input. Please try again")
                continue
            
            if product_id == 0:
                break
            try:
                quantity = int(input_with_typing(f"Enter the quantity of product {product_id}: "))
            except ValueError:
                print('Invalid input. Please try again.')
                continue
                
            if quantity<0:
                print_typing_effect('Invalid Input. Please try again !!')
                continue

            sql = "SELECT id, name, price, quantity FROM products WHERE id = %s"
            values = (product_id,)
            self.cursor.execute(sql, values)
            product_data = self.cursor.fetchone()

            if not product_data:
                print_typing_effect(f"\nProduct with ID {product_id} not found.\n")
                continue

            product = Product(*product_data)

            if product.quantity >= quantity:
                total_cost = product.price * quantity
                products.append((product.name, quantity, total_cost))
                sql = "UPDATE products SET quantity = quantity - %s WHERE id = %s"
                values = (quantity, product_id)
                self.cursor.execute(sql, values)
                self.db_connection.commit()
            else:
                print_typing_effect(f"\nSorry, only {product.quantity} {product.name}(s) available.\n")

        if products:
            total_bill = sum(item[2] for item in products)
            print_typing_effect("\n------------------------ Grocery shop Bill ------------------------\n\n")
            print_typing_effect(f"Customer Name: {self.customer_name}\nCustomer Number: {self.customer_number}\nCustomer Email: {self.customer_email}\n")
            print_typing_effect("Items Bought:\n")
            for name, quantity, cost in products:
                print_typing_effect(f"Product: {name},       Quantity: {quantity},       Cost: ${cost:.2f}\n")
            print('')
            print_typing_effect(f"TOTAL BILL: ${total_bill:.2f}\n")
        else:
            print_typing_effect("\nNo items purchased.\n")
    def __del__(self):
        self.db_connection.close()

def print_typing_effect(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def input_with_typing(prompt, delay=0.02):
    print_typing_effect(prompt, delay)
    return input()

def print_menu():
    print('--------------------------------------------------------------------------')
    print_typing_effect("\n               GROCERY SHOP MANAGEMENT SYSTEM               ")
    time.sleep(0.5)
    print_typing_effect("\n\n• Owner's Options --->\n")
    time.sleep(0.1)
    print_typing_effect("   1.Add product\n")
    time.sleep(0.1)
    print_typing_effect("   2.Update product quantity\n")
    time.sleep(0.1)
    print_typing_effect("   3.Delete product\n")
    time.sleep(0.1)
    print_typing_effect("   4.Display inventory\n")
    time.sleep(0.1)
    print_typing_effect("\n• Customer's Options --->\n")
    time.sleep(0.1)
    print_typing_effect("   5.Display products\n")
    time.sleep(0.1)
    print_typing_effect("   6.Buy products\n")
    time.sleep(0.1)
    print_typing_effect("   7.Exit")

# MySQL connection setup for product table
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="coffee",
    database="trial_code"
)
cursor = db_connection.cursor()

# Creating the products table
create_products_table_sql = '''
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    price FLOAT,
    quantity INT
);
'''
cursor.execute(create_products_table_sql)
db_connection.commit()

# Closing the cursor and database connection for product table
cursor.close()
db_connection.close()

# Creating an instance of the ElectronicShop class
shop = ElectronicShop()

while True:
    print_menu()
    choice = input_with_typing("\nEnter your choice: ")

    if choice == "1":
        # Add product functionality
        try:
         id = int(input_with_typing("Enter product ID: "))
        except ValueError:
            print_typing_effect("Invalid ID! Please try again\n")
            continue

        name =  input_with_typing("Enter product name: ")
        
        try:
         price = float(input_with_typing("Enter product price: "))
        except ValueError:
            print_typing_effect("Invalid price! Please try again.\n")
            continue
        try:
         quantity = int(input_with_typing("Enter product quantity: "))
        except ValueError:
            print_typing_effect("Invalid quantity! Please try again.\n")
            continue
        
        product = Product(id, name, price, quantity)
        if id<0 or price<0 or quantity<0:
            print_typing_effect("Invalid entry! Please try again.\n")
        elif name.isalpha()==False:
            print_typing_effect("Invalid name, Please try again\n")
        elif id>=0 and price>=0 and quantity>=0:
            shop.add_product(product)
        else:
            print_typing_effect('Invalid input detected.')


    elif choice == "2":
        # Update product quantity functionality
        try:
         product_id = int(input_with_typing("Enter product ID: "))
        except ValueError:
            print_typing_effect("Invalid ID\n")
            continue
        
        try:
         new_quantity = int(input_with_typing("Enter new quantity: "))
        except ValueError:
            print_typing_effect("Invalid quantity! Please try again.\n")
            continue
        
        if new_quantity <0:
            print("Invalid entry! Please try again.\n")
        else:
         shop.update_product(product_id, new_quantity)
        print()


    elif choice == "3":
        # Delete product functionality
        try:
         product_id = int(input_with_typing("Enter product ID: "))
        except ValueError:
            print_typing_effect("Invalid ID! Please try again.\n")
            continue
        shop.delete_product(product_id)
        print()

    elif choice == "4":
        # Display inventory functionality
        shop.display_inventory()
        print()

    elif choice == "5":
        # Display products functionality
        shop.display_products()
        print()


    elif choice == "6":
        # Buy products functionality
        try:
         customer_number = int(input_with_typing("Enter your customer number: "))
        except ValueError:
            print_typing_effect("Invalid Number! Please try again.\n")
            continue
        
        if 10000000000>customer_number>999999999:
            customer_name = input_with_typing("Enter your name: ")
            customer_email = input_with_typing("Enter your email: ")
            if customer_name.isalpha()==False:
                print_typing_effect("Invalid name, Please try again\n")
                
            elif 'gmail.com' in customer_email:
                customer = Customer(customer_number, customer_name, customer_email)
                customer.buy_products()
                print()
            elif 'outlook.com' in customer_email:
                customer = Customer(customer_number, customer_name, customer_email)
                customer.buy_products()
            elif 'rediffmail.com' in customer_email:
                customer = Customer(customer_number, customer_name, customer_email)
                customer.buy_products()
            elif 'yahoo.com' in customer_email:
                customer = Customer(customer_number, customer_name, customer_email)
                customer.buy_products()
            elif 'hotmail.com' in customer_email:
                customer = Customer(customer_number, customer_name, customer_email)
                customer.buy_products()
            
            else:
                print_typing_effect("Invalid mail ID\n")
                
        else:
            print_typing_effect('The number you entered is not valid, please try again.\n')

    elif choice == "7":
        # Exiting the program
        print_typing_effect("\n\nWE HOPE TO SEE YOU AGAIN !!! \n")
        time.sleep(1.0)
        print_typing_effect("Exiting the program...")
        break

    else:
        print_typing_effect("Invalid choice. Please try again.\n")
        print()

# Closing the cursor and database connection for the ElectronicShop instance
shop.cursor.close()
shop.db_connection.close()
