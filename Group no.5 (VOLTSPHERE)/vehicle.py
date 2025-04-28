# Hey! This is our vehicle management system where users can add and manage their EVs.
# We're using tkinter for the UI and storing vehicle data in JSON for persistence.


import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Button, Entry, StringVar, Toplevel, Text, Radiobutton
from PIL import Image, ImageTk  # We'll use this for vehicle images later
from datetime import datetime, timedelta
import mysql.connector  # For our database stuff
import json
import os
import matplotlib.pyplot as plt  # For those nice charging cost graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from calendar import monthcalendar, month_name
import sqlite3  # Might switch to SQLite later for better performance

# Our cool color scheme - keeping it modern and clean
COLORS = {
    'primary': "#4CAF50",    # Green for main actions
    'secondary': "#2b2b2b",  # Dark theme background
    'accent': "#d77337",     # Orange pop for highlights
    'text_light': "#ffffff", # White text for dark backgrounds
    'text_dark': "#333333",  # Dark text for light backgrounds
    'warning': "#FFA500",    # Yellow for warnings/alerts
    'error': "#FF0000",      # Red for delete/remove actions
    'success': "#28a745",    # Green for success messages
    'card_bg': "#ffffff"     # White for our vehicle cards
}

# Font styles to keep everything consistent
STYLES = {
    'title': ('Arial', 24, 'bold'),    # Big headers
    'subtitle': ('Arial', 18),         # Card titles
    'button': ('Arial', 16),           # Button text
    'text': ('Arial', 14),             # Regular text
    'small_text': ('Arial', 12)        # Small details
}

# Add these constants after your existing COLORS and STYLES
MAINTENANCE_TYPES = {
    'Regular Service': {
        'description': 'Regular maintenance check and service',
        'estimated_cost': 2000,
        'interval_days': 90
    },
    'Battery Check': {
        'description': 'Check battery health and performance',
        'estimated_cost': 1500,
        'interval_days': 180
    },
    'Tire Rotation': {
        'description': 'Rotate tires for even wear',
        'estimated_cost': 800,
        'interval_days': 120
    }
}

