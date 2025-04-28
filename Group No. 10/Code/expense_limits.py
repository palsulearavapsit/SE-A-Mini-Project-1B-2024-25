import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartSpend")
        self.root.geometry("1200x700")
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'M@nas1601',
            'database': 'expense_tracker'
        }
        self.current_user = None
        self.create_database()
        self.show_login_page()

    def create_database(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense_limits (
                user_id INT PRIMARY KEY,
                month_year VARCHAR(7) NOT NULL,
                limit_amount DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def set_expense_limit(self):
        limit_window = tk.Toplevel(self.root)
        limit_window.title("Set Monthly Limit")
        limit_window.geometry("300x200")
        
        tk.Label(limit_window, text="Set Monthly Expense Limit:").pack(pady=10)
        self.limit_entry = tk.Entry(limit_window)
        self.limit_entry.pack(pady=5)
        
        tk.Button(limit_window, text="Save Limit", command=self.save_expense_limit).pack(pady=10)
    
    def save_expense_limit(self):
        limit = self.limit_entry.get()
        if not limit.isdigit():
            messagebox.showerror("Error", "Enter a valid amount")
            return
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            month_year = datetime.now().strftime("%Y-%m")
            cursor.execute("REPLACE INTO expense_limits (user_id, month_year, limit_amount) VALUES (%s, %s, %s)",
                           (self.current_user['id'], month_year, limit))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Expense limit set successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def check_expense_limit(self, amount):
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            month_year = datetime.now().strftime("%Y-%m")
            cursor.execute("SELECT limit_amount FROM expense_limits WHERE user_id = %s AND month_year = %s", 
                           (self.current_user['id'], month_year))
            result = cursor.fetchone()
            if result:
                limit = result[0]
                cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = %s AND type = 'Expense' AND DATE_FORMAT(date, '%Y-%m') = %s", 
                               (self.current_user['id'], month_year))
                total_expense = cursor.fetchone()[0]
                if total_expense + float(amount) > limit:
                    messagebox.showwarning("Limit Exceeded", "You have exceeded your monthly expense limit!")
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def add_expense(self, amount):
        self.check_expense_limit(amount)
        # Code to add expense to database
    
# Create main application window
root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()
