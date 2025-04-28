from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import qrcode
import time
import os
import mysql.connector
from datetime import datetime

class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("890x580+0+0")
        self.root.title("SIMPLE CAFE BILLING SYSTEM")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="Cafe_billing"
        )
        self.cursor = self.db.cursor()

        self.create_table()

        Tops = Frame(self.root, bg="white", width=1600, height=50, relief=SUNKEN)
        Tops.pack(side=TOP)

        f1 = Frame(self.root, width=900, height=700, relief=SUNKEN)
        f1.pack(side=LEFT)

        self.init_variables()
        self.setup_header(Tops)
        self.setup_billing_form(f1)
        self.setup_calculation_area(f1)
        self.setup_buttons(f1)

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_no VARCHAR(50) NOT NULL,
            fries DECIMAL(10, 2) DEFAULT 0,
            lunch DECIMAL(10, 2) DEFAULT 0,
            burger DECIMAL(10, 2) DEFAULT 0,
            pizza DECIMAL(10, 2) DEFAULT 0,
            cheese_burger DECIMAL(10, 2) DEFAULT 0,
            drinks DECIMAL(10, 2) DEFAULT 0,
            cost DECIMAL(10, 2) NOT NULL,
            service_charge DECIMAL(10, 2) NOT NULL,
            tax DECIMAL(10, 2) NOT NULL,
            subtotal DECIMAL(10, 2) NOT NULL,
            total DECIMAL(10, 2) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(create_table_query)
        self.db.commit()

    def init_variables(self):
        self.variables = {
            'order_no': StringVar(),
            'fries': StringVar(),
            'lunch': StringVar(),
            'burger': StringVar(),
            'pizza': StringVar(),
            'cheese_burger': StringVar(),
            'drinks': StringVar(),
            'cost': StringVar(),
            'service_charge': StringVar(),
            'tax': StringVar(),
            'subtotal': StringVar(),
            'total': StringVar()
        }

        self.prices = {
            'fries': 25,
            'lunch': 40,
            'burger': 35,
            'pizza': 50,
            'cheese_burger': 30,
            'drinks': 35
        }

    def setup_header(self, frame):
        localtime = time.asctime(time.localtime(time.time()))
        Label(frame, font=('aria', 30, 'bold'), text="SIMPLE CAFE BILLING",
              fg="Black", bd=10, anchor='w').grid(row=0, column=0)
        Label(frame, font=('aria', 20), text=localtime,
              fg="steel blue", anchor='w').grid(row=1, column=0)

    def setup_billing_form(self, frame):
        Label(frame, font=('aria', 16, 'bold'), text="Order No.",
              fg="brown", bd=20, anchor='w').grid(row=0, column=0)
        Entry(frame, font=('ariel', 16, 'bold'), textvariable=self.variables['order_no'],
              bd=6, insertwidth=6, bg="yellow", justify='right').grid(row=0, column=1)

        items = [
            ('Drinks', 'drinks', 1),
            ('French Fries', 'fries', 2),
            ('Lunch', 'lunch', 3),
            ('Burger', 'burger', 4),
            ('Pizza', 'pizza', 5),
            ('Cheese burger', 'cheese_burger', 6)
        ]

        for label, var_name, row in items:
            Label(frame, font=('aria', 16, 'bold'), text=label,
                  fg="blue", bd=10, anchor='w').grid(row=row, column=0)
            Entry(frame, font=('ariel', 16, 'bold'), textvariable=self.variables[var_name],
                  bd=6, insertwidth=4, bg="green", justify='right').grid(row=row, column=1)

    def setup_calculation_area(self, frame):
        calcs = [
            ('Cost', 'cost', 2),
            ('Service Charge', 'service_charge', 3),
            ('Tax', 'tax', 4),
            ('Subtotal', 'subtotal', 5),
            ('Total', 'total', 6)
        ]

        for label, var_name, row in calcs:
            Label(frame, font=('aria', 16, 'bold'), text=label,
                  fg="black", bd=10, anchor='w').grid(row=row, column=2)
            Entry(frame, font=('aria', 16, 'bold'), textvariable=self.variables[var_name],
                  bd=6, insertwidth=4, bg="white", justify='right').grid(row=row, column=3)

    def calculate_total(self):
        try:
            total = 0
            for item, price in self.prices.items():
                qty = float(self.variables[item].get() or 0)
                total += qty * price

            tax = total * 0.33
            service = total * 0.10
            final_total = total + tax + service

            self.variables['cost'].set(f"Rs. {total:.2f}")
            self.variables['service_charge'].set(f"Rs. {service:.2f}")
            self.variables['tax'].set(f"Rs. {tax:.2f}")
            self.variables['total'].set(f"Rs. {final_total:.2f}")
            self.variables['subtotal'].set(f"Rs. {final_total:.2f}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers")

    def save_bill(self):
        bill_data = {
            'order_no': self.variables['order_no'].get(),
            'fries': float(self.variables['fries'].get() or 0),
            'lunch': float(self.variables['lunch'].get() or 0),
            'burger': float(self.variables['burger'].get() or 0),
            'pizza': float(self.variables['pizza'].get() or 0),
            'cheese_burger': float(self.variables['cheese_burger'].get() or 0),
            'drinks': float(self.variables['drinks'].get() or 0),
            'cost': float(self.variables['cost'].get().replace("Rs. ", "")),
            'service_charge': float(self.variables['service_charge'].get().replace("Rs. ", "")),
            'tax': float(self.variables['tax'].get().replace("Rs. ", "")),
            'subtotal': float(self.variables['subtotal'].get().replace("Rs. ", "")),
            'total': float(self.variables['total'].get().replace("Rs. ", "")),
        }

        insert_query = """
        INSERT INTO Bills (order_no, fries, lunch, burger, pizza, cheese_burger, drinks, cost, service_charge, tax, subtotal, total)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_query, (
            bill_data['order_no'],
            bill_data['fries'],
            bill_data['lunch'],
            bill_data['burger'],
            bill_data['pizza'],
            bill_data['cheese_burger'],
            bill_data['drinks'],
            bill_data['cost'],
            bill_data['service_charge'],
            bill_data['tax'],
            bill_data['subtotal'],
            bill_data['total']
        ))
        self.db.commit()

        bill_id = self.cursor.lastrowid
        self.generate_qr(bill_id)
        self.generate_receipt(bill_id)
        messagebox.showinfo("Success", "Bill saved successfully!")

    def generate_qr(self, bill_id):
        qr_data = f"Bill ID: {bill_id}\nTotal: Rs. {self.variables['total'].get()}\n"
        qr = qrcode.make(qr_data)

        if not os.path.exists('qr_storage'):
            os.makedirs('qr_storage')
        qr_path = f"qr_storage/bill_{bill_id}.png"
        qr.save(qr_path)

        self.show_qr(qr_path)

    def show_qr(self, qr_path):
        qr_window = Toplevel(self.root)
        qr_window.title("Bill QR Code")
        qr_window.geometry("300x350")

        img = Image.open(qr_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        qr_img = ImageTk.PhotoImage(img)

        Label(qr_window, image=qr_img).pack(pady=20)
        qr_window.qr_img = qr_img

        Button(qr_window, text="Close", command=qr_window.destroy).pack()

    def generate_receipt(self, bill_id):
        receipt_window = Toplevel(self.root)
        receipt_window.title("Bill Receipt")
        receipt_window.geometry("400x500")

        Label(receipt_window, text="Cafe Receipt", font=('aria', 20, 'bold')).pack(pady=10)
        Label(receipt_window, text=f"Bill ID: {bill_id}", font=('aria', 12)).pack()
        Label(receipt_window, text=f"Order No: {self.variables['order_no'].get()}", font=('aria', 12)).pack()
        Label(receipt_window, text="-------------------------------").pack()

        for item in ['drinks', 'fries', 'lunch', 'burger', 'pizza', 'cheese_burger']:
            qty = self.variables[item].get()
            if qty and float(qty) > 0:
                Label(receipt_window, text=f"{item.replace('_',' ').title()}: {qty} x Rs.{self.prices[item]} = Rs.{float(qty)*self.prices[item]:.2f}",
                      font=('aria', 12)).pack()

        Label(receipt_window, text="-------------------------------").pack()
        Label(receipt_window, text=f"Cost: {self.variables['cost'].get()}", font=('aria', 12)).pack()
        Label(receipt_window, text=f"Service Charge: {self.variables['service_charge'].get()}", font=('aria', 12)).pack()
        Label(receipt_window, text=f"Tax: {self.variables['tax'].get()}", font=('aria', 12)).pack()
        Label(receipt_window, text=f"Subtotal: {self.variables['subtotal'].get()}", font=('aria', 12)).pack()
        Label(receipt_window, text=f"Total: {self.variables['total'].get()}", font=('aria', 14, 'bold')).pack()

        Label(receipt_window, text="-------------------------------").pack()
        Label(receipt_window, text="Thank you for visiting!", font=('aria', 12)).pack(pady=10)
        Button(receipt_window, text="Close", command=receipt_window.destroy).pack(pady=10)

    def reset_form(self):
        for var in self.variables.values():
            var.set("")

    def show_menu(self):
        menu_window = Toplevel(self.root)
        menu_window.title("Menu Prices")
        menu_window.geometry("300x400")

        Label(menu_window, text="Menu Prices", font=('aria', 20, 'bold')).pack(pady=10)

        for item, price in self.prices.items():
            Label(menu_window,
                  text=f"{item.replace('_', ' ').title()}: Rs. {price}",
                  font=('aria', 14)).pack(pady=5)

        Button(menu_window, text="Close", command=menu_window.destroy).pack(pady=20)

    def setup_buttons(self, frame):
        buttons = [
            ('TOTAL', 'red', self.calculate_total),
            ('SAVE', 'green', self.save_bill),
            ('RESET', 'gray', self.reset_form),
            ('MENU', 'blue', self.show_menu)
        ]
        for i, (text, color, command) in enumerate(buttons):
            Button(frame, text=text, bg=color, fg="white",
                   font=('aria', 16, 'bold'), command=command,
                   padx=5, pady=5).grid(row=8, column=i, padx=5)

if __name__ == "__main__":
    root = Tk()
    app = CafeBillingSystem(root)
    root.mainloop()