class VehicleSelectionPage:
    """
    This is our main vehicle management page where users can:
    - View all their registered vehicles
    - Add new cars or bikes
    - Edit vehicle details
    - Remove vehicles they no longer use
    """
    def __init__(self, root):
        # Basic window setup - making it fullscreen
        self.root = root
        self.root.title("Vehicle Management")
        
        # Make it responsive
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')
        self.root.resizable(True, True)
        
        # Keep track of our vehicles and their UI cards
        self.vehicle_cards = {}  # Maps vehicle names to their UI cards
        self.cars_data = []     # List of all cars
        self.bikes_data = []    # List of all bikes
        
        # Load any previously saved vehicles
        saved_data = self.load_vehicles_data()
        if saved_data:
            self.cars_data = saved_data.get('cars', [])
            self.bikes_data = saved_data.get('bikes', [])
        
        # Build our UI piece by piece
        self.create_container()
        self.create_header()
        self.create_tabs()

    def create_container(self):
        """Create main container for the page"""
        self.container = tk.Frame(self.root, bg=COLORS['secondary'])
        self.container.pack(fill=tk.BOTH, expand=True)

    def create_header(self):
        """Create header with title and buttons"""
        header_frame = tk.Frame(self.container, bg=COLORS['secondary'], height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)  # Maintain fixed height

        # Title
        title = tk.Label(
            header_frame,
            text="Vehicle Management",
            font=('Arial', 32, 'bold'),
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        title.pack(side=tk.LEFT, padx=40, pady=10)

        # Buttons frame
        buttons_frame = tk.Frame(header_frame, bg=COLORS['secondary'])
        buttons_frame.pack(side=tk.RIGHT, padx=40, pady=10)

        # Exit button
        exit_btn = tk.Button(
            buttons_frame,
            text="Exit",
            font=('Arial', 18),
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            command=self.exit_to_dashboard,
            padx=20,
            pady=10
        )
        exit_btn.pack(side=tk.RIGHT, padx=10)

        # Add Vehicle button
        add_btn = tk.Button(
            buttons_frame,
            text="+ Add New Vehicle",
            font=('Arial', 18),
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=self.show_add_vehicle_form,
            padx=20,
            pady=10
        )
        add_btn.pack(side=tk.RIGHT, padx=10)

    def exit_to_dashboard(self):
        """Exit to dashboard"""
        self.root.destroy()

    def create_vehicle_card(self, parent, vehicle):
        """Create a card widget for a vehicle with enhanced features"""
        card = Frame(parent, bg=COLORS['card_bg'], relief="raised", bd=1)
        card.pack(fill=tk.X, padx=10, pady=5)

        # Vehicle info frame
        info_frame = Frame(card, bg=COLORS['card_bg'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Vehicle name
        Label(
            info_frame,
            text=vehicle['name'],
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(anchor='w')

        # Vehicle details
        details_frame = Frame(info_frame, bg=COLORS['card_bg'])
        details_frame.pack(fill=tk.X, pady=5)

        # Show charging type
        Label(
            details_frame,
            text=f"Charging Type: {vehicle['charging_type']}",
            font=STYLES['text'],
            bg=COLORS['card_bg']
        ).pack(side=tk.LEFT, padx=5)

        # Show status
        Label(
            details_frame,
            text=f"Status: {vehicle['status']}",
            font=STYLES['text'],
            bg=COLORS['card_bg'],
            fg=COLORS['success'] if vehicle['status'] == 'Active' else COLORS['warning']
        ).pack(side=tk.LEFT, padx=5)

        # Buttons frame
        btn_frame = Frame(card, bg=COLORS['card_bg'])
        btn_frame.pack(side=tk.RIGHT, padx=10)

        # Add "Track Charging" button
        Button(
            btn_frame,
            text="Track Charging",
            font=STYLES['small_text'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=lambda: self.show_charging_form(vehicle)
        ).pack(side=tk.TOP, pady=2)

        # Add "Cost Summary" button
        Button(
            btn_frame,
            text="Cost Summary",
            font=STYLES['small_text'],
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            command=lambda: self.show_cost_summary(vehicle)
        ).pack(side=tk.TOP, pady=2)

        # Keep your existing buttons
        Button(
            btn_frame,
            text="Find Stations",
            font=STYLES['small_text'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=lambda: self.find_compatible_stations(vehicle)
        ).pack(side=tk.TOP, pady=2)

        # Edit button
        Button(
            btn_frame,
            text="Edit",
            font=STYLES['small_text'],
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            command=lambda: self.edit_vehicle(vehicle)
        ).pack(side=tk.TOP, pady=2)

        # Remove button
        Button(
            btn_frame,
            text="Remove",
            font=STYLES['small_text'],
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            command=lambda: self.remove_vehicle(vehicle)
        ).pack(side=tk.TOP, pady=2)

        # Store reference to card
        self.vehicle_cards[vehicle['name']] = card

    def edit_vehicle(self, vehicle):
        """Edit vehicle details"""
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Vehicle")
        edit_window.geometry("500x600")
        edit_window.config(bg=COLORS['card_bg'])

        # Safely split vehicle name into make and model
        name_parts = vehicle['name'].split() if vehicle.get('name') else ['', '']
        make = name_parts[0] if len(name_parts) > 0 else ''
        model = name_parts[1] if len(name_parts) > 1 else ''

        # Create entry fields
        entries = {}
        fields = [
            ("Make", make),
            ("Model", model),
            ("Charging Type", vehicle.get('charging_type', '')),
            ("Range", vehicle.get('range', '')),
            ("Status", vehicle.get('status', 'Active'))
        ]

        # Rest of the edit_vehicle method remains the same
        messagebox.showinfo("Info", "Edit functionality will be implemented soon")

    def remove_vehicle(self, vehicle):
        """Remove vehicle from list"""
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this vehicle?"):
            # Remove from data
            if vehicle['type'] == 'bike':
                self.bikes_data.remove(vehicle)
            else:
                self.cars_data.remove(vehicle)
            
            # Remove card from UI
            if vehicle['name'] in self.vehicle_cards:
                self.vehicle_cards[vehicle['name']].destroy()
                del self.vehicle_cards[vehicle['name']]
            
            # Save changes
            self.save_vehicles_data()
            messagebox.showinfo("Success", "Vehicle removed successfully")

    def create_tabs(self):
        """Create tabs for cars and bikes"""
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20)

        # Create tabs
        self.cars_tab = ttk.Frame(self.notebook)
        self.bikes_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.cars_tab, text='Cars')
        self.notebook.add(self.bikes_tab, text='Bikes')

        # Initialize vehicle lists
        self.create_vehicles_list(self.cars_tab, "car")
        self.create_vehicles_list(self.bikes_tab, "bike")

    def create_vehicles_list(self, parent, vehicle_type):
        # Get vehicles based on type
        vehicles = self.cars_data if vehicle_type == "car" else self.bikes_data

        # Create scrollable frame
        canvas = tk.Canvas(parent, bg=COLORS['card_bg'])  # Changed to use card_bg instead
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create vehicle cards
        for vehicle in vehicles:
            self.create_vehicle_card(scrollable_frame, vehicle)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_vehicle(self, entries, form_window):
        try:
            # Create new vehicle dictionary with charging compatibility
            new_vehicle = {
                'name': f"{entries['Make'].get()} {entries['Model'].get()}",
                'type': entries['Vehicle Type'].get().lower(),
                'charging_type': entries['Charging Type'].get(),
                'status': 'Active',
                'charging_history': [],
                'preferred_stations': []
            }

            # Add to appropriate list
            if new_vehicle['type'] == 'car':
                self.cars_data.append(new_vehicle)
            else:
                self.bikes_data.append(new_vehicle)
            
            # Save to file
            self.save_vehicles_data()
            
            # Refresh display
            self.refresh_vehicle_lists()
            
            messagebox.showinfo("Success", "Vehicle added successfully!")
            form_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add vehicle: {str(e)}")

    def get_max_power(self, charging_type):
        power_ratings = {
            'Type 2': 22,
            'CCS': 350,
            'CHAdeMO': 50
        }
        return power_ratings.get(charging_type, 0)

    def refresh_vehicle_lists(self):
        # Clear existing cards
        for widgets in self.cars_tab.winfo_children():
            widgets.destroy()
        for widgets in self.bikes_tab.winfo_children():
            widgets.destroy()
            
        # Recreate vehicle lists
        self.create_vehicles_list(self.cars_tab, "car")
        self.create_vehicles_list(self.bikes_tab, "bike")

    def save_vehicles_data(self):
        try:
            data = {
                "cars": self.cars_data,
                "bikes": self.bikes_data
            }
            
            data_file = os.path.join(os.path.dirname(__file__), 'vehicles_data.json')
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save vehicles data: {str(e)}")

    def load_vehicles_data(self):
        try:
            data_file = os.path.join(os.path.dirname(__file__), 'vehicles_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    return json.load(f)
            return None
                
        except Exception:
            return None

    def open_search_page(self):
        """Open the search page."""
        try:
            # Import the search module
            import search
            
            # Create a new window for search page
            search_window = tk.Toplevel(self.root)
            search.SearchPage(search_window)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open search page: {str(e)}")

    def show_add_vehicle_form(self):
        """Show form to add new vehicle"""
        form_window = Toplevel(self.root)
        form_window.title("Add New Vehicle")
        form_window.geometry("600x500")
        form_window.configure(bg=COLORS['card_bg'])

        # Form title
        Label(form_window, text="Add New Vehicle", font=STYLES['title'], bg=COLORS['card_bg'], fg=COLORS['text_dark']).pack(pady=20)

        # Form fields
        fields = [
            ("Vehicle Type", ["Car", "Bike"]),
            ("Make", None),
            ("Model", None),
            ("Registration Number", None),
            ("Charging Type", ["Type 1", "Type 2", "CCS", "CHAdeMO"]),
        ]

        entries = {}
        for field, options in fields:
            frame = Frame(form_window, bg=COLORS['card_bg'])
            frame.pack(fill=tk.X, padx=20, pady=5)

            Label(frame, text=field, font=STYLES['text'], bg=COLORS['card_bg'], fg=COLORS['text_dark']).pack(anchor='w')

            if options:
                var = StringVar(value=options[0])
                ttk.Combobox(frame, values=options, textvariable=var, state="readonly").pack(fill=tk.X, pady=5)
                entries[field] = var
            else:
                var = StringVar()
                Entry(frame, textvariable=var).pack(fill=tk.X, pady=5)
                entries[field] = var

        Button(
            form_window,
            text="Add Vehicle",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=lambda: self.add_vehicle(entries, form_window)
        ).pack(pady=20)

    def edit_vehicle(self, vehicle):
        """Edit vehicle details"""
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Vehicle")
        edit_window.geometry("600x500")
        edit_window.configure(bg=COLORS['card_bg'])

        Label(edit_window, text="Edit Vehicle", font=STYLES['title'], bg=COLORS['card_bg'], fg=COLORS['text_dark']).pack(pady=20)

        entries = {}
        
        # Vehicle Type (readonly)
        type_frame = Frame(edit_window, bg=COLORS['card_bg'])
        type_frame.pack(fill=tk.X, padx=20, pady=5)
        Label(type_frame, text="Vehicle Type", font=STYLES['text'], bg=COLORS['card_bg'], fg=COLORS['text_dark']).pack(anchor='w')
        type_var = StringVar(value=vehicle['type'].capitalize())
        type_entry = Entry(type_frame, textvariable=type_var, state='readonly')
        type_entry.pack(fill=tk.X, pady=5)
        entries['Vehicle Type'] = type_var

        # Other fields
        fields = [
            ("Make", vehicle['name'].split()[0]),
            ("Model", vehicle['name'].split()[1] if len(vehicle['name'].split()) > 1 else ""),
            ("Charging Type", vehicle['charging_type']),
            ("Status", ["Active", "Inactive"])
        ]

        for field, default in fields:
            frame = Frame(edit_window, bg=COLORS['card_bg'])
            frame.pack(fill=tk.X, padx=20, pady=5)
            Label(frame, text=field, font=STYLES['text'], bg=COLORS['card_bg'], fg=COLORS['text_dark']).pack(anchor='w')

            if isinstance(default, list):
                var = StringVar(value=vehicle.get('status', 'Active'))
                ttk.Combobox(frame, values=default, textvariable=var, state="readonly").pack(fill=tk.X, pady=5)
            else:
                var = StringVar(value=default)
                Entry(frame, textvariable=var).pack(fill=tk.X, pady=5)
            entries[field] = var

        def save_changes():
            # Update vehicle data
            vehicle['name'] = f"{entries['Make'].get()} {entries['Model'].get()}"
            vehicle['charging_type'] = entries['Charging Type'].get()
            vehicle['status'] = entries['Status'].get()
            
            # Save changes
            self.save_vehicles_data()
            self.refresh_vehicle_lists()
            edit_window.destroy()
            messagebox.showinfo("Success", "Vehicle updated successfully!")

        Button(
            edit_window,
            text="Save Changes",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=save_changes
        ).pack(pady=20)

    def update_charging_history(self, vehicle, station_data):
        """Update vehicle charging history after a charging session"""
        try:
            charging_session = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'station_name': station_data['name'],
                'duration': station_data['duration'],
                'cost': station_data['cost'],
                'energy_delivered': station_data['energy']
            }
            
            if 'charging_history' not in vehicle:
                vehicle['charging_history'] = []
            
            vehicle['charging_history'].append(charging_session)
            
            # Update statistics
            total_sessions = len(vehicle['charging_history'])
            vehicle['charging_stats'] = {
                'avg_duration': sum(s['duration'] for s in vehicle['charging_history']) / total_sessions,
                'avg_cost': sum(s['cost'] for s in vehicle['charging_history']) / total_sessions,
                'total_sessions': total_sessions
            }
            
            self.save_vehicles_data()
            
        except Exception as e:
            messagebox.showerror("Error", "Failed to update charging history")

    

    def find_compatible_stations(self, vehicle):
        """Open search page filtered by vehicle's charging type"""
        search_window = Toplevel(self.root)
        search_window.title(f"Recommended Stations - {vehicle['name']}")
        
        # Make window fullscreen
        screen_width = search_window.winfo_screenwidth()
        screen_height = search_window.winfo_screenheight()
        search_window.geometry(f"{screen_width}x{screen_height}")
        search_window.state('zoomed')  # This makes it fullscreen on Windows
        search_window.configure(bg=COLORS['card_bg'])
        
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Shardul203",
                database="ev_station"
            )
            cursor = conn.cursor()

            # Main container with padding
            main_container = tk.Frame(search_window, bg=COLORS['card_bg'], padx=30, pady=20)
            main_container.pack(fill=tk.BOTH, expand=True)

            query = """
            SELECT s.name, s.charging_types, s.available_chargers, s.amenities, 
                   st.state_name, s.operating_hours
            FROM stations s
            JOIN states st ON s.state_id = st.state_id
            WHERE s.charging_types LIKE %s
            AND s.available_chargers > 0
            ORDER BY s.rating DESC, s.available_chargers DESC
            LIMIT 2
            """
            cursor.execute(query, (f"%{vehicle['charging_type']}%",))
            results = cursor.fetchall()

            if results:
                # Title
                tk.Label(
                    main_container,
                    text=f"Recommended Charging Stations for {vehicle['name']}",
                    font=('Arial', 20, 'bold'),
                    bg=COLORS['card_bg'],
                    fg=COLORS['primary']
                ).pack(pady=(0, 20))

                # Vehicle info
                vehicle_info = tk.Frame(main_container, bg=COLORS['card_bg'])
                vehicle_info.pack(fill=tk.X, pady=(0, 20))

                tk.Label(
                    vehicle_info,
                    text=f"Vehicle Charging Type: {vehicle['charging_type']}",
                    font=STYLES['text'],
                    bg=COLORS['card_bg'],
                    fg=COLORS['text_dark']
                ).pack(anchor='w')

                # Create station cards
                for station_data in results:
                    card = tk.Frame(
                        main_container,
                        bg=COLORS['card_bg'],
                        relief="ridge",
                        bd=1
                    )
                    card.pack(fill=tk.X, pady=10)

                    # Station info
                    info_frame = tk.Frame(card, bg=COLORS['card_bg'])
                    info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

                    # Station name
                    tk.Label(
                        info_frame,
                        text=station_data[0],
                        font=STYLES['subtitle'],
                        bg=COLORS['card_bg'],
                        fg=COLORS['primary']
                    ).pack(anchor='w')

                    # Station details
                    details = f"""
Location: {station_data[4]}
Available Chargers: {station_data[2]}
Charging Types: {station_data[1]}
Operating Hours: {station_data[5]}
Amenities: {station_data[3]}"""

                    tk.Label(
                        info_frame,
                        text=details,
                        justify=tk.LEFT,
                        bg=COLORS['card_bg'],
                        fg=COLORS['text_dark'],
                        font=STYLES['text']
                    ).pack(anchor='w', pady=5)

                    # Button frame
                    btn_frame = tk.Frame(info_frame, bg=COLORS['card_bg'])
                    btn_frame.pack(fill=tk.X, pady=(10, 0))

                    # Book Now button
                    tk.Button(
                        btn_frame,
                        text="Book Now",
                        font=STYLES['button'],
                        bg=COLORS['primary'],
                        fg=COLORS['text_light'],
                        command=lambda s=station_data: self.book_station(s),
                        width=15
                    ).pack(side=tk.LEFT, padx=5)

            else:
                tk.Label(
                    search_window,
                    text=f"No compatible stations found for {vehicle['charging_type']} charging type",
                    font=STYLES['subtitle'],
                    bg=COLORS['card_bg'],
                    fg=COLORS['error']
                ).pack(pady=20)

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
            search_window.destroy()

    def book_station(self, station_data):
        # Let's handle the station booking process
        try:
            # First, make sure someone's logged in
            try:
                with open('current_user.txt', 'r') as f:
                    current_user = f.read().strip()
            except:
                messagebox.showinfo("Login Required", "Hey! You need to log in first to book a slot")
                return
                
            # Fire up the booking window
            from booking import BookingPage
            booking_window = Toplevel(self.root)
            booking_window.title("Station Booking")
            booking_window.geometry("800x600")
            
            # Hand it over to the booking page
            booking_page = BookingPage(booking_window, station_data[0], current_user)
            
        except Exception as e:
            messagebox.showerror("Error", f"Oops! Something went wrong: {str(e)}")

    def show_charging_form(self, vehicle):
        # Pop up a window to log a new charging session
        window = Toplevel(self.root)
        window.title("Add Charging Record")
        window.geometry("400x500")
        window.configure(bg=COLORS['card_bg'])

        # Set up our form with all the fields we need
        Label(window, text="Add Charging Record", font=STYLES['subtitle'], 
              bg=COLORS['card_bg']).pack(pady=10)

        fields = {}
        
        # Today's date is usually right, but they can change it
        Label(window, text="Date:", bg=COLORS['card_bg']).pack()
        fields['date'] = Entry(window)
        fields['date'].insert(0, datetime.now().strftime('%Y-%m-%d'))
        fields['date'].pack(pady=5)

        # Where did they charge?
        Label(window, text="Location:", bg=COLORS['card_bg']).pack()
        fields['location'] = ttk.Combobox(window, values=['Home', 'Public Station'])
        fields['location'].pack(pady=5)

        # How much juice did they use?
        Label(window, text="Units Consumed (kWh):", bg=COLORS['card_bg']).pack()
        fields['units'] = Entry(window)
        fields['units'].pack(pady=5)

        # And how much did it cost them?
        Label(window, text="Total Cost (₹):", bg=COLORS['card_bg']).pack()
        fields['cost'] = Entry(window)
        fields['cost'].pack(pady=5)

        def save_record():
            # Make sure everything's filled in right
            try:
                record = {
                    'date': fields['date'].get(),
                    'location': fields['location'].get(),
                    'units': float(fields['units'].get()),
                    'cost': float(fields['cost'].get())
                }
                
                # Create history list if it's their first charge
                if 'charging_history' not in vehicle:
                    vehicle['charging_history'] = []
                
                # Add the new record and save everything
                vehicle['charging_history'].append(record)
                self.save_vehicles_data()
                messagebox.showinfo("Success", "Got it! Your charging record is saved.")
                window.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Hmm... please check your numbers for units and cost")

        # Save button to finish up
        Button(window, text="Save Record", command=save_record,
               bg=COLORS['primary'], fg=COLORS['text_light']).pack(pady=20)


    def show_cost_summary(self, vehicle):
        # Let's show a nice summary of charging costs with some cool graphs
        window = Toplevel(self.root)
        window.title("Cost Summary")
        window.geometry("800x600")
        window.configure(bg=COLORS['card_bg'])

        # Nice big title at the top
        Label(window, text=f"Cost Summary - {vehicle['name']}", 
              font=STYLES['subtitle'], bg=COLORS['card_bg']).pack(pady=10)

        # Check if we have any charging data to show
        if not vehicle.get('charging_history'):
            Label(window, text="No charging history available yet!", 
                  bg=COLORS['card_bg']).pack(pady=20)
            return

        # Crunch some numbers for our summary
        total_cost = sum(record['cost'] for record in vehicle['charging_history'])
        total_units = sum(record['units'] for record in vehicle['charging_history'])
        avg_cost_per_unit = total_cost / total_units if total_units > 0 else 0

        # Show the key numbers in a nice format
        summary_frame = Frame(window, bg=COLORS['card_bg'])
        summary_frame.pack(fill=tk.X, padx=20, pady=10)

        summaries = [
            f"Total Spent: ₹{total_cost:.2f}",
            f"Total Units: {total_units:.2f} kWh",
            f"Average Cost per Unit: ₹{avg_cost_per_unit:.2f}/kWh"
        ]

        for summary in summaries:
            Label(summary_frame, text=summary, bg=COLORS['card_bg'],
                  font=STYLES['text']).pack(anchor='w')

        # Now for the cool part - let's make a graph!
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Get our data ready for plotting
        dates = [record['date'] for record in vehicle['charging_history']]
        costs = [record['cost'] for record in vehicle['charging_history']]
        
        # Make it look nice
        ax.plot(dates, costs, marker='o')
        ax.set_title('Your Charging Costs Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cost (₹)')
        plt.xticks(rotation=45)  # Angle the dates so they don't overlap
        
        # Add it to our window
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def show_maintenance_window(self, vehicle):
        # Pop up our maintenance tracking window
        window = tk.Toplevel(self.root)
        window.title("Maintenance Management")
        window.geometry("800x600")
        window.configure(bg=COLORS['card_bg'])

        # Make sure we have a place to store maintenance records
        if 'maintenance_history' not in vehicle:
            vehicle['maintenance_history'] = []
        if 'upcoming_maintenance' not in vehicle:
            vehicle['upcoming_maintenance'] = []

        # Create tabs to organize everything
        notebook = ttk.Notebook(window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Set up our three main views
        overview_tab = tk.Frame(notebook, bg=COLORS['card_bg'])
        history_tab = tk.Frame(notebook, bg=COLORS['card_bg'])
        schedule_tab = tk.Frame(notebook, bg=COLORS['card_bg'])

        notebook.add(overview_tab, text='Overview')
        notebook.add(history_tab, text='History')
        notebook.add(schedule_tab, text='Schedule')

        # Build our scheduling form
        schedule_frame = tk.Frame(schedule_tab, bg=COLORS['card_bg'])
        schedule_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Let them pick what kind of maintenance it is
        type_frame = tk.Frame(schedule_frame, bg=COLORS['card_bg'])
        type_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(type_frame, text="What type of maintenance?", bg=COLORS['card_bg']).pack(side=tk.LEFT)
        type_var = tk.StringVar(value=list(MAINTENANCE_TYPES.keys())[0])
        type_menu = ttk.Combobox(type_frame, textvariable=type_var, values=list(MAINTENANCE_TYPES.keys()))
        type_menu.pack(side=tk.LEFT, padx=10)

        # When do they want it done?
        date_frame = tk.Frame(schedule_frame, bg=COLORS['card_bg'])
        date_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(date_frame, text="When's it due?", bg=COLORS['card_bg']).pack(side=tk.LEFT)
        date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        date_entry = tk.Entry(date_frame, textvariable=date_var)
        date_entry.pack(side=tk.LEFT, padx=10)

        # How urgent is it?
        priority_frame = tk.Frame(schedule_frame, bg=COLORS['card_bg'])
        priority_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(priority_frame, text="How urgent is it?", bg=COLORS['card_bg']).pack(side=tk.LEFT)
        priority_var = tk.StringVar(value="Medium")
        
        for priority in ["Low", "Medium", "High"]:
            tk.Radiobutton(priority_frame, text=priority, variable=priority_var,
                          value=priority, bg=COLORS['card_bg']).pack(side=tk.LEFT, padx=10)

        # Any extra notes?
        notes_frame = tk.Frame(schedule_frame, bg=COLORS['card_bg'])
        notes_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(notes_frame, text="Any notes to add?", bg=COLORS['card_bg']).pack(anchor='w')
        notes_text = tk.Text(notes_frame, height=4, width=40)
        notes_text.pack(fill=tk.X, pady=5)

        def save_maintenance():
            # Save all the maintenance details
            try:
                new_maintenance = {
                    'type': type_var.get(),
                    'due_date': date_var.get(),
                    'priority': priority_var.get(),
                    'notes': notes_text.get('1.0', tk.END).strip(),
                    'status': 'Scheduled'
                }
                
                vehicle['upcoming_maintenance'].append(new_maintenance)
                self.save_vehicles_data()
                messagebox.showinfo("Success", "Got it! Maintenance is scheduled.")
                self.refresh_maintenance_view(overview_tab, vehicle)
                
            except Exception as e:
                messagebox.showerror("Error", f"Oops! Something went wrong: {str(e)}")

        # Add our save button
        tk.Button(schedule_frame, text="Schedule It!", 
                  command=save_maintenance,
                  bg=COLORS['primary'], 
                  fg=COLORS['text_light']).pack(pady=20)

        # Update the overview to show the latest info
        self.refresh_maintenance_view(overview_tab, vehicle)

# Fire up the app when we run this file directly
if __name__ == "__main__":
    run_vehicle_selection_page()

   