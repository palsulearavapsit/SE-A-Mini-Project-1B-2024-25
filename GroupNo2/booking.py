# Import necessary libraries
import tkinter as tk
from tkinter import messagebox, simpledialog
from database import create_connection  # Custom module for database connection
from datetime import datetime, timedelta  # For date handling
from decimal import Decimal  # For precise monetary calculations

class RentVehiclePage:
    """Class for the vehicle rental page in the application"""
    
    def __init__(self, root, on_back):
        """Initialize the RentVehiclePage
        
        Args:
            root: The parent tkinter widget
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()  # Create the UI elements
        self.vehicle_id_map = {}  # To store vehicle_id for each vehicle_number

    def create_widgets(self):
        """Create and arrange all the widgets for the rental page"""
        
        # Create a frame with scrollbars for the content
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Title label
        tk.Label(main_frame, text="Rent Vehicle", font=("Arial", 24)).pack(pady=20)

        # Form frame for all input fields
        form_frame = tk.Frame(main_frame)
        form_frame.pack(padx=20, pady=10)

        # Customer section - Mobile number input and verification
        tk.Label(form_frame, text="Customer's Mobile Number").grid(row=0, column=0, sticky="w", pady=5)
        self.mobile_number_entry = tk.Entry(form_frame, width=30)
        self.mobile_number_entry.grid(row=0, column=1, pady=5, padx=10)
        tk.Button(form_frame, text="Verify Customer", command=self.verify_customer).grid(row=0, column=2, pady=5)

        # Display customer name when verified
        self.customer_name_var = tk.StringVar()
        tk.Label(form_frame, textvariable=self.customer_name_var).grid(row=1, column=1, sticky="w", pady=5)

        # Date section - Check-in and check-out dates
        tk.Label(form_frame, text="Check-in Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=5)
        self.check_in_date_entry = tk.Entry(form_frame, width=30)
        self.check_in_date_entry.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Check-out Date (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=5)
        self.check_out_date_entry = tk.Entry(form_frame, width=30)
        self.check_out_date_entry.grid(row=3, column=1, pady=5, padx=10)
        
        # Calculate days button
        tk.Button(form_frame, text="Calculate Duration", command=self.calculate_days).grid(row=3, column=2, pady=5)

        # Vehicle selection section
        tk.Label(form_frame, text="Vehicle Type").grid(row=4, column=0, sticky="w", pady=5)
        self.vehicle_type_var = tk.StringVar(value="SUV")
        vehicle_types = ["SUV", "Sedan", "Hatchback", "Bike"]
        tk.OptionMenu(form_frame, self.vehicle_type_var, *vehicle_types).grid(row=4, column=1, sticky="w", pady=5)

        # Button to fetch available vehicles
        tk.Button(form_frame, text="Fetch Available Vehicles", command=self.fetch_available_vehicles).grid(row=4, column=2, pady=5)

        # Available vehicles dropdown
        tk.Label(form_frame, text="Available Vehicles").grid(row=5, column=0, sticky="w", pady=5)
        self.available_vehicles_var = tk.StringVar(value="Select Vehicle")
        self.available_vehicles_menu = tk.OptionMenu(form_frame, self.available_vehicles_var, "")
        self.available_vehicles_menu.grid(row=5, column=1, sticky="w", pady=5)
        
        # Vehicle price display
        self.vehicle_price_var = tk.StringVar()
        tk.Label(form_frame, textvariable=self.vehicle_price_var).grid(row=5, column=2, sticky="w", pady=5)
        
        # Update price button
        tk.Button(form_frame, text="Get Price Details", command=self.update_price_details).grid(row=6, column=2, pady=5)

        # Booking details section - Cost calculations
        tk.Label(form_frame, text="Number of Days").grid(row=7, column=0, sticky="w", pady=5)
        self.number_of_days_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.number_of_days_var, state="readonly").grid(row=7, column=1, sticky="w", pady=5, padx=10)

        tk.Label(form_frame, text="Actual Cost").grid(row=8, column=0, sticky="w", pady=5)
        self.actual_cost_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.actual_cost_var, state="readonly").grid(row=8, column=1, sticky="w", pady=5, padx=10)

        tk.Label(form_frame, text="Tax (10%)").grid(row=9, column=0, sticky="w", pady=5)
        self.tax_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.tax_var, state="readonly").grid(row=9, column=1, sticky="w", pady=5, padx=10)

        tk.Label(form_frame, text="Total Cost").grid(row=10, column=0, sticky="w", pady=5)
        self.total_cost_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.total_cost_var, state="readonly").grid(row=10, column=1, sticky="w", pady=5, padx=10)

        # Buttons frame for action buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Book Now and Back buttons
        tk.Button(button_frame, text="Book Now", command=self.book_vehicle, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Back to Homepage", command=self.on_back).pack(side=tk.LEFT, padx=10)
        
        # Set default values for testing
        today = datetime.now().strftime("%Y-%m-%d")
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.check_in_date_entry.insert(0, today)
        self.check_out_date_entry.insert(0, next_week)

    def verify_customer(self):
        """Verify if customer exists in database using mobile number"""
        mobile_number = self.mobile_number_entry.get().strip()
        
        if not mobile_number:
            messagebox.showerror("Error", "Please enter a mobile number")
            return
            
        # Connect to database and verify customer
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT id, name FROM customers WHERE mobile_number = %s", (mobile_number,))
                customer = cursor.fetchone()
                
                if customer:
                    # Customer found - display name and store ID
                    self.customer_name_var.set(f"Customer: {customer[1]}")
                    self.customer_id = customer[0]  # Store customer ID for booking
                else:
                    # Customer not found - prompt to add new customer
                    if messagebox.askyesno("Customer Not Found", "Customer not found. Would you like to add this customer?"):
                        messagebox.showinfo("Info", "Please use the Add Customer feature to register this customer first.")
                    self.customer_name_var.set("Customer not found")
            except Exception as e:
                messagebox.showerror("Database Error", f"Error verifying customer: {e}")
            finally:
                cursor.close()
                connection.close()

    def calculate_days(self):
        """Calculate the number of days between check-in and check-out dates"""
        try:
            check_in_date = self.check_in_date_entry.get().strip()
            check_out_date = self.check_out_date_entry.get().strip()
            
            if not check_in_date or not check_out_date:
                messagebox.showerror("Error", "Please enter both check-in and check-out dates")
                return
                
            # Parse dates and validate
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
            
            if check_out <= check_in:
                messagebox.showerror("Error", "Check-out date must be after check-in date")
                return
                
            # Calculate and display days
            days = (check_out - check_in).days
            self.number_of_days_var.set(str(days))
            
            # Update price if a vehicle is selected
            if self.available_vehicles_var.get() != "Select Vehicle":
                self.update_price_details()
                
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating days: {e}")

    def fetch_available_vehicles(self):
        """Fetch available vehicles of selected type for the given dates"""
        vehicle_type = self.vehicle_type_var.get()
        check_in_date = self.check_in_date_entry.get().strip()
        check_out_date = self.check_out_date_entry.get().strip()
        
        if not check_in_date or not check_out_date:
            messagebox.showerror("Error", "Please enter check-in and check-out dates first")
            return
            
        try:
            # Validate dates
            check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
            
            if check_out <= check_in:
                messagebox.showerror("Error", "Check-out date must be after check-in date")
                return
                
            # Connect to database and fetch available vehicles
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    # Find vehicles of the selected type that are not booked for the given dates
                    cursor.execute("""
                        SELECT v.id, v.name, v.vehicle_number, v.price_per_day 
                        FROM vehicles v
                        WHERE v.type = %s
                        AND v.id NOT IN (
                            SELECT vehicle_id FROM bookings
                            WHERE (check_in_date <= %s AND check_out_date >= %s)
                            OR (check_in_date <= %s AND check_out_date >= %s)
                            OR (check_in_date >= %s AND check_out_date <= %s)
                        )
                    """, (vehicle_type, check_out_date, check_in_date, check_in_date, check_in_date, check_in_date, check_out_date))
                    
                    vehicles = cursor.fetchall()
                    
                    if vehicles:
                        # Store vehicle IDs mapped to their numbers for later use
                        self.vehicle_id_map = {f"{vehicle[1]} - {vehicle[2]}": vehicle[0] for vehicle in vehicles}
                        self.vehicle_price_map = {f"{vehicle[1]} - {vehicle[2]}": vehicle[3] for vehicle in vehicles}
                        
                        # Update dropdown menu with available vehicles
                        menu = self.available_vehicles_menu["menu"]
                        menu.delete(0, "end")
                        
                        vehicle_labels = list(self.vehicle_id_map.keys())
                        for vehicle_label in vehicle_labels:
                            menu.add_command(label=vehicle_label, 
                                            command=lambda v=vehicle_label: self.on_vehicle_selected(v))
                        
                        # Set first vehicle as default
                        self.available_vehicles_var.set(vehicle_labels[0])
                        self.on_vehicle_selected(vehicle_labels[0])
                    else:
                        self.available_vehicles_var.set("No vehicles available")
                        messagebox.showinfo("No Vehicles", "No vehicles available for the selected type and dates")
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error fetching vehicles: {e}")
                finally:
                    cursor.close()
                    connection.close()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching vehicles: {e}")
    
    def on_vehicle_selected(self, vehicle_label):
        """Handle vehicle selection from dropdown"""
        self.available_vehicles_var.set(vehicle_label)
        # Display price of selected vehicle
        if vehicle_label in self.vehicle_price_map:
            price = self.vehicle_price_map[vehicle_label]
            self.vehicle_price_var.set(f"Price/day: ₹{price}")
            # Update cost calculations
            self.update_price_details()
        
    def update_price_details(self):
        """Update the price details based on selected vehicle and duration"""
        vehicle_label = self.available_vehicles_var.get()
        days_str = self.number_of_days_var.get()
        
        if vehicle_label == "Select Vehicle" or vehicle_label == "No vehicles available" or not days_str:
            return
            
        try:
            days = int(days_str)
            if days <= 0:
                return
                
            if vehicle_label in self.vehicle_price_map:
                price_per_day = self.vehicle_price_map[vehicle_label]
                
                # Convert to Decimal for precise calculation
                if not isinstance(price_per_day, Decimal):
                    price_per_day = Decimal(str(price_per_day))
                    
                # Convert days to Decimal to avoid type mismatch
                days_decimal = Decimal(str(days))
                
                # Perform calculations with Decimal values
                actual_cost = price_per_day * days_decimal
                tax = actual_cost * Decimal('0.10')  # 10% tax
                total_cost = actual_cost + tax
                
                # Update the display fields
                self.actual_cost_var.set(f"{actual_cost:.2f}")
                self.tax_var.set(f"{tax:.2f}")
                self.total_cost_var.set(f"{total_cost:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating prices: {e}")
                
    def book_vehicle(self):
        """Handle the vehicle booking process"""
        # Get all required data from the form
        mobile_number = self.mobile_number_entry.get().strip()
        check_in_date = self.check_in_date_entry.get().strip()
        check_out_date = self.check_out_date_entry.get().strip()
        vehicle_label = self.available_vehicles_var.get()
        total_cost_str = self.total_cost_var.get()
        
        # Validate all required fields are filled
        if (not mobile_number or not check_in_date or not check_out_date or 
            vehicle_label == "Select Vehicle" or vehicle_label == "No vehicles available" or not total_cost_str):
            messagebox.showerror("Error", "All fields are required to book a vehicle")
            return
            
        try:
            # Ensure customer exists
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    # First verify customer exists
                    cursor.execute("SELECT id FROM customers WHERE mobile_number = %s", (mobile_number,))
                    customer = cursor.fetchone()
                    
                    if not customer:
                        messagebox.showerror("Error", "Customer not found. Please verify the mobile number.")
                        return
                        
                    customer_id = customer[0]
                    vehicle_id = self.vehicle_id_map.get(vehicle_label)
                    
                    if not vehicle_id:
                        messagebox.showerror("Error", "Invalid vehicle selection")
                        return
                        
                    total_cost = float(total_cost_str)
                    
                    # Insert booking into database
                    cursor.execute("""
                        INSERT INTO bookings 
                        (customer_id, vehicle_id, check_in_date, check_out_date, total_cost)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (customer_id, vehicle_id, check_in_date, check_out_date, total_cost))
                    connection.commit()
                    messagebox.showinfo("Success", "Vehicle booked successfully!")
                    # Reset form after successful booking
                    self.reset_form()
                except Exception as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error booking vehicle: {e}")
                finally:
                    cursor.close()
                    connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error booking vehicle: {e}")
    
    def reset_form(self):
        """Reset the form after successful booking"""
        self.mobile_number_entry.delete(0, tk.END)
        self.customer_name_var.set("")
        
        # Reset date fields to current and future week
        today = datetime.now().strftime("%Y-%m-%d")
        next_week = (datetime.now().replace(day=datetime.now().day + 7)).strftime("%Y-%m-%d")
        self.check_in_date_entry.delete(0, tk.END)
        self.check_out_date_entry.delete(0, tk.END)
        self.check_in_date_entry.insert(0, today)
        self.check_out_date_entry.insert(0, next_week)
        
        # Reset calculations
        self.number_of_days_var.set("")
        self.actual_cost_var.set("")
        self.tax_var.set("")
        self.total_cost_var.set("")
        self.vehicle_price_var.set("")
        
        # Reset vehicle selection
        self.available_vehicles_var.set("Select Vehicle")
        self.vehicle_type_var.set("SUV")


