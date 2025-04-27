import tkinter as tk
from tkinter import messagebox, ttk
import time
import mysql.connector
from cafeorder import CafeBillingSystem  # Make sure you have cafeorder.py

# Database Connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="12345",  # Your MySQL password
        database="cafe_billing"  # Make sure database exists
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to database: {err}")

class CafeteriaDashboard:
    def __init__(self, root):  # <-- fixed __init__
        self.root = root
        self.root.title("Cafeteria Dashboard")
        self.root.geometry("1200x800")
        self.root.config(bg="#f4b860")
        
        # ================= Header Frame =================
        header_frame = tk.Frame(self.root, bg="#f28c28")
        header_frame.pack(side="top", fill="x")
        
        title_label = tk.Label(header_frame, text="Cafeteria Dashboard",
                               font=("Arial", 28, "bold"), bg="#f28c28", fg="white")
        title_label.pack(side="left", padx=20, pady=10)
        
        self.clock_label = tk.Label(header_frame, font=("Arial", 16), bg="#f28c28", fg="white")
        self.clock_label.pack(side="right", padx=20)
        self.update_clock()
        
        # ================= Navigation Buttons =================
        nav_frame = tk.Frame(self.root, bg="#f4b860")
        nav_frame.pack(pady=20)
        
        buttons = [
            ("Menu", self.show_menu),
            ("Order", self.show_orders),
            ("Customer Details", self.show_customers),
            ("Update Menu", self.show_update_menu),
            ("Generate Bill", self.generate_bill),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(nav_frame, text=text,
                            font=("Arial", 16, "bold"), bg="#3498db", fg="white",
                            width=15, height=2, command=command)
            btn.pack(side="left", padx=10)
        
        self.content_frame = tk.Frame(self.root, bg="white", bd=2, relief="sunken")
        self.content_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.show_welcome()
    
    def update_clock(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_welcome(self):
        self.clear_content_frame()
        welcome_label = tk.Label(self.content_frame,
                                 text="Welcome to the Cafeteria Dashboard!\nSelect an option above to begin.",
                                 font=("Arial", 20), bg="white", fg="black", justify="center")
        welcome_label.pack(expand=True)
    
    # ------------------- Menu Section -------------------
    def show_menu(self):
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Cafeteria Menu",
                         font=("Arial", 30, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)
        
        columns = ("Item", "Price")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=8)
        tree.heading("Item", text="Item")
        tree.heading("Price", text="Price")
        tree.column("Item", width=200, anchor="center")
        tree.column("Price", width=100, anchor="center")
        tree.pack(pady=20)
        
        try:
            cursor.execute("SELECT name, price FROM menu")
            menu_items = cursor.fetchall()
            for item in menu_items:
                tree.insert("", "end", values=(item[0], f"₹{item[1]:.2f}"))
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching menu data: {err}")
    
    # ------------------- Orders Section -------------------
    def show_orders(self):
        self.root.withdraw()
        new_root = tk.Toplevel(self.root)
        app = CafeBillingSystem(new_root)
        new_root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.root.deiconify()
        self.clear_content_frame()
        self.show_welcome()
    
    # ------------------- Customer Details Section -------------------
    def show_customers(self):
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Add Customer Details",
                         font=("Arial", 22, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)

        # Input fields for customer details
        tk.Label(self.content_frame, text="Customer Name:", font=("Arial", 16), bg="white").pack(pady=5)
        self.customer_name_entry = tk.Entry(self.content_frame, font=("Arial", 16))
        self.customer_name_entry.pack(pady=5)

        tk.Label(self.content_frame, text="Phone:", font=("Arial", 16), bg="white").pack(pady=5)
        self.customer_phone_entry = tk.Entry(self.content_frame, font=("Arial", 16))
        self.customer_phone_entry.pack(pady=5)

        tk.Label(self.content_frame, text="Email:", font=("Arial", 16), bg="white").pack(pady=5)
        self.customer_email_entry = tk.Entry(self.content_frame, font=("Arial", 16))
        self.customer_email_entry.pack(pady=5)

        tk.Label(self.content_frame, text="Items Ordered:", font=("Arial", 16), bg="white").pack(pady=5)
        self.customer_items_entry = tk.Entry(self.content_frame, font=("Arial", 16))
        self.customer_items_entry.pack(pady=5)

        save_button = tk.Button(self.content_frame, text="Save Customer", font=("Arial", 16), bg="#3498db", fg="white", command=self.save_customer)
        save_button.pack(pady=20)

    def save_customer(self):
        name = self.customer_name_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        items = self.customer_items_entry.get()

        if not name or not phone or not email or not items:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        try:
            cursor.execute("INSERT INTO customers (name, phone, email, order_details) VALUES (%s, %s, %s, %s)", (name, phone, email, items))
            conn.commit()
            messagebox.showinfo("Success", "Customer details saved successfully!")
            self.customer_name_entry.delete(0, tk.END)
            self.customer_phone_entry.delete(0, tk.END)
            self.customer_email_entry.delete(0, tk.END)
            self.customer_items_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error saving customer data: {err}")

    # ------------------- Update Menu Section -------------------
    def show_update_menu(self):
        self.clear_content_frame()
        title = tk.Label(self.content_frame, text="Update Menu",
                         font=("Arial", 22, "bold"), bg="white", fg="#d77337")
        title.pack(pady=10)

        tk.Label(self.content_frame, text="Item Name:", font=("Arial", 16), bg="white").pack(pady=5)
        self.menu_item_entry = tk.Entry(self.content_frame, font=("Arial", 16))
        self.menu_item_entry.pack(pady=5)

        tk.Label(self.content_frame, text="Price:", font=("Arial", 16), bg="white").pack(pady=5)
        self.menu_price_entry = tk.Entry(self.content_frame, font=("Arial", 16))
        self.menu_price_entry.pack(pady=5)

        add_button = tk.Button(self.content_frame, text="Add Item", font=("Arial", 16), bg="#3498db", fg="white", command=self.add_menu_item)
        add_button.pack(pady=10)

        update_button = tk.Button(self.content_frame, text="Update Item", font=("Arial", 16), bg="#3498db", fg="white", command=self.update_menu_item)
        update_button.pack(pady=10)

    def add_menu_item(self):
        item_name = self.menu_item_entry.get()
        item_price = self.menu_price_entry.get()

        if not item_name or not item_price:
            messagebox.showerror("Input Error", "Both fields are required!")
            return

        try:
            cursor.execute("INSERT INTO menu (name, price) VALUES (%s, %s)", (item_name, float(item_price)))
            conn.commit()
            messagebox.showinfo("Success", "Menu item added successfully!")
            self.menu_item_entry.delete(0, tk.END)
            self.menu_price_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error adding menu item: {err}")

    def update_menu_item(self):
        item_name = self.menu_item_entry.get()
        item_price = self.menu_price_entry.get()

        if not item_name or not item_price:
            messagebox.showerror("Input Error", "Both fields are required!")
            return

        try:
            cursor.execute("UPDATE menu SET price = %s WHERE name = %s", (float(item_price), item_name))
            if cursor.rowcount == 0:
                messagebox.showwarning("Update Warning", "No item found with that name.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Menu item updated successfully!")
            self.menu_item_entry.delete(0, tk.END)
            self.menu_price_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating menu item: {err}")

    # ------------------- Generate Bill Section -------------------
    def generate_bill(self):
        self.show_orders()  # Open the CafeBillingSystem to create a bill
    
    # ------------------- Logout -------------------
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()

# ==================== Main Application ====================
if __name__ == "__main__":  # <-- fixed __name__
    root = tk.Tk()
    app = CafeteriaDashboard(root)
    root.mainloop()
    conn.close()
