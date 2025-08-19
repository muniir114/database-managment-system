import mysql.connector
from mysql.connector import Error

class OnlineStore:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='online_store'
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    # CRUD operations for Products
    def add_product(self, name, price, description):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, price, description))
            self.connection.commit()
            print("Product added successfully")
        except Error as e:
            print(f"Error adding product: {e}")

    def delete_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            self.connection.commit()
            print("Product deleted successfully")
        except Error as e:
            print(f"Error deleting product: {e}")

    def view_products(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            print("\nProducts:")
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}, Description: {product[3]}")
        except Error as e:
            print(f"Error viewing products: {e}")

    # CRUD operations for Customers
    def add_customer(self, name, email, address):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO customers (name, email, address) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, address))
            self.connection.commit()
            print("Customer added successfully")
        except Error as e:
            print(f"Error adding customer: {e}")

    def delete_customer(self, customer_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM customers WHERE id = %s"
            cursor.execute(query, (customer_id,))
            self.connection.commit()
            print("Customer deleted successfully")
        except Error as e:
            print(f"Error deleting customer: {e}")

    def view_customers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM customers")
            customers = cursor.fetchall()
            print("\nCustomers:")
            for customer in customers:
                print(f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Address: {customer[3]}")
        except Error as e:
            print(f"Error viewing customers: {e}")

    # CRUD operations for Orders
    def add_order(self, customer_id, product_id, quantity, order_date):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (customer_id, product_id, quantity, order_date))
            self.connection.commit()
            print("Order added successfully")
        except Error as e:
            print(f"Error adding order: {e}")

    def delete_order(self, order_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            self.connection.commit()
            print("Order deleted successfully")
        except Error as e:
            print(f"Error deleting order: {e}")

    def view_orders(self):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT o.id, c.name AS customer, p.name AS product, o.quantity, p.price, 
                   (o.quantity * p.price) AS total, o.order_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN products p ON o.product_id = p.id
            """
            cursor.execute(query)
            orders = cursor.fetchall()
            print("\nOrders:")
            for order in orders:
                print(f"Order ID: {order[0]}, Customer: {order[1]}, Product: {order[2]}, "
                      f"Quantity: {order[3]}, Unit Price: ${order[4]:.2f}, "
                      f"Total: ${order[5]:.2f}, Date: {order[6]}")
        except Error as e:
            print(f"Error viewing orders: {e}")

    # Special queries
    def list_orders_by_customer(self, customer_id):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT o.id, p.name AS product, o.quantity, p.price, 
                   (o.quantity * p.price) AS total, o.order_date
            FROM orders o
            JOIN products p ON o.product_id = p.id
            WHERE o.customer_id = %s
            """
            cursor.execute(query, (customer_id,))
            orders = cursor.fetchall()
            print(f"\nOrders for Customer ID {customer_id}:")
            for order in orders:
                print(f"Order ID: {order[0]}, Product: {order[1]}, Quantity: {order[2]}, "
                      f"Unit Price: ${order[3]:.2f}, Total: ${order[4]:.2f}, Date: {order[5]}")
        except Error as e:
            print(f"Error listing orders by customer: {e}")

    def list_orders_by_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT o.id, c.name AS customer, o.quantity, p.price, 
                   (o.quantity * p.price) AS total, o.order_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN products p ON o.product_id = p.id
            WHERE o.product_id = %s
            """
            cursor.execute(query, (product_id,))
            orders = cursor.fetchall()
            print(f"\nOrders for Product ID {product_id}:")
            for order in orders:
                print(f"Order ID: {order[0]}, Customer: {order[1]}, Quantity: {order[2]}, "
                      f"Unit Price: ${order[3]:.2f}, Total: ${order[4]:.2f}, Date: {order[5]}")
        except Error as e:
            print(f"Error listing orders by product: {e}")

def main():
    store = OnlineStore()
    
    while True:
        print("\nOnline Store Database Management System")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Manage Orders")
        print("4. Special Queries")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Product management
            print("\nProduct Management")
            print("1. Add Product")
            print("2. Delete Product")
            print("3. View Products")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                description = input("Enter product description: ")
                store.add_product(name, price, description)
            elif sub_choice == '2':
                product_id = int(input("Enter product ID to delete: "))
                store.delete_product(product_id)
            elif sub_choice == '3':
                store.view_products()
                
        elif choice == '2':
            # Customer management
            print("\nCustomer Management")
            print("1. Add Customer")
            print("2. Delete Customer")
            print("3. View Customers")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                address = input("Enter customer address: ")
                store.add_customer(name, email, address)
            elif sub_choice == '2':
                customer_id = int(input("Enter customer ID to delete: "))
                store.delete_customer(customer_id)
            elif sub_choice == '3':
                store.view_customers()
                
        elif choice == '3':
            # Order management
            print("\nOrder Management")
            print("1. Add Order")
            print("2. Delete Order")
            print("3. View Orders")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                customer_id = int(input("Enter customer ID: "))
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))
                order_date = input("Enter order date (YYYY-MM-DD): ")
                store.add_order(customer_id, product_id, quantity, order_date)
            elif sub_choice == '2':
                order_id = int(input("Enter order ID to delete: "))
                store.delete_order(order_id)
            elif sub_choice == '3':
                store.view_orders()
                
        elif choice == '4':
            # Special queries
            print("\nSpecial Queries")
            print("1. List all orders from a specific customer")
            print("2. List all orders that contain a specific product")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                customer_id = int(input("Enter customer ID: "))
                store.list_orders_by_customer(customer_id)
            elif sub_choice == '2':
                product_id = int(input("Enter product ID: "))
                store.list_orders_by_product(product_id)
                
        elif choice == '5':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()