import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="stock.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT NOT NULL,
                              quantity INTEGER NOT NULL,
                              price REAL NOT NULL)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              product_id INTEGER,
                              quantity INTEGER,
                              transaction_type TEXT,
                              date TEXT,
                              FOREIGN KEY(product_id) REFERENCES products(id))''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def add_product(self, name, quantity, price):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")

    def get_products(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

    def update_product_quantity(self, product_id, quantity, transaction_type):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?",
                           (quantity if transaction_type == 'purchase' else -quantity, product_id))
            cursor.execute(
                "INSERT INTO transactions (product_id, quantity, transaction_type, date) VALUES (?, ?, ?, ?)",
                (product_id, quantity, transaction_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error updating product: {e}")

    def get_transactions_by_date(self, start_date, end_date):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE date BETWEEN ? AND ?", (start_date, end_date))
        return cursor.fetchall()

    def get_product_by_id(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()

    def get_all_transactions(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM transactions")
        return cursor.fetchall()