class BookedVehicleDetailsPage:
    """Class for viewing booked vehicle details"""
    
    def __init__(self, root, on_back):
        """Initialize the BookedVehicleDetailsPage
        
        Args:
            root: The parent tkinter widget
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange all the widgets for the booked details page"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="Booked Vehicle Details", font=("Arial", 24)).pack(pady=20)

        # Search frame
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Enter Phone Number:").pack(side=tk.LEFT, padx=5)
        self.phone_number_entry = tk.Entry(search_frame, width=20)
        self.phone_number_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_bookings, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        # Results frame with scrollbar
        results_frame = tk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=1, pady=10)
        
        # Create text widget to display results
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=15, width=70)
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        # Disable text widget for editing
        self.results_text.config(state=tk.DISABLED)
        
        # Navigation buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Back to Homepage", command=self.on_back).pack()

    def search_bookings(self):
        """Search for bookings using customer's phone number"""
        phone_number = self.phone_number_entry.get().strip()

        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number to search.")
            return

        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        # Connect to database and search for bookings
        connection = create_connection()
        if connection:
            cursor = connection.cursor(buffered=True)
            try:
                # Check if customer exists with this number
                cursor.execute("SELECT id FROM customers WHERE mobile_number = %s", (phone_number,))
                customer = cursor.fetchone()
                
                if not customer:
                    self.results_text.insert(tk.END, f"No customer found with phone number: {phone_number}\n")
                    return
                    
                # Query for bookings
                cursor.execute("""
                    SELECT 
                        b.id, 
                        c.name AS customer_name, 
                        c.mobile_number,
                        v.name AS vehicle_name, 
                        v.type AS vehicle_type,
                        v.vehicle_number, 
                        DATE_FORMAT(b.check_in_date, '%Y-%m-%d') AS check_in,  
                        DATE_FORMAT(b.check_out_date, '%Y-%m-%d') AS check_out,
                        b.total_cost,
                        DATEDIFF(b.check_out_date, b.check_in_date) AS days
                    FROM bookings b
                    JOIN customers c ON b.customer_id = c.id
                    JOIN vehicles v ON b.vehicle_id = v.id
                    WHERE c.mobile_number = %s
                    ORDER BY b.check_in_date DESC
                """, (phone_number,))
                
                bookings = cursor.fetchall()
                
                if bookings:
                    self.results_text.insert(tk.END, f"Found {len(bookings)} bookings for {bookings[0][1]}\n\n")
                    
                    # Display each booking's details
                    for booking in bookings:
                        self.results_text.insert(tk.END, f"Booking ID: {booking[0]}\n")
                        self.results_text.insert(tk.END, f"Customer: {booking[1]} (Phone: {booking[2]})\n")
                        self.results_text.insert(tk.END, f"Vehicle: {booking[3]} ({booking[4]}) - {booking[5]}\n")
                        self.results_text.insert(tk.END, f"Duration: {booking[9]} days ({booking[6]} to {booking[7]})\n")
                        self.results_text.insert(tk.END, f"Total Cost: ₹{booking[8]:.2f}\n")
                        self.results_text.insert(tk.END, "-" * 50 + "\n\n")
                else:
                    self.results_text.insert(tk.END, f"No bookings found for phone number: {phone_number}\n")
            except Exception as e:
                self.results_text.insert(tk.END, f"Error searching bookings: {e}\n")
            finally:
                cursor.close()
                connection.close()
        
        # Disable text widget again after updating
        self.results_text.config(state=tk.DISABLED)


