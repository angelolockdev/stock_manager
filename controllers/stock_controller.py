from database.db_manager import DatabaseManager

class StockController:
    def __init__(self):
        self.db = DatabaseManager()

    def add_product(self, name, quantity, price):
        return self.db.add_product(name, quantity, price)

    def get_products(self):
        return self.db.get_products()

    def update_product_quantity(self, product_id, quantity, transaction_type):
        return self.db.update_product_quantity(product_id, quantity, transaction_type)

    def generate_report(self, start_date, end_date):
        return self.db.get_transactions_by_date(start_date, end_date)

    def get_product_by_id(self, product_id):
        return self.db.get_product_by_id(product_id)

    def get_all_transactions(self):
        return self.db.get_all_transactions()
