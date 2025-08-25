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

    
    def add_salesperson(self, first_name, last_name, employment_type):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO salespeople (first_name, last_name, employment_type) VALUES (%s, %s, %s)"
            cursor.execute(query, (first_name, last_name, employment_type))
            self.connection.commit()
            print("Salesperson added successfully")
        except Error as e:
            print(f"Error adding salesperson: {e}")

    def delete_salesperson(self, salesperson_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM salespeople WHERE id = %s"
            cursor.execute(query, (salesperson_id,))
            self.connection.commit()
            print("Salesperson deleted successfully")
        except Error as e:
            print(f"Error deleting salesperson: {e}")

    def view_salespeople(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM salespeople")
            salespeople = cursor.fetchall()
            print("\nSalespeople:")
            for salesperson in salespeople:
                print(f"ID: {salesperson[0]}, Name: {salesperson[1]} {salesperson[2]}, Employment Type: {salesperson[3]}")
        except Error as e:
            print(f"Error viewing salespeople: {e}")

    def add_order(self, customer_id, salesperson_id, order_date):
        """Create a new order and return the order ID"""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO orders (customer_id, salesperson_id, order_date) VALUES (%s, %s, %s)"
            cursor.execute(query, (customer_id, salesperson_id, order_date))
            self.connection.commit()
            order_id = cursor.lastrowid
            print(f"Order created successfully. Order ID: {order_id}")
            return order_id
        except Error as e:
            print(f"Error creating order: {e}")
            return None

    def add_order_item(self, order_id, product_id, quantity):
        """Add a product to an existing order"""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (order_id, product_id, quantity))
            self.connection.commit()
            print("Product added to order successfully")
        except Error as e:
            print(f"Error adding product to order: {e}")

    def delete_order(self, order_id):
        try:
            cursor = self.connection.cursor()
            
            query = "DELETE FROM order_items WHERE order_id = %s"
            cursor.execute(query, (order_id,))
           
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
            SELECT o.id, c.name AS customer, 
                   CONCAT(s.first_name, ' ', s.last_name) AS salesperson,
                   o.order_date, SUM(oi.quantity * p.price) AS total_amount
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN salespeople s ON o.salesperson_id = s.id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            GROUP BY o.id
            ORDER BY o.order_date DESC
            """
            cursor.execute(query)
            orders = cursor.fetchall()
            print("\nOrders Summary:")
            for order in orders:
                print(f"Order ID: {order[0]}, Customer: {order[1]}, "
                      f"Salesperson: {order[2]}, Date: {order[3]}, "
                      f"Total: ${order[4]:.2f}")
        except Error as e:
            print(f"Error viewing orders: {e}")

    def view_order_details(self, order_id):
        """View detailed information about a specific order"""
        try:
            cursor = self.connection.cursor()
            
            
            query_header = """
            SELECT o.id, c.name AS customer, c.email, c.address,
                   CONCAT(s.first_name, ' ', s.last_name) AS salesperson,
                   s.employment_type, o.order_date
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN salespeople s ON o.salesperson_id = s.id
            WHERE o.id = %s
            """
            cursor.execute(query_header, (order_id,))
            order_header = cursor.fetchone()
            
            if order_header:
                print(f"\nOrder Details - ID: {order_header[0]}")
                print(f"Customer: {order_header[1]}")
                print(f"Email: {order_header[2]}")
                print(f"Address: {order_header[3]}")
                print(f"Salesperson: {order_header[4]} ({order_header[5]})")
                print(f"Order Date: {order_header[6]}")
                
              
                query_items = """
                SELECT p.name, p.price, oi.quantity, (p.price * oi.quantity) AS total
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
                """
                cursor.execute(query_items, (order_id,))
                items = cursor.fetchall()
                
                print("\nOrder Items:")
                total_order = 0
                for item in items:
                    print(f"  Product: {item[0]}, Price: ${item[1]:.2f}, "
                          f"Quantity: {item[2]}, Total: ${item[3]:.2f}")
                    total_order += item[3]
                
                print(f"\nOrder Total: ${total_order:.2f}")
            else:
                print(f"Order with ID {order_id} not found.")
                
        except Error as e:
            print(f"Error viewing order details: {e}")

    def list_orders_by_customer(self, customer_id):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT o.id, o.order_date, COUNT(oi.product_id) AS product_count,
                   SUM(oi.quantity * p.price) AS total_amount
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE o.customer_id = %s
            GROUP BY o.id
            ORDER BY o.order_date DESC
            """
            cursor.execute(query, (customer_id,))
            orders = cursor.fetchall()
            print(f"\nOrders for Customer ID {customer_id}:")
            for order in orders:
                print(f"Order ID: {order[0]}, Date: {order[1]}, "
                      f"Products: {order[2]}, Total: ${order[3]:.2f}")
        except Error as e:
            print(f"Error listing orders by customer: {e}")

    def list_orders_by_salesperson(self, salesperson_id):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT o.id, c.name AS customer, o.order_date,
                   COUNT(oi.product_id) AS product_count,
                   SUM(oi.quantity * p.price) AS total_amount
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE o.salesperson_id = %s
            GROUP BY o.id
            ORDER BY o.order_date DESC
            """
            cursor.execute(query, (salesperson_id,))
            orders = cursor.fetchall()
            print(f"\nOrders handled by Salesperson ID {salesperson_id}:")
            for order in orders:
                print(f"Order ID: {order[0]}, Customer: {order[1]}, "
                      f"Date: {order[2]}, Products: {order[3]}, "
                      f"Total: ${order[4]:.2f}")
        except Error as e:
            print(f"Error listing orders by salesperson: {e}")

    def list_orders_by_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT o.id, c.name AS customer, o.order_date,
                   oi.quantity, p.price, (oi.quantity * p.price) AS total
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            JOIN order_items oi ON o.id = oi.order_id
            JOIN products p ON oi.product_id = p.id
            WHERE oi.product_id = %s
            ORDER BY o.order_date DESC
            """
            cursor.execute(query, (product_id,))
            orders = cursor.fetchall()
            print(f"\nOrders containing Product ID {product_id}:")
            for order in orders:
                print(f"Order ID: {order[0]}, Customer: {order[1]}, "
                      f"Date: {order[2]}, Quantity: {order[3]}, "
                      f"Unit Price: ${order[4]:.2f}, Total: ${order[5]:.2f}")
        except Error as e:
            print(f"Error listing orders by product: {e}")

def main():
    store = OnlineStore()
    
    while True:
        print("\nOnline Store Database Management System")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Manage Salespeople")
        print("4. Manage Orders")
        print("5. View Reports")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            
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
            
            print("\nSalesperson Management")
            print("1. Add Salesperson")
            print("2. Delete Salesperson")
            print("3. View Salespeople")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                first_name = input("Enter salesperson first name: ")
                last_name = input("Enter salesperson last name: ")
                employment_type = input("Enter employment type (payroll/on_call): ")
                store.add_salesperson(first_name, last_name, employment_type)
            elif sub_choice == '2':
                salesperson_id = int(input("Enter salesperson ID to delete: "))
                store.delete_salesperson(salesperson_id)
            elif sub_choice == '3':
                store.view_salespeople()
                
        elif choice == '4':
       
            print("\nOrder Management")
            print("1. Create New Order")
            print("2. Add Product to Order")
            print("3. Delete Order")
            print("4. View Orders Summary")
            print("5. View Order Details")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                customer_id = int(input("Enter customer ID: "))
                salesperson_id = int(input("Enter salesperson ID: "))
                order_date = input("Enter order date (YYYY-MM-DD): ")
                store.add_order(customer_id, salesperson_id, order_date)
            elif sub_choice == '2':
                order_id = int(input("Enter order ID: "))
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))
                store.add_order_item(order_id, product_id, quantity)
            elif sub_choice == '3':
                order_id = int(input("Enter order ID to delete: "))
                store.delete_order(order_id)
            elif sub_choice == '4':
                store.view_orders()
            elif sub_choice == '5':
                order_id = int(input("Enter order ID to view details: "))
                store.view_order_details(order_id)
                
        elif choice == '5':
           
            print("\nReports & Special Queries")
            print("1. Orders by Customer")
            print("2. Orders by Salesperson")
            print("3. Orders by Product")
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                customer_id = int(input("Enter customer ID: "))
                store.list_orders_by_customer(customer_id)
            elif sub_choice == '2':
                salesperson_id = int(input("Enter salesperson ID: "))
                store.list_orders_by_salesperson(salesperson_id)
            elif sub_choice == '3':
                product_id = int(input("Enter product ID: "))
                store.list_orders_by_product(product_id)
                
        elif choice == '6':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()