class CancelBookingsPage:
    """Class for canceling existing bookings"""
    
    def __init__(self, root, on_back):
        """Initialize the CancelBookingsPage
        
        Args:
            root: The parent tkinter widget
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()
        self.bookings = []  # To store fetched bookings

    def create_widgets(self):
        """Create and arrange all the widgets for the cancel bookings page"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="Cancel Booking", font=("Arial", 24)).pack(pady=20)

        # Search frame
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Enter Phone Number:").pack(side=tk.LEFT, padx=5)
        self.phone_number_entry = tk.Entry(search_frame, width=20)
        self.phone_number_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Fetch Bookings", command=self.fetch_bookings, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        # Create frame for bookings list
        bookings_frame = tk.Frame(main_frame)
        bookings_frame.pack(fill=tk.BOTH, expand=1, pady=10)
        
        # Create listbox to display bookings
        self.bookings_listbox = tk.Listbox(bookings_frame, height=10, width=70)
        scrollbar = tk.Scrollbar(bookings_frame, command=self.bookings_listbox.yview)
        self.bookings_listbox.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bookings_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        # Action buttons frame
        actions_frame = tk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(actions_frame, text="Cancel Selected Booking", command=self.cancel_booking, bg="#FF5722", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="View Booking Details", command=self.view_booking_details).pack(side=tk.LEFT, padx=5)
        
        # Navigation buttons frame
        nav_frame = tk.Frame(main_frame)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="Back to Homepage", command=self.on_back).pack()

    def fetch_bookings(self):
        """Fetch bookings for a given phone number"""
        phone_number = self.phone_number_entry.get().strip()

        if not phone_number:
            messagebox.showerror("Error", "Please enter a phone number to fetch bookings.")
            return

        # Clear previous results
        self.bookings_listbox.delete(0, tk.END)
        self.bookings = []

        # Connect to database and fetch bookings
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT 
                        b.id, 
                        c.name, 
                        v.name, 
                        v.vehicle_number, 
                        DATE_FORMAT(b.check_in_date, '%Y-%m-%d'),
                        DATE_FORMAT(b.check_out_date, '%Y-%m-%d'), 
                        b.total_cost
                    FROM bookings b
                    JOIN customers c ON b.customer_id = c.id
                    JOIN vehicles v ON b.vehicle_id = v.id
                    WHERE c.mobile_number = %s
                    ORDER BY b.check_in_date
                """, (phone_number,))
                
                fetched_bookings = cursor.fetchall()
                
                if fetched_bookings:
                    # Populate the bookings list and listbox
                    for i, booking in enumerate(fetched_bookings):
                        self.bookings.append(booking)
                        display_text = f"ID: {booking[0]} - {booking[2]} ({booking[3]}) - {booking[4]} to {booking[5]}"
                        self.bookings_listbox.insert(tk.END, display_text)
                else:
                    messagebox.showinfo("No Bookings", f"No bookings found for phone number: {phone_number}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch bookings: {e}")
            finally:
                cursor.close()
                connection.close()

    def view_booking_details(self):
        """Display details of the selected booking"""
        selected_index = self.bookings_listbox.curselection()
        
        if not selected_index:
            messagebox.showinfo("Select Booking", "Please select a booking to view.")
            return
            
        # Get the selected booking and display its details
        booking = self.bookings[selected_index[0]]
        
        details = (f"Booking ID: {booking[0]}\n"
                   f"Customer: {booking[1]}\n"
                   f"Vehicle: {booking[2]} - {booking[3]}\n"
                   f"Period: {booking[4]} to {booking[5]}\n"
                   f"Total Cost: ₹{booking[6]}")
                   
        messagebox.showinfo("Booking Details", details)

    def cancel_booking(self):
        """Cancel the selected booking"""
        selected_index = self.bookings_listbox.curselection()
        
        if not selected_index:
            messagebox.showinfo("Select Booking", "Please select a booking to cancel.")
            return
            
        booking = self.bookings[selected_index[0]]
        booking_id = booking[0]
        
        # Confirm cancellation with user
        if messagebox.askyesno("Confirm Cancellation", 
                             f"Are you sure you want to cancel booking {booking_id} for {booking[2]}?"):
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    # Delete the booking from database
                    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
                    connection.commit()
                    messagebox.showinfo("Success", "Booking cancelled successfully!")
                    
                    # Remove from list and refresh display
                    self.bookings.pop(selected_index[0])
                    self.bookings_listbox.delete(selected_index[0])
                    
                except Exception as e:
                    connection.rollback()
                    messagebox.showerror("Error", f"Failed to cancel booking: {e}")
                finally:
                    cursor.close()
                    connection.close()