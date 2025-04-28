import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from decimal import Decimal
from booking import RentVehiclePage, BookedVehicleDetailsPage, CancelBookingsPage
from feedback import FeedbackPage

class DashboardPage:
    def __init__(self, root, username="Guest", role="user"):
        """
        Initialize the Dashboard page.
        
        Args:
            root: The parent Tkinter window/container
            username: The logged in username (default "Guest")
            role: The user's role ("admin" or "user", default "user")
        """
        self.root = root
        self.username = username
        self.role = role
        self.chart_widgets = []  # Track matplotlib widgets for proper cleanup
        
        # Clear any existing widgets in the root
        self.clear_root()
        
        # Create dashboard widgets
        self.create_widgets()

    def clear_root(self):
        """
        Clear all existing widgets in the root frame.
        Special handling for matplotlib canvas widgets.
        """
        for widget in self.root.winfo_children():
            if hasattr(widget, 'get_tk_widget'):  # For matplotlib canvases
                widget.get_tk_widget().destroy()
            widget.destroy()
            
    def create_widgets(self):
        """
        Create the main dashboard layout with title and role-specific content.
        """
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title with role indicator
        if self.role == "admin":
            title = "Admin Dashboard"
        else:
            title = "User Dashboard"
            
        # Title frame with colored background
        title_frame = tk.Frame(main_frame, bg="#4CAF50", height=60)
        title_frame.pack(fill=tk.X, pady=5)
        tk.Label(title_frame, 
                text=title, 
                font=("Arial", 20, "bold"), 
                fg="white", 
                bg="#4CAF50").pack(pady=10)
        
        # Welcome message with current date/time
        welcome_frame = tk.Frame(main_frame, bg="#f2f2f2")
        welcome_frame.pack(fill=tk.X, pady=10)
        
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        welcome_text = f"Welcome back, {self.username}! Today is {current_time}"
        tk.Label(welcome_frame, 
                text=welcome_text, 
                font=("Arial", 12), 
                bg="#f2f2f2").pack(anchor=tk.W, pady=5)
        
        # Display different content based on role
        if self.role == "admin":
            self.create_admin_dashboard(main_frame)
        else:
            self.create_user_dashboard(main_frame)

    def create_admin_dashboard(self, parent):
        """
        Create dashboard for admin users with full metrics and analytics.
        
        Args:
            parent: The parent frame to contain the admin dashboard
        """
        # Admin info text
        info_frame = tk.Frame(parent, bg="#f2f2f2")
        info_frame.pack(fill=tk.X, pady=5)
        
        info_text = "Admin dashboard provides a complete overview of the car rental system."
        tk.Label(info_frame, 
                text=info_text, 
                font=("Arial", 10, "italic"), 
                fg="gray", 
                bg="#f2f2f2").pack(anchor=tk.W)
        
        # Key metrics row - shows important statistics
        metrics_frame = tk.Frame(parent, bg="#f2f2f2")
        metrics_frame.pack(fill=tk.X, pady=10)
        
        # Collect metrics data from database
        total_customers = self.get_total_customers()
        total_vehicles = self.get_total_vehicles()
        total_bookings = self.get_total_bookings()
        total_revenue = self.get_total_revenue()
        
        # Create metric cards with different colors
        metrics = [
            ("Total Customers", f"{total_customers}", "#2196F3"),  # Blue
            ("Available Vehicles", f"{total_vehicles}", "#4CAF50"),  # Green
            ("Total Bookings", f"{total_bookings}", "#FFC107"),  # Yellow
            ("Revenue Generated", f"₹{total_revenue:,.2f}", "#F44336"),  # Red
        ]
        
        # Create and position each metric card
        for i, (label, value, color) in enumerate(metrics):
            # Create a card-like frame for each metric
            card = tk.Frame(metrics_frame, 
                           bg="white", 
                           relief=tk.RAISED, 
                           bd=1)
            card.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            
            # Add a colored header strip
            header = tk.Frame(card, bg=color, height=5)
            header.pack(fill=tk.X)
            
            # Add metric content (label and value)
            tk.Label(card, 
                    text=label, 
                    font=("Arial", 12), 
                    bg="white").pack(pady=(15,5))
            tk.Label(card, 
                    text=value, 
                    font=("Arial", 18, "bold"), 
                    bg="white").pack(pady=(5,15))
            
        # Configure grid to expand cards evenly
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)
        
        # Recent activity section - shows latest bookings
        activity_frame = tk.LabelFrame(parent, 
                                     text="Recent Bookings", 
                                     bg="#f2f2f2", 
                                     padx=10, pady=10)
        activity_frame.pack(fill=tk.X, pady=10)
        
        # Create a treeview to display recent bookings
        columns = ("ID", "Customer", "Vehicle", "Check-in", "Check-out", "Amount")
        bookings_tree = ttk.Treeview(activity_frame, 
                                   columns=columns, 
                                   show="headings", 
                                   height=5)
        
        # Configure column widths and alignment
        bookings_tree.column("ID", width=50, anchor=tk.CENTER)
        bookings_tree.column("Customer", width=150)
        bookings_tree.column("Vehicle", width=150)
        bookings_tree.column("Check-in", width=100, anchor=tk.CENTER)
        bookings_tree.column("Check-out", width=100, anchor=tk.CENTER)
        bookings_tree.column("Amount", width=100, anchor=tk.E)
        
        # Set column headings
        bookings_tree.heading("ID", text="ID")
        bookings_tree.heading("Customer", text="Customer")
        bookings_tree.heading("Vehicle", text="Vehicle")
        bookings_tree.heading("Check-in", text="Check-in")
        bookings_tree.heading("Check-out", text="Check-out")
        bookings_tree.heading("Amount", text="Amount")
        
        # Add scrollbar for the treeview
        scrollbar = ttk.Scrollbar(activity_frame, 
                                orient=tk.VERTICAL, 
                                command=bookings_tree.yview)
        bookings_tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        bookings_tree.pack(fill=tk.X, expand=True)
        
        # Load recent bookings data into the treeview
        self.load_recent_bookings(bookings_tree)
        
        # Charts section - contains data visualizations
        charts_frame = tk.Frame(parent, bg="#f2f2f2")
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create left chart frame for vehicle usage
        left_chart_frame = tk.LabelFrame(charts_frame, 
                                       text="Vehicle Usage", 
                                       bg="#f2f2f2", 
                                       padx=10, pady=10)
        left_chart_frame.pack(side=tk.LEFT, 
                            fill=tk.BOTH, 
                            expand=True, 
                            padx=(0,5))
        
        # Create right chart frame for vehicle types
        right_chart_frame = tk.LabelFrame(charts_frame, 
                                        text="Vehicle Types", 
                                        bg="#f2f2f2", 
                                        padx=10, pady=10)
        right_chart_frame.pack(side=tk.RIGHT, 
                             fill=tk.BOTH, 
                             expand=True, 
                             padx=(5,0))
        
        # Plot the charts
        self.plot_vehicle_usage(left_chart_frame)
        self.plot_vehicle_type_distribution(right_chart_frame)

    def create_user_dashboard(self, parent):
        """
        Create dashboard for regular users with personalized info.
        
        Args:
            parent: The parent frame to contain the user dashboard
        """
        # User welcome section
        welcome_frame = tk.Frame(parent, bg="#f2f2f2")
        welcome_frame.pack(fill=tk.X, pady=5)
        
        info_text = f"Welcome to your personalized dashboard. Here you can see your rental activity and available vehicles."
        tk.Label(welcome_frame, 
                text=info_text, 
                font=("Arial", 10, "italic"), 
                fg="gray", 
                bg="#f2f2f2").pack(anchor=tk.W)
                
        # Quick actions card - provides navigation shortcuts
        actions_frame = tk.LabelFrame(parent, 
                                    text="Quick Actions", 
                                    bg="#f2f2f2", 
                                    padx=10, pady=10)
        actions_frame.pack(fill=tk.X, pady=10)
        
        # Add action buttons
        ttk.Button(actions_frame, 
                  text="Rent a Vehicle", 
                  command=self.open_rent_vehicle).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(actions_frame, 
                  text="My Bookings", 
                  command=self.open_my_bookings).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(actions_frame, 
                  text="Submit Feedback", 
                  command=self.open_feedback).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Popular vehicles section - shows most booked vehicles
        popular_frame = tk.LabelFrame(parent, 
                                    text="Popular Vehicles", 
                                    bg="#f2f2f2", 
                                    padx=10, pady=10)
        popular_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a treeview to display popular vehicles
        columns = ("Name", "Type", "Fuel", "Price", "Available")
        vehicles_tree = ttk.Treeview(popular_frame, 
                                   columns=columns, 
                                   show="headings", 
                                   height=6)
        
        # Configure column widths and alignment
        vehicles_tree.column("Name", width=150)
        vehicles_tree.column("Type", width=100, anchor=tk.CENTER)
        vehicles_tree.column("Fuel", width=100, anchor=tk.CENTER)
        vehicles_tree.column("Price", width=100, anchor=tk.E)
        vehicles_tree.column("Available", width=100, anchor=tk.CENTER)
        
        # Set column headings
        vehicles_tree.heading("Name", text="Vehicle Name")
        vehicles_tree.heading("Type", text="Type")
        vehicles_tree.heading("Fuel", text="Fuel Type")
        vehicles_tree.heading("Price", text="Price/Day")
        vehicles_tree.heading("Available", text="Available")
        
        # Add scrollbar for the treeview
        scrollbar = ttk.Scrollbar(popular_frame, 
                                orient=tk.VERTICAL, 
                                command=vehicles_tree.yview)
        vehicles_tree.configure(yscroll=scrollbar.set)
        
        # Pack tree and scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        vehicles_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load popular vehicles data into the treeview
        self.load_popular_vehicles(vehicles_tree)
        
        # Upcoming bookings section (placeholder)
        upcoming_frame = tk.LabelFrame(parent, 
                                     text="Your Upcoming Rentals", 
                                     bg="#f2f2f2", 
                                     padx=10, pady=10)
        upcoming_frame.pack(fill=tk.X, pady=10)
        
        # Placeholder text (would show actual bookings in a real implementation)
        placeholder_text = "You have no upcoming bookings. Click 'Rent a Vehicle' to make a reservation!"
        tk.Label(upcoming_frame, 
               text=placeholder_text, 
               padx=10, pady=20,
               bg="white", 
               fg="#555").pack(fill=tk.X)
    
    def open_rent_vehicle(self):
        """Open the Rent Vehicle page and clear current dashboard."""
        self.clear_root()
        RentVehiclePage(
            root=self.root,
            on_back=lambda: DashboardPage(self.root, self.username, self.role)
        )
    
    def open_my_bookings(self):
        """Open the My Bookings page and clear current dashboard."""
        self.clear_root()
        BookedVehicleDetailsPage(
            root=self.root,
            on_back=lambda: DashboardPage(self.root, self.username, self.role)
        )
    
    def open_feedback(self):
        """Open the Feedback page and clear current dashboard."""
        self.clear_root()
        FeedbackPage(
            root=self.root,
            on_back=lambda: DashboardPage(self.root, self.username, self.role)
        )

    # Database functions
    def get_total_customers(self):
        """Get the total number of registered customers from database."""
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM customers")
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error fetching total customers: {e}")
                return 0
            finally:
                cursor.close()
                connection.close()
        return 0

    def get_total_vehicles(self):
        """Get the total number of registered vehicles from database."""
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM vehicles")
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error fetching total vehicles: {e}")
                return 0
            finally:
                cursor.close()
                connection.close()
        return 0

    def get_total_bookings(self):
        """Get the total number of bookings from database."""
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM bookings")
                return cursor.fetchone()[0]
            except Exception as e:
                print(f"Error fetching total bookings: {e}")
                return 0
            finally:
                cursor.close()
                connection.close()
        return 0

    def get_total_revenue(self):
        """Get the total revenue from all bookings in database."""
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT SUM(total_cost) FROM bookings")
                revenue = cursor.fetchone()[0]
                # Explicitly convert Decimal to float safely
                return float(revenue) if revenue is not None else 0.0
            except Exception as e:
                print(f"Error fetching total revenue: {e}")
                return 0.0
            finally:
                cursor.close()
                connection.close()
        return 0.0

    def load_recent_bookings(self, tree_widget):
        """
        Load recent bookings into the provided treeview.
        
        Args:
            tree_widget: The Treeview widget to populate with booking data
        """
        # Clear existing items
        for item in tree_widget.get_children():
            tree_widget.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Query to get recent bookings with customer and vehicle details
                query = """
                    SELECT 
                        b.id, 
                        c.name AS customer_name, 
                        v.name AS vehicle_name, 
                        DATE_FORMAT(b.check_in_date, '%Y-%m-%d') AS check_in, 
                        DATE_FORMAT(b.check_out_date, '%Y-%m-%d') AS check_out, 
                        b.total_cost
                    FROM 
                        bookings b
                    JOIN 
                        customers c ON b.customer_id = c.id
                    JOIN 
                        vehicles v ON b.vehicle_id = v.id
                    ORDER BY 
                        b.id DESC
                    LIMIT 10
                """
                cursor.execute(query)
                bookings = cursor.fetchall()
                
                if bookings:
                    for booking in bookings:
                        # Format the amount as currency
                        amount = f"₹{booking[5]:.2f}" if booking[5] else "₹0.00"
                        
                        # Insert booking into treeview
                        tree_widget.insert("", tk.END, values=(
                            booking[0],  # ID
                            booking[1],  # Customer name
                            booking[2],  # Vehicle name
                            booking[3],  # Check-in date
                            booking[4],  # Check-out date
                            amount       # Total cost
                        ))
                else:
                    tree_widget.insert("", tk.END, 
                                     values=("", "No recent bookings found", "", "", "", ""))
                    
            except Exception as e:
                print(f"Error loading recent bookings: {e}")
                tree_widget.insert("", tk.END, 
                                 values=("", f"Error loading data: {e}", "", "", "", ""))
            finally:
                cursor.close()
                connection.close()

    def load_popular_vehicles(self, tree_widget):
        """
        Load popular (most booked) vehicles into the provided treeview.
        
        Args:
            tree_widget: The Treeview widget to populate with vehicle data
        """
        # Clear existing items
        for item in tree_widget.get_children():
            tree_widget.delete(item)
            
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Query to get vehicles ordered by booking frequency
                query = """
                    SELECT 
                        v.name, 
                        v.type, 
                        v.fuel_type,
                        v.price_per_day,
                        CASE
                            WHEN EXISTS (
                                SELECT 1 FROM bookings b 
                                WHERE b.vehicle_id = v.id 
                                AND CURRENT_DATE BETWEEN b.check_in_date AND b.check_out_date
                            ) THEN 'No'
                            ELSE 'Yes'
                        END AS available
                    FROM 
                        vehicles v
                    LEFT JOIN 
                        bookings b ON v.id = b.vehicle_id
                    GROUP BY 
                        v.id
                    ORDER BY 
                        COUNT(b.id) DESC
                    LIMIT 6
                """
                cursor.execute(query)
                vehicles = cursor.fetchall()
                
                if vehicles:
                    for vehicle in vehicles:
                        # Format price as currency
                        price = f"₹{vehicle[3]:.2f}" if vehicle[3] else "₹0.00"
                        
                        # Insert vehicle into treeview
                        tree_widget.insert("", tk.END, values=(
                            vehicle[0],  # Name
                            vehicle[1],  # Type
                            vehicle[2],  # Fuel type
                            price,       # Price per day
                            vehicle[4]   # Availability
                        ))
                else:
                    tree_widget.insert("", tk.END, 
                                     values=("No vehicles found", "", "", "", ""))
                    
            except Exception as e:
                print(f"Error loading popular vehicles: {e}")
                tree_widget.insert("", tk.END, 
                                 values=(f"Error loading data: {e}", "", "", "", ""))
            finally:
                cursor.close()
                connection.close()

    def plot_vehicle_usage(self, parent_frame):
        """
        Plot vehicle usage chart (bookings per vehicle) in the specified frame.
        
        Args:
            parent_frame: The frame to contain the vehicle usage chart
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT v.name, COUNT(b.id) AS booking_count
                    FROM vehicles v
                    LEFT JOIN bookings b ON v.id = b.vehicle_id
                    GROUP BY v.name
                    ORDER BY booking_count DESC
                    LIMIT 10
                """)
                results = cursor.fetchall()

                if results:
                    # Extract data for plotting
                    vehicle_names = [row[0][:10] + "..." if len(row[0]) > 10 else row[0] for row in results]
                    booking_counts = [row[1] for row in results]

                    # Set up the plot
                    fig = Figure(figsize=(5, 4), dpi=100)
                    ax = fig.add_subplot(111)
                    
                    # Create horizontal bar chart (easier to read with long names)
                    bars = ax.barh(vehicle_names, booking_counts, color='#4CAF50')
                    
                    # Add data labels
                    for i, bar in enumerate(bars):
                        width = bar.get_width()
                        ax.text(width + 0.1, 
                               bar.get_y() + bar.get_height()/2,
                               str(booking_counts[i]), 
                               ha='left', 
                               va='center')
                    
                    ax.set_title("Most Booked Vehicles")
                    ax.set_xlabel("Number of Bookings")
                    
                    # Add a grid
                    ax.grid(axis='x', linestyle='--', alpha=0.6)
                    
                    # Tight layout to ensure everything fits
                    fig.tight_layout()

                    # Create canvas for embedding
                    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
                    canvas.draw()
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(fill=tk.BOTH, expand=True)
                    
                    # Store the canvas so we can destroy it properly later
                    self.chart_widgets.append(canvas)
                else:
                    # Show message if no data
                    tk.Label(parent_frame, 
                           text="No booking data available", 
                           fg="gray", 
                           bg="#f2f2f2", 
                           font=("Arial", 12)).pack(pady=30)
                    
            except Exception as e:
                print(f"Error plotting vehicle usage: {e}")
                tk.Label(parent_frame, 
                       text=f"Error creating chart: {e}", 
                       fg="red", 
                       bg="#f2f2f2").pack(pady=30)
            finally:
                cursor.close()
                connection.close()
        else:
            # Show message if connection failed
            tk.Label(parent_frame, 
                   text="Database connection failed", 
                   fg="red", 
                   bg="#f2f2f2").pack(pady=30)

    def plot_vehicle_type_distribution(self, parent_frame):
        """
        Plot pie chart of vehicle type distribution in the specified frame.
        
        Args:
            parent_frame: The frame to contain the vehicle type chart
        """
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT type, COUNT(*) AS count
                    FROM vehicles
                    GROUP BY type
                """)
                results = cursor.fetchall()

                if results:
                    # Extract data for plotting
                    vehicle_types = [row[0] for row in results]
                    counts = [row[1] for row in results]
                    
                    # Custom colors for different vehicle types
                    colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336']
                    
                    # Create pie chart
                    fig = Figure(figsize=(5, 4), dpi=100)
                    ax = fig.add_subplot(111)
                    
                    # Draw pie chart with slight explosion effect
                    wedges, texts, autotexts = ax.pie(
                        counts, 
                        labels=vehicle_types, 
                        autopct='%1.1f%%', 
                        startangle=90,
                        colors=colors[:len(vehicle_types)],
                        explode=[0.05] * len(vehicle_types)  # Slightly explode all slices
                    )
                    
                    # Enhance text properties
                    for text in texts:
                        text.set_fontsize(10)
                        text.set_fontweight('bold')
                    
                    for autotext in autotexts:
                        autotext.set_fontsize(8)
                        autotext.set_color('white')
                        
                    ax.set_title("Vehicle Fleet Composition")
                    ax.axis('equal')  # Equal aspect ratio ensures circular pie
                    
                    # Tight layout to ensure everything fits
                    fig.tight_layout()

                    # Create canvas for embedding
                    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
                    canvas.draw()
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.pack(fill=tk.BOTH, expand=True)
                    
                    # Store the canvas so we can destroy it properly later
                    self.chart_widgets.append(canvas)
                else:
                    # Show message if no data
                    tk.Label(parent_frame, 
                           text="No vehicle data available", 
                           fg="gray", 
                           bg="#f2f2f2", 
                           font=("Arial", 12)).pack(pady=30)
                    
            except Exception as e:
                print(f"Error plotting vehicle type distribution: {e}")
                tk.Label(parent_frame, 
                       text=f"Error creating chart: {e}", 
                       fg="red", 
                       bg="#f2f2f2").pack(pady=30)
            finally:
                cursor.close()
                connection.close()
        else:
            # Show message if connection failed
            tk.Label(parent_frame, 
                   text="Database connection failed", 
                   fg="red", 
                   bg="#f2f2f2").pack(pady=30)

    def __del__(self):
        """Destructor to clean up properly when the dashboard is removed."""
        self.cleanup()
        
    def cleanup(self):
        """Clean up matplotlib resources to prevent memory leaks."""
        for chart in self.chart_widgets:
            if chart and hasattr(chart, 'get_tk_widget'):
                chart.get_tk_widget().destroy()