import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# ---------- MySQL Connection ----------
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="12345",
        database="restaurant_db"
    )

# ---------- User Registration ----------
def register_user(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False

# ---------- Login Check ----------
def check_login(username, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not connect to database.\n{e}")
        return False

# ---------- Billing Window ----------
def open_billing_window():
    billing = tk.Tk()
    billing.title("Restaurant Billing System")
    billing.attributes('-fullscreen', True)
    billing.configure(bg="#f7f9fc")

    FONT_TITLE = ("Helvetica", 30, "bold")
    FONT_LABEL = ("Helvetica", 16)
    FONT_BILL = ("Courier New", 12)

    menu_prices = {"Burger": 100, "Pizza": 200, "Fries": 70, "Coke": 40}
    qty_vars = {}

    tk.Label(billing, text="\U0001F37D\uFE0F Restaurant Billing System", font=FONT_TITLE,
             bg="#1976d2", fg="white", pady=20).pack(fill=tk.X)

    customer_frame = tk.Frame(billing, bg="#f7f9fc")
    customer_frame.pack(pady=30)
    tk.Label(customer_frame, text="Customer Name:", font=FONT_LABEL, bg="#f7f9fc").grid(row=0, column=0, padx=10)
    customer_name = tk.Entry(customer_frame, font=FONT_LABEL, width=30, relief="groove", bd=3)
    customer_name.grid(row=0, column=1, padx=10)

    items_frame = tk.LabelFrame(billing, text="Select Items", font=("Helvetica", 18, "bold"), padx=20, pady=20,
                                bg="#ffffff", fg="#333", bd=2)
    items_frame.pack(pady=20)

    for i, (item, price) in enumerate(menu_prices.items()):
        tk.Label(items_frame, text=f"{item} (\u20B9{price})", font=FONT_LABEL, bg="#ffffff").grid(row=i, column=0, padx=10, pady=8, sticky="e")
        qty = tk.IntVar(value=0)
        qty_vars[item] = qty
        entry = tk.Entry(items_frame, textvariable=qty, width=5, font=FONT_LABEL, relief="ridge", bd=2, justify='center')
        entry.grid(row=i, column=1, padx=5)

    bill_text = tk.Text(billing, height=15, width=80, font=FONT_BILL, bd=3, relief="solid", bg="#f0f0f0")
    bill_text.pack(pady=20)

    def store_in_db(name, items_str, total, bill_string):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO orders (customer_name, items, total, bill_text) VALUES (%s, %s, %s, %s)",
                           (name, items_str, total, bill_string))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "\u2705 Bill saved successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save to database.\n{e}")

    def generate_bill():
        name = customer_name.get().strip()
        if name == "":
            messagebox.showwarning("Missing Info", "Please enter the customer's name.")
            return

        bill_text.delete("1.0", tk.END)
        total = 0
        items_str = ""

        bill_lines = []
        bill_lines.append("** RESTAURANT BILL **")
        bill_lines.append(f"Customer: {name}")
        bill_lines.append(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        bill_lines.append("------------------------------")
        bill_lines.append("Item\tQty\tPrice")
        bill_lines.append("------------------------------")

        for item, price in menu_prices.items():
            qty = qty_vars[item].get()
            if qty > 0:
                item_total = price * qty
                bill_lines.append(f"{item}\t{qty}\t\u20B9{item_total}")
                items_str += f"{item}({qty}), "
                total += item_total

        if total == 0:
            messagebox.showinfo("No Items", "Please select at least one item.")
            return

        tax = round(total * 0.05, 2)
        grand_total = total + tax

        bill_lines.append("------------------------------")
        bill_lines.append(f"Subtotal:\t\t\u20B9{total}")
        bill_lines.append(f"Tax (5%):\t\t\u20B9{tax}")
        bill_lines.append(f"Total:\t\t\u20B9{grand_total}")
        bill_lines.append("------------------------------")

        final_bill = "\n".join(bill_lines)
        bill_text.insert(tk.END, final_bill)

        store_in_db(name, items_str.strip(", "), grand_total, final_bill)

    btn_frame = tk.Frame(billing, bg="#f7f9fc")
    btn_frame.pack(pady=10)

    btn_style = {"font": FONT_LABEL, "padx": 30, "pady": 12, "relief": "raised", "bd": 3, "width": 20}

    tk.Button(btn_frame, text="Generate Bill", command=generate_bill,
              bg="#43a047", fg="white", **btn_style).grid(row=0, column=0, padx=20, pady=10)

    tk.Button(btn_frame, text="Logout", command=lambda: [billing.destroy(), login_window()],
              bg="#e53935", fg="white", **btn_style).grid(row=0, column=1, padx=20, pady=10)

    billing.mainloop()

# ---------- Registration Window ----------
def registration_window():
    reg = tk.Toplevel()
    reg.title("Register")
    reg.attributes('-fullscreen', True)
    reg.configure(bg="#e3f2fd")

    tk.Label(reg, text="\U0001F510 Register", font=("Helvetica", 28, "bold"), bg="#1e88e5", fg="white", pady=20).pack(fill=tk.X)

    tk.Label(reg, text="Username:", font=("Helvetica", 16), bg="#e3f2fd").pack(pady=10)
    username_entry = tk.Entry(reg, font=("Helvetica", 16), width=30, relief="groove", bd=3)
    username_entry.pack(pady=5)

    tk.Label(reg, text="Password:", font=("Helvetica", 16), bg="#e3f2fd").pack(pady=10)
    password_entry = tk.Entry(reg, show="*", font=("Helvetica", 16), width=30, relief="groove", bd=3)
    password_entry.pack(pady=5)

    def register():
        user = username_entry.get()
        pwd = password_entry.get()
        if user == "" or pwd == "":
            messagebox.showwarning("Missing Fields", "Please fill all fields.")
        elif register_user(user, pwd):
            messagebox.showinfo("Success", "\u2705 Registered Successfully!")
            reg.destroy()

    tk.Button(reg, text="Register", font=("Helvetica", 16), command=register,
              bg="#4CAF50", fg="white", padx=20, pady=10, relief="raised").pack(pady=20)
    tk.Button(reg, text="Back to Login", font=("Helvetica", 14), command=reg.destroy,
              bg="#e53935", fg="white", width=20).pack(pady=10)

# ---------- Login Window ----------
def login_window():
    login = tk.Tk()
    login.title("Login")
    login.attributes('-fullscreen', True)
    login.configure(bg="#f0f0f0")

    tk.Label(login, text="\U0001F510 Login", font=("Helvetica", 28, "bold"), bg="#283593", fg="white", pady=20).pack(fill=tk.X, pady=10)

    tk.Label(login, text="Username:", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)
    username_entry = tk.Entry(login, font=("Helvetica", 16), width=30, relief="groove", bd=3)
    username_entry.pack(pady=5)

    tk.Label(login, text="Password:", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=10)
    password_entry = tk.Entry(login, show="*", font=("Helvetica", 16), width=30, relief="groove", bd=3)
    password_entry.pack(pady=5)

    def attempt_login():
        user = username_entry.get()
        pwd = password_entry.get()
        if check_login(user, pwd):
            login.destroy()
            open_billing_window()
        else:
            messagebox.showerror("Login Failed", "\u274C Invalid username or password.")

    tk.Button(login, text="Login", font=("Helvetica", 16), command=attempt_login,
              bg="#4CAF50", fg="white", padx=20, pady=10, relief="raised", width=20).pack(pady=20)
    tk.Button(login, text="New User? Register", font=("Helvetica", 14), command=registration_window,
              bg="#1e88e5", fg="white", width=20).pack(pady=10)

    tk.Button(login, text="Exit", font=("Helvetica", 14), command=login.destroy,
              bg="#e53935", fg="white", width=20).pack(pady=10)

    login.mainloop() 

# ---------- Main Execution ----------
if __name__ == "__main__":
    login_window()