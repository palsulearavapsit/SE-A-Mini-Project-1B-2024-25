from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import qrcode
import time
import os
from datetime import datetime

class InMemoryStorage:
    def __init__(self):
        self.bills = []
        self.qr_codes = []
    
    def save_bill(self, bill_data):
        bill_data['id'] = len(self.bills) + 1
        bill_data['timestamp'] = datetime.now()
        self.bills.append(bill_data)
        return bill_data['id']
    
    def save_qr(self, qr_data):
        self.qr_codes.append(qr_data)

# Global storage instance
storage = InMemoryStorage()

class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("890x580+0+0")
        self.root.title("SIMPLE CAFE BILLING SYSTEM")
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        
        # Create main frames
        Tops = Frame(self.root, bg="white", width=1600, height=50, relief=SUNKEN)
        Tops.pack(side=TOP)
        
        f1 = Frame(self.root, width=900, height=700, relief=SUNKEN)
        f1.pack(side=LEFT)
        
        # Initialize variables
        self.init_variables()
        
        # Setup header
        self.setup_header(Tops)
        
        # Setup billing form
        self.setup_billing_form(f1)
        
        # Setup calculation area
        self.setup_calculation_area(f1)
        
        # Setup buttons
        self.setup_buttons(f1)

    def init_variables(self):
        # Billing variables
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
        
        # Menu prices
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
        # Order number
        Label(frame, font=('aria', 16, 'bold'), text="Order No.", 
              fg="brown", bd=20, anchor='w').grid(row=0, column=0)
        Entry(frame, font=('ariel', 16, 'bold'), textvariable=self.variables['order_no'],
              bd=6, insertwidth=6, bg="yellow", justify='right').grid(row=0, column=1)
        
        # Menu items
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
            
            # Update display
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
            'items': {
                item: float(self.variables[item].get() or 0)
                for item in self.prices.keys()
            },
            'total': float(self.variables['total'].get().replace("Rs. ", ""))
        }
        
        bill_id = storage.save_bill(bill_data)
        self.generate_qr(bill_id)
        messagebox.showinfo("Success", "Bill saved successfully!")

    def generate_qr(self, bill_id):
        # Create QR code data
        bill = storage.bills[bill_id - 1]
        qr_data = f"""
        Order No: {bill['order_no']}
        Total: Rs. {bill['total']:.2f}
        Date: {bill['timestamp']}
        """
        
        # Generate and save QR code
        qr = qrcode.make(qr_data)
        if not os.path.exists('qr_storage'):
            os.makedirs('qr_storage')
        qr_path = f"qr_storage/bill_{bill_id}.png"
        qr.save(qr_path)
        
        # Show QR code
        self.show_qr(qr_path)

    def show_qr(self, qr_path):
        qr_window = Toplevel(self.root)
        qr_window.title("Bill QR Code")
        qr_window.geometry("300x350")
        
        img = Image.open(qr_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)
        qr_img = ImageTk.PhotoImage(img)
        
        Label(qr_window, image=qr_img).pack(pady=20)
        qr_window.qr_img = qr_img  # Keep reference
        
        Button(qr_window, text="Close", command=qr_window.destroy).pack()

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
