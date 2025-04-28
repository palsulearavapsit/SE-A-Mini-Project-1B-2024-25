import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime

class AverageUsagePage:
    def __init__(self, root, on_back):
        """
        Initialize the Average Usage Page.
        
        Args:
            root: The parent Tkinter window/container
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.canvas = None  # To store the canvas reference
        self.create_widgets()

    def create_widgets(self):
        """
        Create and arrange all GUI widgets for the page.
        Includes title, controls, graph area, and statistics display.
        """
        # Main container
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title
        tk.Label(main_frame, text="Vehicle Usage Analytics", font=("Arial", 24, "bold"), 
                bg="#f2f2f2").pack(pady=10)
                
        # Controls Frame
        controls_frame = tk.Frame(main_frame, bg="#f2f2f2")
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Time period selection
        period_frame = tk.LabelFrame(controls_frame, text="Select Time Period", bg="#f2f2f2", padx=10, pady=5)
        period_frame.pack(side=tk.LEFT, padx=10)
        
        self.period_var = tk.StringVar(value="All Time")
        periods = ["All Time", "Last 30 Days", "Last 90 Days", "This Year"]
        ttk.Combobox(period_frame, textvariable=self.period_var, values=periods, 
                    state="readonly", width=15).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Graph type selection
        graph_frame = tk.LabelFrame(controls_frame, text="Graph Type", bg="#f2f2f2", padx=10, pady=5)
        graph_frame.pack(side=tk.LEFT, padx=10)
        
        self.graph_type_var = tk.StringVar(value="Average Duration")
        graph_types = ["Average Duration", "Total Bookings", "Revenue Generated"]
        ttk.Combobox(graph_frame, textvariable=self.graph_type_var, values=graph_types, 
                    state="readonly", width=15).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Vehicle type filter
        filter_frame = tk.LabelFrame(controls_frame, text="Filter by Vehicle Type", bg="#f2f2f2", padx=10, pady=5)
        filter_frame.pack(side=tk.LEFT, padx=10)
        
        self.filter_var = tk.StringVar(value="All Types")
        ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["All Types", "SUV", "Sedan", "Hatchback", "Bike"], 
                    state="readonly", width=10).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Generate button
        ttk.Button(controls_frame, text="Generate Report", command=self.show_average_usage_graph, 
                  style="TButton").pack(side=tk.LEFT, padx=20, pady=5)
        
        # Create a frame for the graph
        self.graph_frame = tk.Frame(main_frame, bg="white", height=400)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add a placeholder message
        self.placeholder = tk.Label(self.graph_frame, text="Click 'Generate Report' to view analytics", 
                                  bg="white", font=("Arial", 14))
        self.placeholder.pack(expand=True)
        
        # Results frame for detailed stats
        self.results_frame = tk.LabelFrame(main_frame, text="Statistics", bg="#f2f2f2", padx=10, pady=5)
        self.results_frame.pack(fill=tk.X, pady=5)
        
        # Create label for stats
        self.stats_label = tk.Label(self.results_frame, text="", bg="#f2f2f2", font=("Arial", 10),
                                  justify=tk.LEFT)
        self.stats_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f2f2f2")
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Back to Homepage", command=self.on_back).pack(pady=5)

    def clear_graph(self):
        """
        Clear the existing graph from the display.
        Removes all widgets from the graph frame and resets the canvas reference.
        """
        # Remove all widgets from graph frame
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Clear the reference to canvas if it exists
        if self.canvas:
            self.canvas = None

    def get_time_filter(self):
        """
        Generate SQL WHERE clause for time filtering based on selected period.
        
        Returns:
            str: SQL WHERE clause fragment for time filtering
        """
        period = self.period_var.get()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if period == "Last 30 Days":
            return f"AND b.check_in_date >= DATE_SUB('{today}', INTERVAL 30 DAY)"
        elif period == "Last 90 Days":
            return f"AND b.check_in_date >= DATE_SUB('{today}', INTERVAL 90 DAY)"
        elif period == "This Year":
            year = datetime.now().year
            return f"AND YEAR(b.check_in_date) = {year}"
        else:  # All Time
            return ""
            
    def get_vehicle_type_filter(self):
        """
        Generate SQL WHERE clause for vehicle type filtering.
        
        Returns:
            str: SQL WHERE clause fragment for vehicle type filtering
        """
        vehicle_type = self.filter_var.get()
        
        if vehicle_type != "All Types":
            return f"AND v.type = '{vehicle_type}'"
        return ""

    def show_average_usage_graph(self):
        """
        Generate and display the usage graph based on selected options.
        Handles data retrieval, graph generation, and statistics calculation.
        """
        self.clear_graph()
        
        graph_type = self.graph_type_var.get()
        time_filter = self.get_time_filter()
        vehicle_filter = self.get_vehicle_type_filter()
        period_label = self.period_var.get()
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Construct query based on selected graph type
                if graph_type == "Average Duration":
                    query = f"""
                        SELECT 
                            v.name, 
                            v.type, 
                            AVG(DATEDIFF(b.check_out_date, b.check_in_date)) AS avg_days,
                            COUNT(b.id) AS booking_count
                        FROM 
                            bookings b
                        JOIN 
                            vehicles v ON b.vehicle_id = v.id
                        WHERE 
                            1=1 {time_filter} {vehicle_filter}
                        GROUP BY 
                            v.name, v.type
                        HAVING 
                            COUNT(b.id) > 0
                        ORDER BY 
                            avg_days DESC
                        LIMIT 10
                    """
                    y_label = "Average Rental Duration (Days)"
                    title = f"Average Vehicle Rental Duration ({period_label})"
                    
                elif graph_type == "Total Bookings":
                    query = f"""
                        SELECT 
                            v.name, 
                            v.type, 
                            COUNT(b.id) AS booking_count
                        FROM 
                            bookings b
                        JOIN 
                            vehicles v ON b.vehicle_id = v.id
                        WHERE 
                            1=1 {time_filter} {vehicle_filter}
                        GROUP BY 
                            v.name, v.type
                        ORDER BY 
                            booking_count DESC
                        LIMIT 10
                    """
                    y_label = "Number of Bookings"
                    title = f"Total Bookings by Vehicle ({period_label})"
                    
                else:  # Revenue Generated
                    query = f"""
                        SELECT 
                            v.name, 
                            v.type, 
                            SUM(b.total_cost) AS total_revenue,
                            COUNT(b.id) AS booking_count
                        FROM 
                            bookings b
                        JOIN 
                            vehicles v ON b.vehicle_id = v.id
                        WHERE 
                            1=1 {time_filter} {vehicle_filter}
                        GROUP BY 
                            v.name, v.type
                        ORDER BY 
                            total_revenue DESC
                        LIMIT 10
                    """
                    y_label = "Total Revenue (₹)"
                    title = f"Revenue Generated by Vehicle ({period_label})"
                
                cursor.execute(query)
                results = cursor.fetchall()
                
                if not results:
                    # Show message if no data
                    tk.Label(self.graph_frame, text="No data available for the selected filters.", 
                           bg="white", font=("Arial", 14)).pack(expand=True)
                    self.stats_label.config(text="No statistics available.")
                    return
                
                # Extract data for plotting
                vehicle_names = [f"{row[0]}\n({row[1]})" for row in results]  # Include type in name
                
                if graph_type == "Average Duration":
                    values = [float(row[2]) if row[2] is not None else 0 for row in results]
                    booking_counts = [row[3] for row in results]
                    # Calculate statistics
                    stats = f"• Total vehicles analyzed: {len(results)}\n"
                    stats += f"• Average rental duration across all vehicles: {sum(values)/len(values):.2f} days\n"
                    stats += f"• Most frequently rented vehicle: {results[0][0]} ({booking_counts[0]} bookings)\n"
                    stats += f"• Vehicle with longest average rental: {results[0][0]} ({values[0]:.2f} days)"
                    
                elif graph_type == "Total Bookings":
                    values = [row[2] for row in results]
                    # Calculate statistics
                    total_bookings = sum(values)
                    stats = f"• Total bookings: {total_bookings}\n"
                    stats += f"• Total vehicles with bookings: {len(results)}\n"
                    stats += f"• Most booked vehicle: {results[0][0]} ({values[0]} bookings, {values[0]/total_bookings*100:.1f}% of total)\n"
                    stats += f"• Average bookings per vehicle: {total_bookings/len(results):.1f}"
                    
                else:  # Revenue
                    values = [float(row[2]) if row[2] is not None else 0 for row in results]
                    booking_counts = [row[3] for row in results]
                    # Calculate statistics
                    total_revenue = sum(values)
                    stats = f"• Total revenue: ₹{total_revenue:,.2f}\n"
                    stats += f"• Number of vehicles generating revenue: {len(results)}\n"
                    stats += f"• Highest revenue vehicle: {results[0][0]} (₹{values[0]:,.2f}, {values[0]/total_revenue*100:.1f}% of total)\n"
                    stats += f"• Average revenue per booking: ₹{total_revenue/sum(booking_counts):,.2f}"
                
                # Update stats display
                self.stats_label.config(text=stats)
                
                # Create color scheme based on vehicle type
                colors = []
                for row in results:
                    if row[1] == "SUV":
                        colors.append("#4CAF50")  # Green for SUV
                    elif row[1] == "Sedan":
                        colors.append("#2196F3")  # Blue for Sedan
                    elif row[1] == "Hatchback":
                        colors.append("#FFC107")  # Yellow for Hatchback
                    elif row[1] == "Bike":
                        colors.append("#F44336")  # Red for Bike
                    else:
                        colors.append("#9C27B0")  # Purple for others
                
                # Create the figure with adjusted size
                plt.figure(figsize=(10, 6))
                
                # Create bar chart with colors
                bars = plt.bar(range(len(vehicle_names)), values, color=colors)
                
                # Add data labels on top of bars
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    if graph_type == "Average Duration":
                        label_text = f"{height:.1f}"
                    elif graph_type == "Total Bookings":
                        label_text = f"{int(height)}"
                    else:  # Revenue
                        label_text = f"₹{int(height):,}"
                        
                    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                             label_text, ha='center', va='bottom', fontsize=8)
                
                # Set labels and title
                plt.xlabel("Vehicle Name (Type)")
                plt.ylabel(y_label)
                plt.title(title)
                
                # Set x-tick labels and rotate them for better readability
                plt.xticks(range(len(vehicle_names)), vehicle_names, rotation=45, ha='right')
                
                # Tight layout to ensure everything fits
                plt.tight_layout()
                
                # Add a legend for vehicle types
                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor="#4CAF50", label='SUV'),
                    Patch(facecolor="#2196F3", label='Sedan'),
                    Patch(facecolor="#FFC107", label='Hatchback'),
                    Patch(facecolor="#F44336", label='Bike')
                ]
                plt.legend(handles=legend_elements, loc='upper right')
                
                # Embed the graph into the Tkinter window
                self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.graph_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            except Exception as e:
                # Clear graph frame and show error
                self.clear_graph()
                error_label = tk.Label(self.graph_frame, text=f"Error generating graph: {str(e)}",
                                     fg="red", bg="white")
                error_label.pack(expand=True)
                print(f"Database error: {e}")  # For debugging
                self.stats_label.config(text="No statistics available due to error.")
            finally:
                cursor.close()
                connection.close()
        else:
            # Show connection error
            tk.Label(self.graph_frame, text="Could not connect to the database.",
                   fg="red", bg="white", font=("Arial", 14)).pack(expand=True)
            self.stats_label.config(text="Database connection failed.")