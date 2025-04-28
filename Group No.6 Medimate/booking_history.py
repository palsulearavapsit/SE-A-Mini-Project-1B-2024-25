import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import json
from datetime import datetime

class BookingHistory:
    def __init__(self, root, user_name, username):
        self.root = root
        self.root.title("MEDIMATE - Booking History")
        self.root.geometry("1200x800")
        self.root.configure(bg="white")
        
        self.user_name = user_name
        self.username = username
        
        self.create_widgets()
        self.load_bookings()
    
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
        title_label = tk.Label(header_frame, text="Medical Bookings History", 
                             font=("Arial", 24, "bold"), bg="#28a745", fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        logo_text = tk.Label(header_frame, text="MEDIMATE", 
                           font=("Arial", 24, "bold"), bg="#28a745", fg="white")
        logo_text.pack(side=tk.RIGHT, padx=20, pady=10)
        
        slogan_text = tk.Label(header_frame, text="Simplifying Healthcare Access", 
                             font=("Arial", 12), bg="#28a745", fg="white")
        slogan_text.place(relx=0.95, rely=0.7, anchor="e")
        
        # User information display
        info_frame = tk.Frame(main_frame, bg="white", pady=20)
        info_frame.pack(fill=tk.X)
        
        # Display username from dashboard
        username_label = tk.Label(info_frame, text=f"User: {self.user_name}", font=("Arial", 14, "bold"), bg="white")
        username_label.pack(pady=5)
        
         # Create bookings table frame
        self.table_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SOLID)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create details display frame
        self.details_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SOLID)
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Back button frame should be AFTER the details frame
        button_frame = tk.Frame(main_frame, bg="white", pady=10)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Pack at the bottom
        
        back_button = tk.Button(button_frame, text="Back to Dashboard", command=self.back_to_dashboard, 
                            bg="white", fg="#28a745", font=("Arial", 14, "bold"),
                            width=20, relief=tk.SOLID, bd=1)
        back_button.pack()
    
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
    
    def load_bookings(self):
        """Load and display booking history"""
        connection = self.db_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Fetch all bookings for this user including delivery info
            query = """
            SELECT booking_id, booking_date, items_data, delivery_date, delivery_time_slot, delivery_instructions
            FROM medical_bookings
            WHERE p_username = %s
            ORDER BY booking_date DESC
            """
            cursor.execute(query, (self.username,))
            bookings = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            # Clear the table frame
            for widget in self.table_frame.winfo_children():
                widget.destroy()
            
            # Create table headers with delivery info and total amount
            headers = ["Booking ID", "Order Date", "Time", "Medicines", "Tests", "Diagnostics", "Total Amount", "Delivery Date", "Time Slot", "Details"]
            
            # Create header row
            for i, header in enumerate(headers):
                header_label = tk.Label(self.table_frame, text=header, font=("Arial", 12, "bold"),
                                    bg="#e1f0da", relief=tk.RIDGE, bd=1, padx=5, pady=5)
                header_label.grid(row=0, column=i, sticky="nsew")
                self.table_frame.columnconfigure(i, weight=1)
            
            # Add booking rows
            if not bookings:
                no_bookings_label = tk.Label(self.table_frame, text="No bookings found", 
                                        font=("Arial", 12), bg="white")
                no_bookings_label.grid(row=1, column=0, columnspan=len(headers), sticky="nsew", pady=10)
                return
            
            for row_idx, booking in enumerate(bookings, start=1):
                booking_id = booking[0]
                booking_date = booking[1]
                items_data = json.loads(booking[2])
                delivery_date = booking[3]
                delivery_time_slot = booking[4]
                delivery_instructions = booking[5]
                
                # Format date and time
                date_str = booking_date.strftime("%Y-%m-%d")
                time_str = booking_date.strftime("%H:%M:%S")
                
                # Format delivery date
                delivery_date_str = delivery_date.strftime("%Y-%m-%d") if delivery_date else "N/A"
                
                # Count items
                medicine_count = len(items_data.get("medicines", []))
                test_count = len(items_data.get("tests", []))
                diagnostic_count = len(items_data.get("diagnostics", []))
                
                # Get total price
                total_price = items_data.get("total_price", 0)
                
                # Create row data
                row_data = [
                    booking_id[:8] + "...",  # Show only first 8 chars of UUID
                    date_str,
                    time_str,
                    f"{medicine_count} items" if medicine_count else "-",
                    f"{test_count} items" if test_count else "-",
                    f"{diagnostic_count} items" if diagnostic_count else "-",
                    f"₹{total_price:.2f}",  # Add total price column
                    delivery_date_str,
                    delivery_time_slot if delivery_time_slot else "N/A"
                ]
                
                # Add row data cells
                for col_idx, data in enumerate(row_data):
                    cell = tk.Label(self.table_frame, text=data, font=("Arial", 10),
                                bg="white", relief=tk.RIDGE, bd=1, padx=5, pady=5)
                    cell.grid(row=row_idx, column=col_idx, sticky="nsew")
                
                # Add details button
                details_btn = tk.Button(self.table_frame, text="View", bg="#28a745", fg="white",
                                    command=lambda b_id=booking_id, b_data=items_data, b_delivery_date=delivery_date_str, 
                                                b_delivery_time=delivery_time_slot, b_instructions=delivery_instructions: 
                                    self.show_booking_details(b_id, b_data, b_delivery_date, b_delivery_time, b_instructions))
                details_btn.grid(row=row_idx, column=len(row_data), sticky="nsew", padx=5, pady=5)
                
                # Configure row
                self.table_frame.rowconfigure(row_idx, weight=1)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load booking history: {e}")
    
    def show_booking_details(self, booking_id, items_data, delivery_date, delivery_time, delivery_instructions):
        """Display detailed view of a booking"""
        # Clear details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Create header
        header_label = tk.Label(self.details_frame, text=f"Booking Details - ID: {booking_id}", 
                            font=("Arial", 14, "bold"), bg="#e1f0da", padx=10, pady=5)
        header_label.pack(fill=tk.X)
        
        # Create content frame with scrollbar
        content_frame = tk.Frame(self.details_frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Track total price if not already in the data
        total_price = items_data.get("total_price", 0)
        
        # Display medicines
        if items_data.get("medicines"):
            tk.Label(content_frame, text="MEDICINES & CONSUMABLES:", font=("Arial", 12, "bold"), 
                bg="white", anchor="w").pack(fill=tk.X, pady=(10, 5))
            
            for med in items_data["medicines"]:
                price_str = ""
                if "price" in med and "total" in med:
                    price_str = f" - ₹{med['price']:.2f} x {med['quantity']} = ₹{med['total']:.2f}"
                    # Add to total if not already included
                    if "total_price" not in items_data:
                        total_price += med['total']
                        
                tk.Label(content_frame, text=f"• {med['item']} (Qty: {med['quantity']}){price_str}", 
                    font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X)
        
        # Display tests
        if items_data.get("tests"):
            tk.Label(content_frame, text="TESTS:", font=("Arial", 12, "bold"), 
                bg="white", anchor="w").pack(fill=tk.X, pady=(10, 5))
            
            for test in items_data["tests"]:
                price_str = ""
                if isinstance(test, dict) and "price" in test:
                    price_str = f" - ₹{test['price']:.2f}"
                    # Add to total if not already included
                    if "total_price" not in items_data:
                        total_price += test['price']
                        
                    test_name = test['item']
                else:
                    test_name = test  # For backward compatibility
                    
                tk.Label(content_frame, text=f"• {test_name}{price_str}", 
                    font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X)
        
        # Display diagnostics
        if items_data.get("diagnostics"):
            tk.Label(content_frame, text="DIAGNOSTICS:", font=("Arial", 12, "bold"), 
                bg="white", anchor="w").pack(fill=tk.X, pady=(10, 5))
            
            for diag in items_data["diagnostics"]:
                price_str = ""
                if "price" in diag and "total" in diag:
                    price_str = f" - ₹{diag['price']:.2f} x {diag['quantity']} = ₹{diag['total']:.2f}"
                    # Add to total if not already included
                    if "total_price" not in items_data:
                        total_price += diag['total']
                        
                tk.Label(content_frame, text=f"• {diag['item']} (Qty: {diag['quantity']}){price_str}", 
                    font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X)
                
        # Use the stored total price if available, otherwise calculate it
        total_price = items_data.get("total_price", 0)
        
        # Display total price
        tk.Label(content_frame, text=f"TOTAL AMOUNT: ₹{total_price:.2f}", font=("Arial", 12, "bold"), 
            bg="white", fg="#28a745", anchor="w").pack(fill=tk.X, pady=(10, 5))
        
        
        # Display payment method
        tk.Label(content_frame, text="Payment Method: Cash on Delivery", font=("Arial", 10), 
            bg="white", anchor="w").pack(fill=tk.X)
        
        # Display delivery details
        tk.Label(content_frame, text="DELIVERY DETAILS:", font=("Arial", 12, "bold"), 
            bg="white", anchor="w").pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(content_frame, text=f"• Delivery Date: {delivery_date}", 
            font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X)
        
        tk.Label(content_frame, text=f"• Time Slot: {delivery_time if delivery_time else 'N/A'}", 
            font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X)
        
        if delivery_instructions:
            tk.Label(content_frame, text=f"• Special Instructions: {delivery_instructions}", 
                font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X)
    
    def back_to_dashboard(self):
        self.root.destroy()
        from userdashboard import NavigationApp
        new_root = tk.Tk()
        app = NavigationApp(new_root, self.user_name, self.username)
        new_root.mainloop()