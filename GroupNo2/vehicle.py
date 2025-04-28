import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import create_connection
import re

class AddVehiclePage:
    def __init__(self, root, on_back):
        """
        Initialize the Add Vehicle page.
        
        Args:
            root: The parent Tkinter window/container
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()
        self.load_vehicles()  # Load existing vehicles for the list view

    def create_widgets(self):
        """
        Create and arrange all GUI widgets for the page.
        Sets up a notebook (tabbed interface) with two tabs:
        1. Add New Vehicle
        2. View/Search Vehicles
        """
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Add Vehicle
        add_frame = ttk.Frame(notebook)
        notebook.add(add_frame, text="Add New Vehicle")
        
        # Tab 2: View/Search Vehicles
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="View/Search Vehicles")
        
        # Configure Add Vehicle tab
        self.setup_add_vehicle_tab(add_frame)
        
        # Configure View/Search tab
        self.setup_view_search_tab(view_frame)

    def setup_add_vehicle_tab(self, parent):
        """
        Set up the 'Add New Vehicle' tab with form fields and buttons.
        
        Args:
            parent: The parent frame for this tab
        """
        # Title
        tk.Label(parent, text="Add New Vehicle", font=("Arial", 20, "bold"), bg="#f2f2f2").pack(pady=10)
        
        # Main form frame
        form_frame = tk.Frame(parent, bg="#f2f2f2")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Vehicle details frame - use grid for better alignment
        details_frame = tk.Frame(form_frame, bg="#f2f2f2")
        details_frame.pack(fill=tk.X, pady=10)
        
        # Basic information section
        basic_frame = tk.LabelFrame(details_frame, text="Basic Information", bg="#f2f2f2", padx=10, pady=10)
        basic_frame.pack(fill=tk.X, pady=5)
        
        # Row 0: Vehicle Name and Model
        tk.Label(basic_frame, text="Vehicle Name:", bg="#f2f2f2").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = ttk.Entry(basic_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(basic_frame, text="Vehicle Model:", bg="#f2f2f2").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.model_entry = ttk.Entry(basic_frame, width=25)
        self.model_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # Row 1: Vehicle Type and Vehicle Number
        tk.Label(basic_frame, text="Vehicle Type:", bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.type_var = tk.StringVar(value="SUV")
        vehicle_types = ["SUV", "Sedan", "Hatchback", "Bike"]
        ttk.Combobox(basic_frame, textvariable=self.type_var, values=vehicle_types, state="readonly", width=22).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(basic_frame, text="Vehicle Number:", bg="#f2f2f2").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.vehicle_number_entry = ttk.Entry(basic_frame, width=25)
        self.vehicle_number_entry.grid(row=1, column=3, padx=10, pady=5)
        
        # Additional details section
        props_frame = tk.LabelFrame(details_frame, text="Vehicle Properties", bg="#f2f2f2", padx=10, pady=10)
        props_frame.pack(fill=tk.X, pady=5)
        
        # Row 0: Luggage Capacity and Fuel Type
        tk.Label(props_frame, text="Luggage Capacity:", bg="#f2f2f2").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.luggage_capacity_entry = ttk.Entry(props_frame, width=25)
        self.luggage_capacity_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(props_frame, text="Fuel Type:", bg="#f2f2f2").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.fuel_type_var = tk.StringVar(value="Petrol")
        fuel_types = ["Petrol", "Diesel", "Electric"]
        ttk.Combobox(props_frame, textvariable=self.fuel_type_var, values=fuel_types, state="readonly", width=22).grid(row=0, column=3, padx=10, pady=5)
        
        # Row 1: Price Per Day
        tk.Label(props_frame, text="Price Per Day (₹):", bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.price_per_day_entry = ttk.Entry(props_frame, width=25)
        self.price_per_day_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Error message label
        self.error_var = tk.StringVar()
        error_label = tk.Label(form_frame, textvariable=self.error_var, fg="red", bg="#f2f2f2")
        error_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg="#f2f2f2")
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Vehicle", command=self.add_vehicle).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Homepage", command=self.on_back).pack(side=tk.LEFT, padx=10)

    def setup_view_search_tab(self, parent):
        """
        Set up the 'View/Search Vehicles' tab with search controls and results display.
        
        Args:
            parent: The parent frame for this tab
        """
        # Main container
        main_frame = tk.Frame(parent, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Search section
        search_frame = tk.LabelFrame(main_frame, text="Search Vehicles", bg="#f2f2f2", padx=10, pady=10)
        search_frame.pack(fill=tk.X, pady=10)
        
        # Search options
        search_options_frame = tk.Frame(search_frame, bg="#f2f2f2")
        search_options_frame.pack(fill=tk.X, pady=5)
        
        # Search field selection
        tk.Label(search_options_frame, text="Search by:", bg="#f2f2f2").pack(side=tk.LEFT, padx=5)
        self.search_field_var = tk.StringVar(value="Vehicle Number")
        search_fields = ["Vehicle Number", "Name", "Model", "Type"]
        ttk.Combobox(search_options_frame, textvariable=self.search_field_var, values=search_fields, 
                     state="readonly", width=15).pack(side=tk.LEFT, padx=5)
        
        # Search entry
        self.search_entry = ttk.Entry(search_options_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=10)
        
        # Search button
        ttk.Button(search_options_frame, text="Search", command=self.search_vehicle).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_options_frame, text="Show All", command=self.load_vehicles).pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = tk.LabelFrame(main_frame, text="Vehicle List", bg="#f2f2f2", padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview for vehicles
        columns = ("ID", "Name", "Model", "Type", "Luggage", "Fuel", "Price", "Number")
        self.vehicle_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
        
        # Define column widths and headings
        self.vehicle_tree.column("ID", width=50)
        self.vehicle_tree.column("Name", width=150)
        self.vehicle_tree.column("Model", width=150)
        self.vehicle_tree.column("Type", width=100)
        self.vehicle_tree.column("Luggage", width=100)
        self.vehicle_tree.column("Fuel", width=100)
        self.vehicle_tree.column("Price", width=100)
        self.vehicle_tree.column("Number", width=120)
        
        self.vehicle_tree.heading("ID", text="ID")
        self.vehicle_tree.heading("Name", text="Vehicle Name")
        self.vehicle_tree.heading("Model", text="Model")
        self.vehicle_tree.heading("Type", text="Type")
        self.vehicle_tree.heading("Luggage", text="Luggage")
        self.vehicle_tree.heading("Fuel", text="Fuel Type")
        self.vehicle_tree.heading("Price", text="Price/Day")
        self.vehicle_tree.heading("Number", text="Vehicle Number")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.vehicle_tree.yview)
        self.vehicle_tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vehicle_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind double click to view details
        self.vehicle_tree.bind("<Double-1>", self.show_vehicle_details)
        
        # Action buttons for selected vehicle
        action_frame = tk.Frame(main_frame, bg="#f2f2f2")
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="View Details", command=self.show_selected_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Edit Vehicle", command=self.edit_selected_vehicle).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Delete Vehicle", command=self.delete_selected_vehicle).pack(side=tk.LEFT, padx=5)

    def validate_form(self):
        """
        Validate the form inputs before adding a vehicle.
        
        Returns:
            bool: True if all validations pass, False otherwise
        """
        self.error_var.set("")  # Clear previous error
        
        # Get form values
        name = self.name_entry.get().strip()
        model = self.model_entry.get().strip()
        vehicle_type = self.type_var.get()
        luggage_capacity = self.luggage_capacity_entry.get().strip()
        fuel_type = self.fuel_type_var.get()
        price_per_day = self.price_per_day_entry.get().strip()
        vehicle_number = self.vehicle_number_entry.get().strip()
        
        # Check required fields
        if not name or not model or not luggage_capacity or not price_per_day or not vehicle_number:
            self.error_var.set("All fields are required!")
            return False
            
        # Validate luggage capacity is an integer
        try:
            luggage_int = int(luggage_capacity)
            if luggage_int < 0:
                self.error_var.set("Luggage capacity must be a positive number!")
                return False
        except ValueError:
            self.error_var.set("Luggage capacity must be a number!")
            return False
            
        # Validate price per day is a valid number
        try:
            price_float = float(price_per_day)
            if price_float <= 0:
                self.error_var.set("Price per day must be greater than zero!")
                return False
        except ValueError:
            self.error_var.set("Price per day must be a valid number!")
            return False
            
        # Validate vehicle number format (basic check for now)
        if not re.match(r'^[A-Z0-9\- ]{4,15}$', vehicle_number):
            self.error_var.set("Vehicle number format is invalid!")
            return False
            
        return True

    def add_vehicle(self):
        """Add a new vehicle to the database after validation."""
        if not self.validate_form():
            return
            
        # Get form values
        model = self.model_entry.get().strip()
        name = self.name_entry.get().strip()
        vehicle_type = self.type_var.get()
        luggage_capacity = int(self.luggage_capacity_entry.get().strip())
        fuel_type = self.fuel_type_var.get()
        price_per_day = float(self.price_per_day_entry.get().strip())
        vehicle_number = self.vehicle_number_entry.get().strip().upper()

        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # First check if vehicle number already exists
                cursor.execute("SELECT id FROM vehicles WHERE vehicle_number = %s", (vehicle_number,))
                if cursor.fetchone():
                    self.error_var.set(f"Vehicle with number {vehicle_number} already exists!")
                    return
                
                # Insert new vehicle
                cursor.execute("""
                    INSERT INTO vehicles (
                        model, name, type, luggage_capacity, fuel_type, price_per_day, vehicle_number
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (model, name, vehicle_type, luggage_capacity, fuel_type, price_per_day, vehicle_number))
                
                connection.commit()
                messagebox.showinfo("Success", f"Vehicle {name} ({vehicle_number}) added successfully!")
                
                # Clear form and refresh vehicle list
                self.clear_form()
                self.load_vehicles()
                
            except Exception as e:
                connection.rollback()
                error_msg = str(e)
                
                # More user-friendly error messages
                if "Duplicate entry" in error_msg and "vehicle_number" in error_msg:
                    self.error_var.set(f"Vehicle with number {vehicle_number} already exists!")
                else:
                    self.error_var.set(f"Failed to add vehicle: {error_msg}")
            finally:
                cursor.close()
                connection.close()

    def clear_form(self):
        """Reset all fields in the add vehicle form."""
        self.name_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.type_var.set("SUV")
        self.luggage_capacity_entry.delete(0, tk.END)
        self.fuel_type_var.set("Petrol")
        self.price_per_day_entry.delete(0, tk.END)
        self.vehicle_number_entry.delete(0, tk.END)
        self.error_var.set("")
    
    def load_vehicles(self):
        """Load all vehicles from database into the treeview."""
        # Clear existing items
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT id, name, model, type, luggage_capacity, fuel_type, price_per_day, vehicle_number
                    FROM vehicles
                    ORDER BY name
                """)
                
                vehicles = cursor.fetchall()
                
                if not vehicles:
                    # Insert a placeholder message
                    self.vehicle_tree.insert("", tk.END, values=("", "No vehicles found", "", "", "", "", "", ""))
                    return
                
                # Insert vehicles into the treeview
                for vehicle in vehicles:
                    self.vehicle_tree.insert("", tk.END, values=vehicle)
                    
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to load vehicles: {e}")
            finally:
                cursor.close()
                connection.close()

    def search_vehicle(self):
        """Search for vehicles based on selected criteria and search term."""
        search_term = self.search_entry.get().strip()
        search_field = self.search_field_var.get()
        
        if not search_term:
            messagebox.showinfo("Info", "Please enter a search term.")
            return
            
        # Clear existing items
        for item in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(item)
            
        # Map the search field to its database column name
        field_map = {
            "Vehicle Number": "vehicle_number",
            "Name": "name",
            "Model": "model",
            "Type": "type"
        }
        
        db_field = field_map.get(search_field, "vehicle_number")
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Use LIKE for partial matching
                query = f"""
                    SELECT id, name, model, type, luggage_capacity, fuel_type, price_per_day, vehicle_number
                    FROM vehicles
                    WHERE {db_field} LIKE %s
                    ORDER BY name
                """
                cursor.execute(query, (f"%{search_term}%",))
                
                vehicles = cursor.fetchall()
                
                if not vehicles:
                    # Insert a placeholder message
                    self.vehicle_tree.insert("", tk.END, values=("", f"No vehicles found matching '{search_term}'", "", "", "", "", "", ""))
                    return
                
                # Insert vehicles into the treeview
                for vehicle in vehicles:
                    self.vehicle_tree.insert("", tk.END, values=vehicle)
                    
            except Exception as e:
                messagebox.showerror("Database Error", f"Search failed: {e}")
            finally:
                cursor.close()
                connection.close()

    def show_vehicle_details(self, event):
        """
        Handle double-click event on a vehicle in the treeview.
        
        Args:
            event: The Tkinter event object
        """
        self.show_selected_details()

    def show_selected_details(self):
        """Display detailed information about the selected vehicle in a new window."""
        selected_item = self.vehicle_tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Select Vehicle", "Please select a vehicle to view details.")
            return
            
        # Get values of selected item
        values = self.vehicle_tree.item(selected_item[0], "values")
        
        if not values[0]:  # Handle the "No vehicles found" placeholder
            return
            
        # Format the details
        details = (
            f"Vehicle ID: {values[0]}\n\n"
            f"Name: {values[1]}\n"
            f"Model: {values[2]}\n"
            f"Type: {values[3]}\n"
            f"Luggage Capacity: {values[4]} bags\n"
            f"Fuel Type: {values[5]}\n"
            f"Price Per Day: ₹{values[6]}\n"
            f"Vehicle Number: {values[7]}\n"
        )
        
        # Create a new window for details
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Details: {values[1]} ({values[7]})")
        detail_window.geometry("400x300")
        detail_window.resizable(False, False)
        
        # Add details to window
        tk.Label(detail_window, text="Vehicle Details", font=("Arial", 16, "bold")).pack(pady=10)
        
        details_frame = tk.Frame(detail_window)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        detail_text = tk.Text(details_frame, wrap=tk.WORD, width=40, height=10)
        detail_text.insert(tk.END, details)
        detail_text.config(state=tk.DISABLED)  # Make read-only
        detail_text.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        ttk.Button(detail_window, text="Close", command=detail_window.destroy).pack(pady=10)
        
        # Make the window modal
        detail_window.transient(self.root)
        detail_window.grab_set()
        self.root.wait_window(detail_window)

    def edit_selected_vehicle(self):
        """Open an edit window for the selected vehicle."""
        selected_item = self.vehicle_tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Select Vehicle", "Please select a vehicle to edit.")
            return
            
        # Get values of selected item
        values = self.vehicle_tree.item(selected_item[0], "values")
        
        if not values[0]:  # Handle the "No vehicles found" placeholder
            return
            
        vehicle_id = values[0]
        
        # Create edit window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Vehicle: {values[1]} ({values[7]})")
        edit_window.geometry("500x400")
        edit_window.configure(bg="#f2f2f2")
        
        # Form frame
        form_frame = tk.Frame(edit_window, bg="#f2f2f2")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Vehicle details
        tk.Label(form_frame, text="Vehicle Name:", bg="#f2f2f2").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.insert(0, values[1])
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Vehicle Model:", bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        model_entry = ttk.Entry(form_frame, width=30)
        model_entry.insert(0, values[2])
        model_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Vehicle Type:", bg="#f2f2f2").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        type_var = tk.StringVar(value=values[3])
        vehicle_types = ["SUV", "Sedan", "Hatchback", "Bike"]
        ttk.Combobox(form_frame, textvariable=type_var, values=vehicle_types, 
                    state="readonly", width=28).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Luggage Capacity:", bg="#f2f2f2").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        luggage_entry = ttk.Entry(form_frame, width=30)
        luggage_entry.insert(0, values[4])
        luggage_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Fuel Type:", bg="#f2f2f2").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        fuel_var = tk.StringVar(value=values[5])
        fuel_types = ["Petrol", "Diesel", "Electric"]
        ttk.Combobox(form_frame, textvariable=fuel_var, values=fuel_types, 
                    state="readonly", width=28).grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Price Per Day (₹):", bg="#f2f2f2").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        price_entry = ttk.Entry(form_frame, width=30)
        price_entry.insert(0, values[6])
        price_entry.grid(row=5, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Vehicle Number:", bg="#f2f2f2").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        number_entry = ttk.Entry(form_frame, width=30)
        number_entry.insert(0, values[7])
        number_entry.grid(row=6, column=1, padx=10, pady=5)
        
        # Error message label
        error_var = tk.StringVar()
        error_label = tk.Label(form_frame, textvariable=error_var, fg="red", bg="#f2f2f2")
        error_label.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Button frame
        button_frame = tk.Frame(edit_window, bg="#f2f2f2")
        button_frame.pack(pady=10)
        
        # Update function for the edit window
        def update_vehicle():
            # Validate inputs
            name = name_entry.get().strip()
            model = model_entry.get().strip()
            vehicle_type = type_var.get()
            luggage = luggage_entry.get().strip()
            fuel = fuel_var.get()
            price = price_entry.get().strip()
            number = number_entry.get().strip().upper()
            
            # Basic validation
            if not name or not model or not luggage or not price or not number:
                error_var.set("All fields are required!")
                return
                
            try:
                luggage_int = int(luggage)
                if luggage_int < 0:
                    error_var.set("Luggage capacity must be a positive number!")
                    return
            except ValueError:
                error_var.set("Luggage capacity must be a number!")
                return
                
            try:
                price_float = float(price)
                if price_float <= 0:
                    error_var.set("Price must be greater than zero!")
                    return
            except ValueError:
                error_var.set("Price must be a valid number!")
                return
            
            # Update in database
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    # Check if another vehicle already has this number
                    cursor.execute("SELECT id FROM vehicles WHERE vehicle_number = %s AND id != %s", 
                                 (number, vehicle_id))
                    if cursor.fetchone():
                        error_var.set(f"Vehicle number {number} is already in use!")
                        return
                    
                    # Update the vehicle
                    cursor.execute("""
                        UPDATE vehicles
                        SET name = %s, model = %s, type = %s, luggage_capacity = %s,
                            fuel_type = %s, price_per_day = %s, vehicle_number = %s
                        WHERE id = %s
                    """, (name, model, vehicle_type, luggage_int, fuel, price_float, number, vehicle_id))
                    
                    connection.commit()
                    messagebox.showinfo("Success", f"Vehicle {name} updated successfully!")
                    
                    # Close window and refresh vehicle list
                    edit_window.destroy()
                    self.load_vehicles()
                    
                except Exception as e:
                    connection.rollback()
                    error_var.set(f"Failed to update vehicle: {e}")
                finally:
                    cursor.close()
                    connection.close()
        
        # Add buttons
        ttk.Button(button_frame, text="Update", command=update_vehicle).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side=tk.LEFT, padx=10)
        
        # Make the window modal
        edit_window.transient(self.root)
        edit_window.grab_set()
        self.root.wait_window(edit_window)

    def delete_selected_vehicle(self):
        """Delete the selected vehicle after confirmation."""
        selected_item = self.vehicle_tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Select Vehicle", "Please select a vehicle to delete.")
            return
            
        # Get values of selected item
        values = self.vehicle_tree.item(selected_item[0], "values")
        
        if not values[0]:  # Handle the "No vehicles found" placeholder
            return
            
        vehicle_id = values[0]
        vehicle_name = values[1]
        vehicle_number = values[7]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm Deletion", 
                                 f"Are you sure you want to delete {vehicle_name} ({vehicle_number})?"):
            return
            
        # Check if vehicle is in use (has bookings)
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM bookings WHERE vehicle_id = %s", (vehicle_id,))
                booking_count = cursor.fetchone()[0]
                
                if booking_count > 0:
                    if not messagebox.askyesno("Warning", 
                                            f"This vehicle has {booking_count} bookings. Deleting it will also " 
                                            f"delete all associated bookings. Continue?"):
                        return
                    
                    # Delete associated bookings first
                    cursor.execute("DELETE FROM bookings WHERE vehicle_id = %s", (vehicle_id,))
                
                # Now delete the vehicle
                cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
                connection.commit()
                
                messagebox.showinfo("Success", f"Vehicle {vehicle_name} deleted successfully!")
                
                # Refresh vehicle list
                self.load_vehicles()
                
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Failed to delete vehicle: {e}")
            finally:
                cursor.close()
                connection.close()