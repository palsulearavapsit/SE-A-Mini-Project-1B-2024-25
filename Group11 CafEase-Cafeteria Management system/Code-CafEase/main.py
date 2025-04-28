import tkinter as tk
from tkinter import messagebox, ttk
import time

class CafeteriaDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Cafeteria Dashboard")
        self.root.geometry("1200x800")
        self.root.config(bg="#f4b860")
        
        # ================= Header Frame with Title and Clock =================
        header_frame = tk.Frame(self.root, bg="#f28c28")
        header_frame.pack(side="top", fill="x")
        
        title_label = tk.Label(header_frame, text="Cafeteria Dashboard",
                               font=("Arial", 28, "bold"), bg="#f28c28", fg="white")
        title_label.pack(side="left", padx=20, pady=10)
        
        # Clock label to display current date and time
        self.clock_label = tk.Label(header_frame, font=("Arial", 16), bg="#f28c28", fg="white")
        self.clock_label.pack(side="right", padx=20)
        self.update_clock()
        
        # ================= Navigation Buttons Frame =================
        nav_frame = tk.Frame(self.root, bg="#f4b860")
        nav_frame.pack(pady=20)
        
        # List of buttons with corresponding commands
        buttons = [
            ("Menu", self.show_menu),
            ("Orders", self.show_orders),
            ("Customer Details", self.show_customer_details),
            ("Generate Bill", self.show_generate_bill),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(nav_frame, text=text,
                            font=("Arial", 16, "bold"), bg="#3498db", fg="white",
                            width=15, height=2, command=command)
            btn.pack(side="left", padx=10)
        
        # ================= Content Frame =================
        self.content_frame = tk.Frame(self.root, bg="white", bd=2, relief="sunken")
        self.content_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Initially display a welcome message
        self.show_welcome()

    def update_clock(self):
        """Updates the clock every second."""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def clear_content_frame(self):
        """Clears all widgets from the content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome(self):
        """Displays a welcome message in the content area."""
        self.clear_content_frame()
        welcome_label = tk.Label(self.content_frame,
                                 text="Welcome to the Cafeteria Dashboard!\nSelect an option above to begin.",
                                 font=("Arial", 20), bg="white", fg="black", justify="center")
        welcome_label.pack(expand=True)

    # ------------------- Menu Section -------------------
    def show_menu(self):
        """Displays the cafeteria menu."""
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Cafeteria Menu",
                         font=("Arial", 22, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)
        
        # Sample menu items
        menu_items = [
            {"Item": "Coffee", "Price": "$2.50"},
            {"Item": "Tea", "Price": "$2.00"},
            {"Item": "Sandwich", "Price": "$5.00"},
            {"Item": "Burger", "Price": "$7.50"},
            {"Item": "Salad", "Price": "$4.00"},
        ]
        
        # Display menu items in a Treeview widget
        columns = ("Item", "Price")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        tree.heading("Item", text="Item")
        tree.heading("Price", text="Price")
        tree.column("Item", width=200, anchor="center")
        tree.column("Price", width=100, anchor="center")
        
        for item in menu_items:
            tree.insert("", "end", values=(item["Item"], item["Price"]))
        tree.pack(pady=20)

    # ------------------- Orders Section -------------------
    def show_orders(self):
        """Displays the list of orders with a search feature."""
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Orders",
                         font=("Arial", 22, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)
        
        # Sample orders data
        orders = [
            {"Order ID": "1001", "Item": "Coffee", "Quantity": 2, "Price": "$5.00"},
            {"Order ID": "1002", "Item": "Sandwich", "Quantity": 1, "Price": "$5.00"},
            {"Order ID": "1003", "Item": "Burger", "Quantity": 3, "Price": "$22.50"},
        ]
        
        # Create a Treeview to display orders
        columns = ("Order ID", "Item", "Quantity", "Price")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)
        
        for order in orders:
            tree.insert("", "end", values=(order["Order ID"], order["Item"], order["Quantity"], order["Price"]))
        tree.pack(pady=20, padx=20, fill="x")
        
        # Add a search feature for Order ID
        search_frame = tk.Frame(self.content_frame, bg="white")
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search Order ID:", font=("Arial", 14), bg="white").pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, font=("Arial", 14))
        search_entry.pack(side="left", padx=5)
        
        def search_order():
            search_id = search_entry.get().strip()
            for child in tree.get_children():
                values = tree.item(child)["values"]
                if str(values[0]) == search_id:
                    tree.selection_set(child)
                    tree.see(child)
                    return
            messagebox.showinfo("Search Result", "Order not found!")
        
        tk.Button(search_frame, text="Search", font=("Arial", 14), bg="#2ecc71",
                  fg="white", command=search_order).pack(side="left", padx=5)

    # ------------------- Customer Details Section -------------------
    def show_customer_details(self):
        """Displays sample customer details."""
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Customer Details",
                         font=("Arial", 22, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)
        
        # Sample customer details
        customers = [
            {"Customer ID": "C001", "Name": "Alice", "Email": "alice@example.com", "Phone": "123-456-7890"},
            {"Customer ID": "C002", "Name": "Bob", "Email": "bob@example.com", "Phone": "987-654-3210"},
            {"Customer ID": "C003", "Name": "Charlie", "Email": "charlie@example.com", "Phone": "555-666-7777"},
        ]
        
        columns = ("Customer ID", "Name", "Email", "Phone")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)
        
        for cust in customers:
            tree.insert("", "end", values=(cust["Customer ID"], cust["Name"], cust["Email"], cust["Phone"]))
        tree.pack(pady=20, padx=20, fill="x")

    # ------------------- Generate Bill Section -------------------
    def show_generate_bill(self):
        """Displays a form to generate a bill."""
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Generate Bill",
                         font=("Arial", 22, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)
        
        form_frame = tk.Frame(self.content_frame, bg="white")
        form_frame.pack(pady=20)
        
        # Order ID
        tk.Label(form_frame, text="Order ID:", font=("Arial", 16), bg="white")\
            .grid(row=0, column=0, padx=10, pady=5, sticky="e")
        order_id_entry = tk.Entry(form_frame, font=("Arial", 16))
        order_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Customer Name
        tk.Label(form_frame, text="Customer Name:", font=("Arial", 16), bg="white")\
            .grid(row=1, column=0, padx=10, pady=5, sticky="e")
        customer_name_entry = tk.Entry(form_frame, font=("Arial", 16))
        customer_name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Items (as a comma-separated list)
        tk.Label(form_frame, text="Items:", font=("Arial", 16), bg="white")\
            .grid(row=2, column=0, padx=10, pady=5, sticky="e")
        items_entry = tk.Entry(form_frame, font=("Arial", 16))
        items_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Total Amount
        tk.Label(form_frame, text="Total Amount:", font=("Arial", 16), bg="white")\
            .grid(row=3, column=0, padx=10, pady=5, sticky="e")
        total_entry = tk.Entry(form_frame, font=("Arial", 16))
        total_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def generate_bill():
            order_id = order_id_entry.get()
            customer_name = customer_name_entry.get()
            items = items_entry.get()
            total = total_entry.get()
            if not order_id or not customer_name or not items or not total:
                messagebox.showerror("Error", "Please fill all fields!")
                return
            # Here you could add logic to store the bill, print an invoice, etc.
            messagebox.showinfo("Bill Generated", f"Bill for Order ID {order_id} has been generated!")
        
        tk.Button(form_frame, text="Generate Bill", font=("Arial", 16, "bold"),
                  bg="#8e44ad", fg="white", command=generate_bill)\
                  .grid(row=4, column=0, columnspan=2, pady=20)

    # ------------------- Logout -------------------
    def logout(self):
        """Logs out after confirmation."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

# ==================== Main Application ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = CafeteriaDashboard(root)
    root.mainloop()
