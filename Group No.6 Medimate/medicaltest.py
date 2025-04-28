import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import uuid
import pymysql
import json
from tkcalendar import DateEntry

class MedimateBookingSystem:
    def __init__(self, root, user_name, username):
        self.root = root
        self.root.title("MEDIMATE - Simplifying Healthcare Access")
        self.root.geometry("1200x900")
        self.root.configure(bg="white")
        
        self.user_name = user_name
        self.username = username
    
        # Initialize test_vars
        self.test_vars = {}
        self.diagnostic_vars = {}
        self.diagnostic_qty_vars = {}
    

        
        print(f"User: {self.user_name}, Username: {self.username}")
        # Lists of items for each category
        self.medicines_items = [
            "Crocin",
            "Ascorill",
            "Candid-B",
            "CLindac AP",
            "Penicillin",
            "Ketorolac",
            "RabAvert",
            "Gauge",
            "Bandages",
            "Cottons",
            "Neusporin",
            "Paracetamol",
            "Omez",
            "Pain Relievers"
        ]
        
        self.tests_items = [
            "Complete Blood Count (CBC)",
            "Liver Function Test (LFT)",
            "Kidney Function Test (KFT)",
            "Lipid Profile",
            "Thyroid Function Test (TFT)",
            "HbA1c Test",
            "Blood Glucose (Fasting & Random)",
            "Vitamin D & Vitamin B12 Test",
            "Electrolytes Test",
            "HRCT",
            "HIV 1 & 2 Test",
            "Hepatitis B & C Test"
        ]
        
        self.diagnostics_items = [
            "Digital Blood Pressure Monitor",
            "Pulse Oximeter",
            "Portable ECG/EKG Monitor",
            "Holter Monitor",
            "Glucometer",
            "Continuous Glucose Monitoring Device",
            "Spirometer",
            "Peak Flow Meter",
            "Digital Thermometer",
            "Asthma Inhaler",
            "HIV Self-Test Kit",
            "Hepatitis B & C Home Test"
        ]

        self.medicines_prices = {
            "Crocin": 30.00,
            "Ascorill": 209.00,
            "Candid-B": 173.50,
            "CLindac AP": 350.00,
            "Penicillin": 67.70,
            "Ketorolac": 146.75,
            "RabAvert": 80.75,
            "Gauge": 120.00,  
            "Bandages": 50.00,  
            "Cottons": 30.00,  
            "Neusporin": 85.00,  
            "Paracetamol": 25.00,  
            "Omez": 65.00,  
            "Pain Relievers": 45.00 
        }

        self.tests_prices = {
            "Complete Blood Count (CBC)": 350.00,
            "Liver Function Test (LFT)": 500.00,
            "Kidney Function Test (KFT)": 550.00,
            "Lipid Profile": 450.00,
            "Thyroid Function Test (TFT)": 355.00,
            "HbA1c Test": 349.00,
            "Blood Glucose (Fasting & Random)": 150.00,
            "Vitamin D & Vitamin B12 Test": 750.00,
            "Electrolytes Test": 300.00,  
            "HRCT": 3500.00,  
            "HIV 1 & 2 Test": 500.00,  
            "Hepatitis B & C Test": 800.00  
        }

        self.diagnostics_prices = {
            "Digital Blood Pressure Monitor": 1202.00,
            "Pulse Oximeter": 350.00,
            "Portable ECG/EKG Monitor": 8200.00,
            "Holter Monitor": 6000.00,
            "Glucometer": 650.00,
            "Continuous Glucose Monitoring Device": 4500.00,
            "Spirometer": 150.00,
            "Peak Flow Meter": 719.00,
            "Digital Thermometer": 200.00,  
            "Asthma Inhaler": 450.00,  
            "HIV Self-Test Kit": 800.00,  
            "Hepatitis B & C Home Test": 1200.00  
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create header with logo and title
        header_frame = tk.Frame(self.root, bg="#28a745", height=100)
        header_frame.pack(fill=tk.X)
        
        # Add green border around the entire window
        border_frame = tk.Frame(self.root, bg="#28a745", padx=2, pady=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_frame = tk.Frame(border_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header content
        title_label = tk.Label(header_frame, text="Medicines & Diagnostics", 
                             font=("Arial", 24, "bold"), bg="#28a745", fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        logo_text = tk.Label(header_frame, text="MEDIMATE", 
                           font=("Arial", 24, "bold"), bg="#28a745", fg="white")
        logo_text.pack(side=tk.RIGHT, padx=20, pady=10)
        
        slogan_text = tk.Label(header_frame, text="Simplifying Healthcare Access", 
                             font=("Arial", 12), bg="#28a745", fg="white")
        slogan_text.place(relx=0.95, rely=0.7, anchor="e")
        
        # User information display (not editable)
        info_frame = tk.Frame(main_frame, bg="white", pady=20)
        info_frame.pack(fill=tk.X)
        
        # Display username from dashboard
        username_label = tk.Label(info_frame, text=f"User: {self.user_name}", font=("Arial", 14, "bold"), bg="white")
        username_label.pack(pady=5)
        
        # Create selections frame
        selections_frame = tk.Frame(main_frame, bg="white")
        selections_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create three columns
        meds_frame = tk.Frame(selections_frame, bd=1, relief=tk.SOLID)
        meds_frame.grid(row=0, column=0, sticky="nsew")
        
        tests_frame = tk.Frame(selections_frame, bd=1, relief=tk.SOLID)
        tests_frame.grid(row=0, column=1, sticky="nsew")
        
        diag_frame = tk.Frame(selections_frame, bd=1, relief=tk.SOLID)
        diag_frame.grid(row=0, column=2, sticky="nsew")
        
        # Configure the grid to make columns equal width
        selections_frame.columnconfigure(0, weight=1)
        selections_frame.columnconfigure(1, weight=1)
        selections_frame.columnconfigure(2, weight=1)
        selections_frame.rowconfigure(0, weight=1)
        
        # Headers for each column
        meds_header = tk.Label(meds_frame, text="Medicines & Consumables", font=("Arial", 14, "bold"), 
                              relief=tk.SOLID, bd=1, pady=5)
        meds_header.pack(fill=tk.X)
        
        tests_header = tk.Label(tests_frame, text="Tests", font=("Arial", 14, "bold"), 
                               relief=tk.SOLID, bd=1, pady=5)
        tests_header.pack(fill=tk.X)
        
        diag_header = tk.Label(diag_frame, text="Diagnostics", font=("Arial", 14, "bold"), 
                              relief=tk.SOLID, bd=1, pady=5)
        diag_header.pack(fill=tk.X)
        
        # Create scrollable frames for each column
        meds_canvas = tk.Canvas(meds_frame, bg="white")
        meds_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        meds_scrollbar = ttk.Scrollbar(meds_frame, orient="vertical", command=meds_canvas.yview)
        meds_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        meds_canvas.configure(yscrollcommand=meds_scrollbar.set)
        meds_canvas.bind('<Configure>', lambda e: meds_canvas.configure(scrollregion=meds_canvas.bbox("all")))
        
        meds_scrollable_frame = tk.Frame(meds_canvas, bg="white")
        meds_canvas.create_window((0, 0), window=meds_scrollable_frame, anchor="nw")
        
        # Repeat for tests
        tests_canvas = tk.Canvas(tests_frame, bg="white")
        tests_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tests_scrollbar = ttk.Scrollbar(tests_frame, orient="vertical", command=tests_canvas.yview)
        tests_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tests_canvas.configure(yscrollcommand=tests_scrollbar.set)
        tests_canvas.bind('<Configure>', lambda e: tests_canvas.configure(scrollregion=tests_canvas.bbox("all")))
        
        tests_scrollable_frame = tk.Frame(tests_canvas, bg="white")
        tests_canvas.create_window((0, 0), window=tests_scrollable_frame, anchor="nw")
        
        # Repeat for diagnostics
        diag_canvas = tk.Canvas(diag_frame, bg="white")
        diag_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        diag_scrollbar = ttk.Scrollbar(diag_frame, orient="vertical", command=diag_canvas.yview)
        diag_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        diag_canvas.configure(yscrollcommand=diag_scrollbar.set)
        diag_canvas.bind('<Configure>', lambda e: diag_canvas.configure(scrollregion=diag_canvas.bbox("all")))
        
        diag_scrollable_frame = tk.Frame(diag_canvas, bg="white")
        diag_canvas.create_window((0, 0), window=diag_scrollable_frame, anchor="nw")
        
        # Add a delivery options frame
        delivery_frame = tk.LabelFrame(main_frame, text="Delivery Options", font=("Arial", 14, "bold"), bg="white", pady=10)
        delivery_frame.pack(fill=tk.X, padx=20, pady=10)

        # Date selection
        date_frame = tk.Frame(delivery_frame, bg="white")
        date_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(date_frame, text="Delivery Date:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # DateEntry widget for selecting delivery date
        self.delivery_date = DateEntry(date_frame, width=12, background='#28a745', foreground='white', 
                                    borderwidth=2, date_pattern='yyyy-mm-dd',
                                    mindate=datetime.datetime.now().date())
        self.delivery_date.grid(row=0, column=1, padx=5, pady=5)

        # Time slot selection
        time_frame = tk.Frame(delivery_frame, bg="white")
        time_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(time_frame, text="Delivery Time Slot:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Define time slots
        self.time_slots = [
            "09:00 AM - 11:00 AM",
            "11:00 AM - 01:00 PM",
            "01:00 PM - 03:00 PM",
            "03:00 PM - 05:00 PM",
            "05:00 PM - 07:00 PM"
        ]

        self.selected_time_slot = tk.StringVar(value=self.time_slots[0])
        time_slot_dropdown = ttk.Combobox(time_frame, textvariable=self.selected_time_slot, values=self.time_slots, state="readonly", width=20)
        time_slot_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Add special instructions for delivery
        instruction_frame = tk.Frame(delivery_frame, bg="white")
        instruction_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(instruction_frame, text="Special Instructions:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.delivery_instructions = tk.Text(instruction_frame, height=3, width=40)
        self.delivery_instructions.grid(row=0, column=1, padx=5, pady=5)

        #the column headers for medicines
        tk.Label(meds_scrollable_frame, text="Item", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(meds_scrollable_frame, text="Price (₹)", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Label(meds_scrollable_frame, text="Select", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        tk.Label(meds_scrollable_frame, text="Quantity", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=3, sticky="w", padx=10, pady=5)

        #the column headers for tests
        tk.Label(tests_scrollable_frame, text="Test", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(tests_scrollable_frame, text="Price (₹)", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Label(tests_scrollable_frame, text="Select", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=2, sticky="w", padx=10, pady=5)

        #the column headers for diagnostics
        tk.Label(diag_scrollable_frame, text="Item", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(diag_scrollable_frame, text="Price (₹)", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Label(diag_scrollable_frame, text="Select", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        tk.Label(diag_scrollable_frame, text="Quantity", font=("Arial", 12, "bold"), bg="white").grid(row=0, column=3, sticky="w", padx=10, pady=5)
        
        # Create checkboxes and quantity spinboxes for medicines
        self.medicine_vars = {}
        self.medicine_qty_vars = {}
        
        # Update medicines listing
        for i, item in enumerate(self.medicines_items):
            var = tk.BooleanVar()
            qty_var = tk.StringVar(value="1")
            self.medicine_vars[item] = var
            self.medicine_qty_vars[item] = qty_var
            
            price = self.medicines_prices.get(item, 0)
            
            tk.Label(meds_scrollable_frame, text=item, bg="white").grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            tk.Label(meds_scrollable_frame, text=f"{price:.2f}", bg="white").grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
            cb = tk.Checkbutton(meds_scrollable_frame, variable=var, bg="white")
            cb.grid(row=i+1, column=2, sticky="w", padx=10, pady=5)
            
            spinbox = ttk.Spinbox(meds_scrollable_frame, from_=1, to=10, width=5, textvariable=qty_var, state="readonly")
            spinbox.grid(row=i+1, column=3, sticky="w", padx=10, pady=5)

        # Update tests listing
        for i, item in enumerate(self.tests_items):
            var = tk.BooleanVar()
            self.test_vars[item] = var
            
            price = self.tests_prices.get(item, 0)
            
            tk.Label(tests_scrollable_frame, text=item, bg="white").grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            tk.Label(tests_scrollable_frame, text=f"{price:.2f}", bg="white").grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
            cb = tk.Checkbutton(tests_scrollable_frame, variable=var, bg="white")
            cb.grid(row=i+1, column=2, sticky="w", padx=10, pady=5)

        # Update diagnostics listing  
        for i, item in enumerate(self.diagnostics_items):
            var = tk.BooleanVar()
            qty_var = tk.StringVar(value="1")
            self.diagnostic_vars[item] = var
            self.diagnostic_qty_vars[item] = qty_var
            
            price = self.diagnostics_prices.get(item, 0)
            
            tk.Label(diag_scrollable_frame, text=item, bg="white").grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
            tk.Label(diag_scrollable_frame, text=f"{price:.2f}", bg="white").grid(row=i+1, column=1, sticky="w", padx=10, pady=5)
            cb = tk.Checkbutton(diag_scrollable_frame, variable=var, bg="white")
            cb.grid(row=i+1, column=2, sticky="w", padx=10, pady=5)
            
            spinbox = ttk.Spinbox(diag_scrollable_frame, from_=1, to=10, width=5, textvariable=qty_var, state="readonly")
            spinbox.grid(row=i+1, column=3, sticky="w", padx=10, pady=5)
        
        # Book button at the bottom
        button_frame = tk.Frame(main_frame, bg="white", pady=10)
        button_frame.pack()

        # Create a sub-frame to hold the buttons side by side
        buttons_container = tk.Frame(button_frame, bg="white")
        buttons_container.pack()

        # Back to Dashboard button
        back_button = tk.Button(buttons_container, text="Back to Dashboard", 
                            bg="white", fg="#007bff", font=("Arial", 14, "bold"),
                            width=20, relief=tk.SOLID, bd=1,
                            command=self.back_to_dashboard)
        back_button.grid(row=0, column=0, padx=10)

        # Book button
        book_button = tk.Button(buttons_container, text="Book", command=self.book_appointment, 
                            bg="white", fg="#28a745", font=("Arial", 14, "bold"),
                            width=20, relief=tk.SOLID, bd=1)
        book_button.grid(row=0, column=1, padx=10)
    
    def db_connection(self):
        """Establish database connection"""
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="Drishti2005@",
                database="medimate"
            )
            return connection
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
            return None
    
    def book_appointment(self):
        # Get selected items with quantities
        selected_medicines = []
        total_medicine_price = 0
        for item, var in self.medicine_vars.items():
            if var.get():
                quantity = int(self.medicine_qty_vars[item].get())
                price = self.medicines_prices.get(item, 0)
                item_total = price * quantity
                total_medicine_price += item_total
                selected_medicines.append({
                    "item": item, 
                    "quantity": quantity,
                    "price": price,
                    "total": item_total
                })
        
        selected_tests = []
        total_test_price = 0
        for item, var in self.test_vars.items():
            if var.get():
                price = self.tests_prices.get(item, 0)
                total_test_price += price
                selected_tests.append({
                    "item": item,
                    "price": price
                })
        
        selected_diagnostics = []
        total_diagnostic_price = 0
        for item, var in self.diagnostic_vars.items():
            if var.get():
                quantity = int(self.diagnostic_qty_vars[item].get())
                price = self.diagnostics_prices.get(item, 0)
                item_total = price * quantity
                total_diagnostic_price += item_total
                selected_diagnostics.append({
                    "item": item, 
                    "quantity": quantity,
                    "price": price,
                    "total": item_total
                })
        
        total_price = total_medicine_price + total_test_price + total_diagnostic_price

        try:
            delivery_date = self.delivery_date.get_date()  # This gives you a Python date object
            delivery_time_slot = self.selected_time_slot.get()
            delivery_instructions = self.delivery_instructions.get("1.0", tk.END).strip()
            
            # Validate delivery date (should be today or future)
            if delivery_date < datetime.datetime.now().date():
                messagebox.showerror("Error", "Please select a valid delivery date (today or future)")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Invalid delivery information: {e}")
            return

        # Create booking data
        booking_id = str(uuid.uuid1())
        booking_date = datetime.datetime.now()
        
        # Create the JSON data for storage
        items_data = {
            "medicines": selected_medicines,
            "tests": selected_tests,
            "diagnostics": selected_diagnostics,
            "total_price": total_price
        }
        
        # Convert to JSON string for database storage
        items_json = json.dumps(items_data)
        
        # Save to database
        connection = self.db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO medical_bookings 
                (booking_id, p_username, user_name, booking_date, items_data, 
                delivery_date, delivery_time_slot, delivery_instructions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    booking_id, 
                    self.username, 
                    self.user_name, 
                    booking_date, 
                    items_json,
                    delivery_date,
                    delivery_time_slot,
                    delivery_instructions
                ))
                connection.commit()
                cursor.close()
                connection.close()
                
                # Show booking details and clear form
                self.show_booking_details(booking_id, selected_medicines, selected_tests, selected_diagnostics,
                                        delivery_date, delivery_time_slot, delivery_instructions)
                self.clear_form()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to save booking: {e}")
        else:
            # No database connection, just show the details
            self.show_booking_details(booking_id, selected_medicines, selected_tests, selected_diagnostics,
                                    delivery_date, delivery_time_slot, delivery_instructions)
        
        if not (selected_medicines or selected_tests or selected_diagnostics):
            messagebox.showerror("Error", "Please select at least one item to book")
            return
        
        # Get delivery information
        try:
            delivery_date = self.delivery_date.get_date()
            delivery_time_slot = self.selected_time_slot.get()
            delivery_instructions = self.delivery_instructions.get("1.0", tk.END).strip()
            
            # Validate delivery date (should be today or future)
            if delivery_date < datetime.datetime.now().date():
                messagebox.showerror("Error", "Please select a valid delivery date (today or future)")
                return
                
        except Exception as e:
            messagebox.showerror("Error", f"Invalid delivery information: {e}")
            return
        
        # Create booking data
        booking_id = str(uuid.uuid1())
        booking_date = datetime.datetime.now()
        
        # Create the JSON data for storage
        items_data = {
            "medicines": selected_medicines,
            "tests": selected_tests,
            "diagnostics": selected_diagnostics,
            "total_price": total_price
        }
        
        # Convert to JSON string for database storage
        items_json = json.dumps(items_data)
    
    def show_booking_details(self, booking_id, selected_medicines, selected_tests, selected_diagnostics, 
                     delivery_date, delivery_time_slot, delivery_instructions):
        """Display booking details in a message box"""
        details = f"Booking ID: {booking_id}\n"
        details += f"Name: {self.user_name}\n\n"
        
        # Initialize total price
        total_price = 0
        
        if selected_medicines:
            details += "MEDICINES & CONSUMABLES:\n"
            for med in selected_medicines:
                med_total = med['total']
                total_price += med_total
                details += f"- {med['item']} (Qty: {med['quantity']}) - ₹{med['price']:.2f} x {med['quantity']} = ₹{med_total:.2f}\n"
            details += "\n"
            
        if selected_tests:
            details += "TESTS:\n"
            for test in selected_tests:
                test_price = test['price']
                total_price += test_price
                details += f"- {test['item']} - ₹{test_price:.2f}\n"
            details += "\n"
            
        if selected_diagnostics:
            details += "DIAGNOSTICS:\n"
            for diag in selected_diagnostics:
                diag_total = diag['total']
                total_price += diag_total
                details += f"- {diag['item']} (Qty: {diag['quantity']}) - ₹{diag['price']:.2f} x {diag['quantity']} = ₹{diag_total:.2f}\n"
            details += "\n"
        
        # Add total price
        details += f"TOTAL AMOUNT: ₹{total_price:.2f}\n\n"
        
        # Add delivery information
        details += "DELIVERY DETAILS:\n"
        details += f"Date: {delivery_date.strftime('%Y-%m-%d')}\n"
        details += f"Time Slot: {delivery_time_slot}\n"
        if delivery_instructions:
            details += f"Special Instructions: {delivery_instructions}\n"
        
        # Add payment method
        details += "\nPayment Method: Cash on Delivery\n"
            
        messagebox.showinfo("Booking Successful", 
                        f"Your booking has been confirmed!\n\nDETAILS:\n{details}")
        
    def clear_form(self):
        # Clear checkboxes and reset quantities
        for var in self.medicine_vars.values():
            var.set(False)
        for qty_var in self.medicine_qty_vars.values():
            qty_var.set("1")
            
        for var in self.test_vars.values():
            var.set(False)
            
        for var in self.diagnostic_vars.values():
            var.set(False)
        for qty_var in self.diagnostic_qty_vars.values():
            qty_var.set("1")
        today = datetime.datetime.now().date()
        self.delivery_date.set_date(today)
        self.selected_time_slot.set(self.time_slots[0])
        self.delivery_instructions.delete("1.0", tk.END)

    def back_to_dashboard(self):
        self.root.destroy()  # Close the current window
        from userdashboard import NavigationApp
        new_root = tk.Tk()
        app = NavigationApp(new_root, self.user_name, self.username)