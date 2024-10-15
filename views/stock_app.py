import tkinter as tk
from tkinter import messagebox, ttk
from controllers.stock_controller import StockController
import openpyxl

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        self.controller = StockController()

        self.create_widgets()

    def create_widgets(self):
        # Boutons principaux
        self.btn_show_products = tk.Button(self.root, text="Afficher Produits", command=self.show_products)
        self.btn_show_products.grid(row=0, column=0, padx=10, pady=10)

        self.btn_add_product = tk.Button(self.root, text="Ajouter Produit", command=self.add_product)
        self.btn_add_product.grid(row=0, column=1, padx=10, pady=10)

        self.btn_purchase = tk.Button(self.root, text="Acheter Produit", command=self.purchase_product)
        self.btn_purchase.grid(row=0, column=2, padx=10, pady=10)

        self.btn_sell = tk.Button(self.root, text="Vendre Produit", command=self.sell_product)
        self.btn_sell.grid(row=0, column=3, padx=10, pady=10)

        self.btn_report = tk.Button(self.root, text="Générer Rapport", command=self.generate_report)
        self.btn_report.grid(row=0, column=4, padx=10, pady=10)

        self.btn_export_excel = tk.Button(self.root, text="Exporter en Excel", command=self.export_to_excel)
        self.btn_export_excel.grid(row=0, column=5, padx=10, pady=10)

    def show_products(self):
        product_list_window = tk.Toplevel(self.root)
        product_list_window.title("Liste des Produits")

        # Cadre pour le tableau et la barre de défilement
        frame_tree = tk.Frame(product_list_window)
        frame_tree.grid(row=0, column=0, padx=10, pady=10)

        # Utilisation de ttk pour le tableau
        tree = ttk.Treeview(frame_tree, columns=("ID", "Nom", "Quantité", "Prix"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nom", text="Nom")
        tree.heading("Quantité", text="Quantité")
        tree.heading("Prix", text="Prix")
        tree.pack(side="left", fill="both", expand=True)

        # Barre de défilement verticale
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Fonction pour rafraîchir le tableau
        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            products = self.controller.get_products()
            for product in products:
                tree.insert("", "end", values=(product[0], product[1], product[2], product[3]))

        # Initialiser le tableau avec les produits
        refresh_tree()

        # Cadre pour l'étiquette et les boutons
        frame_selection = tk.Frame(product_list_window)
        frame_selection.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frame_selection.columnconfigure(0, weight=1)
        frame_selection.columnconfigure(1, weight=1)
        frame_selection.columnconfigure(2, weight=1)

        # Étiquette dynamique pour afficher les détails du produit sélectionné
        selected_product_label = tk.Label(frame_selection, text="Sélectionnez un produit pour voir les détails")
        selected_product_label.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        # Variables pour stocker l'ID du produit sélectionné
        selected_product_id = tk.StringVar()

        # Fonction pour mettre à jour l'étiquette dynamique et l'ID du produit sélectionné
        def on_tree_select(event):
            selected_item = tree.selection()
            if selected_item:
                item_values = tree.item(selected_item, "values")
                selected_product_id.set(item_values[0])
                selected_product_label.config(text=f"Produit sélectionné: {item_values[1]} - Quantité: {item_values[2]} - Prix: {item_values[3]} Ariary")
                btn_acheter.config(state="normal")
                btn_vendre.config(state="normal")
            else:
                btn_acheter.config(state="disabled")
                btn_vendre.config(state="disabled")

        # Lier l'événement de sélection de ligne à la fonction
        tree.bind("<<TreeviewSelect>>", on_tree_select)

        # Bouton Acheter
        btn_acheter = tk.Button(frame_selection, text="Acheter", state="disabled", command=lambda: self.purchase_product(selected_product_id.get(), refresh_tree))
        btn_acheter.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Bouton Vendre
        btn_vendre = tk.Button(frame_selection, text="Vendre", state="disabled", command=lambda: self.sell_product(selected_product_id.get(), refresh_tree))
        btn_vendre.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

    def add_product(self):
        def submit():
            name = entry_name.get()
            quantity = int(entry_quantity.get())
            price = float(entry_price.get())
            self.controller.add_product(name, quantity, price)
            add_product_window.destroy()

        add_product_window = tk.Toplevel(self.root)
        add_product_window.title("Ajouter Produit")

        tk.Label(add_product_window, text="Nom").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(add_product_window, text="Quantité").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(add_product_window, text="Prix").grid(row=2, column=0, padx=10, pady=10)

        entry_name = tk.Entry(add_product_window)
        entry_quantity = tk.Entry(add_product_window)
        entry_price = tk.Entry(add_product_window)

        entry_name.grid(row=0, column=1, padx=10, pady=10)
        entry_quantity.grid(row=1, column=1, padx=10, pady=10)
        entry_price.grid(row=2, column=1, padx=10, pady=10)

        btn_submit = tk.Button(add_product_window, text="Ajouter", command=submit)
        btn_submit.grid(row=3, column=1, padx=10, pady=10)

    def purchase_product(self, product_id=None, refresh_callback=None):
        self.simulate_transaction("purchase", product_id, refresh_callback)

    def sell_product(self, product_id=None, refresh_callback=None):
        self.simulate_transaction("sale", product_id, refresh_callback)

    def simulate_transaction(self, transaction_type, product_id=None, refresh_callback=None):
        def submit():
            selected_product_label = combobox_product_id.get()
            selected_product_id = product_id if product_id else product_map[selected_product_label]
            quantity = int(entry_quantity.get())
            if transaction_type == "sale":
                product = self.controller.get_product_by_id(selected_product_id)
                if product and product[2] < quantity:
                    messagebox.showerror("Erreur", "Quantité insuffisante pour la vente.")
                    return
            self.controller.update_product_quantity(selected_product_id, quantity, transaction_type)
            transaction_window.destroy()
            if refresh_callback:
                refresh_callback()

        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Simuler Transaction")

        tk.Label(transaction_window, text="Produit").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(transaction_window, text="Quantité").grid(row=1, column=0, padx=10, pady=10)

        # Liste des produits pour la sélection
        products = self.controller.get_products()
        product_map = {f"{product[1]}": product[0] for product in products}  # Map product name to ID
        product_names = list(product_map.keys())

        # Utilisation de Combobox pour la sélection du produit
        combobox_product_id = ttk.Combobox(transaction_window, values=product_names, state="readonly")
        combobox_product_id.grid(row=0, column=1, padx=10, pady=10)

        entry_quantity = tk.Entry(transaction_window)
        entry_quantity.grid(row=1, column=1, padx=10, pady=10)

        btn_submit = tk.Button(transaction_window, text="Valider", command=submit)
        btn_submit.grid(row=2, column=1, padx=10, pady=10)

    def export_to_excel(self):
        products = self.controller.get_products()
        transactions = self.controller.get_all_transactions()

        workbook = openpyxl.Workbook()
        sheet_products = workbook.active
        sheet_products.title = "Produits"

        # En-tête pour la liste des produits
        headers = ["ID", "Nom", "Quantité", "Prix"]
        sheet_products.append(headers)

        # Ajouter les produits
        for product in products:
            sheet_products.append(list(product))

        # Créer un onglet pour les transactions
        sheet_transactions = workbook.create_sheet(title="Transactions")
        headers_transactions = ["ID", "ID Produit", "Quantité", "Type de transaction", "Date"]
        sheet_transactions.append(headers_transactions)

        # Ajouter les transactions
        for transaction in transactions:
            sheet_transactions.append(list(transaction))

        workbook.save("rapport_stock.xlsx")
        messagebox.showinfo("Exportation réussie", "Les données ont été exportées vers rapport_stock.xlsx")

    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Générer Rapport")

        tk.Label(report_window, text="Date de Début (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(report_window, text="Date de Fin (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=10)

        entry_start_date = tk.Entry(report_window)
        entry_end_date = tk.Entry(report_window)

        entry_start_date.grid(row=0, column=1, padx=10, pady=10)
        entry_end_date.grid(row=1, column=1, padx=10, pady=10)

        # Utilisation de ttk pour afficher les transactions sous forme de tableau
        tree = ttk.Treeview(report_window, columns=("ID", "ID Produit", "Quantité", "Type", "Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("ID Produit", text="ID Produit")
        tree.heading("Quantité", text="Quantité")
        tree.heading("Type", text="Type")
        tree.heading("Date", text="Date")
        tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Fonction pour rafraîchir le tableau
        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            start_date = entry_start_date.get()
            end_date = entry_end_date.get()
            transactions = self.controller.generate_report(start_date, end_date)
            for transaction in transactions:
                tree.insert("", "end", values=(transaction[0], transaction[1], transaction[2], transaction[3], transaction[4]))

        btn_submit = tk.Button(report_window, text="Générer", command=refresh_tree)
        btn_submit.grid(row=2, column=1, padx=10, pady=10)
