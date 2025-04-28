# Hey there! This is our charging station finder app.
# It helps users find and book charging stations for their EVs.


import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import booking  # For handling station bookings
import json, os

# Database settings - keep these secure!
DB_CONFIG = {
    'host': "127.0.0.1",
    'user': "root",
    'password': "Shardul203",  # Remember to change in production!
    'database': "ev_station"
}

# Our app's color scheme - keeping it modern and clean
COLORS = {
    'primary': "#4CAF50",    # Nice green for main actions
    'secondary': "#2b2b2b",  # Dark theme background
    'accent': "#d77337",     # Orange pop for highlights
    'text_light': "#ffffff", # White text that pops
    'text_dark': "#333333",  # Easy to read dark text
    'warning': "#FFA500",    # Orange for warnings
    'error': "#FF0000",      # Red for errors
    'success': "#28a745",    # Green for success messages
    'card_bg': "#ffffff"     # Clean white backgrounds
}

# Font styles to keep everything looking consistent
STYLES = {
    'title': ('Arial', 24, 'bold'),    # Big headers
    'subtitle': ('Arial', 18),         # Section titles
    'button': ('Arial', 16),           # Nice clickable buttons
    'text': ('Arial', 14),             # Regular text
    'small_text': ('Arial', 12)        # Details and less important stuff
}

class SearchPage:
    def __init__(self, root, username=None, selected_vehicle=None):
        # Set up our main window and keep track of who's logged in
        self.root = root
        self.username = username
        self.selected_vehicle = selected_vehicle
        self.setup_window()
        self.load_user_vehicles()  # Get their vehicles for compatibility checking
        self.create_interface()

    def setup_window(self):
        # Make our window look nice and professional
        self.root.title("Find Charging Stations")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')  # Start maximized
        self.root.config(bg=COLORS['secondary'])

    def create_interface(self):
        # Build our UI piece by piece
        self.container = tk.Frame(self.root, bg=COLORS['secondary'])
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.create_header()        # Title and exit button
        self.create_search_section()  # Search bar
        self.create_results_section() # Where we'll show stations

    def execute_db_query(self, query, params=None):
        # Helper to run database queries safely
        try:
            with mysql.connector.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return []

    def load_user_vehicles(self):
        # Load the user's vehicles from our JSON file
        try:
            data_file = os.path.join(os.path.dirname(__file__), 'vehicles_data.json')
            with open(data_file, 'r') as f:
                data = json.load(f)
                self.user_vehicles = data.get('cars', []) + data.get('bikes', [])
        except Exception:
            self.user_vehicles = []  # Start fresh if something goes wrong

    def update_results(self, *args):
        # Clear out old results first
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Search for stations matching their query
        search_term = self.search_var.get()
        query = """
        SELECT s.name, s.charging_types, s.available_chargers, s.amenities, 
               st.state_name, s.operating_hours, s.rating, s.address
        FROM stations s
        JOIN states st ON s.state_id = st.state_id
        WHERE st.state_name LIKE %s 
        OR s.name LIKE %s 
        OR s.address LIKE %s
        """
        results = self.execute_db_query(query, (f"%{search_term}%",) * 3)

        # Show results or a "nothing found" message
        if not results:
            self.show_no_results()
        else:
            self.display_results(results)

    def display_results(self, results):
        # Create a scrollable area for our results
        canvas = tk.Canvas(self.results_frame, bg=COLORS['secondary'])
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['secondary'])

        # Wire up the scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a card for each station
        for station_data in results:
            self.create_station_card(scrollable_frame, station_data)

        # Pack everything together
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_header(self):
        """Creates the top bar with title and exit button"""
        header_frame = tk.Frame(self.container, bg=COLORS['secondary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Page title
        title = tk.Label(
            header_frame,
            text="Find Charging Stations",
            font=STYLES['title'],
            bg=COLORS['secondary'],
            fg=COLORS['text_light']
        )
        title.pack(side=tk.LEFT)

        # Exit button to go back
        exit_btn = tk.Button(
            header_frame,
            text="Exit",
            font=STYLES['button'],
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            command=self.exit_to_dashboard,
            padx=20,
            pady=10
        )
        exit_btn.pack(side=tk.RIGHT)

    def exit_to_dashboard(self):
        """Exit to dashboard"""
        self.root.destroy()

    def create_search_section(self):
        search_frame = tk.Frame(self.container, bg=COLORS['card_bg'], padx=20, pady=20)
        search_frame.pack(fill=tk.X, pady=(0, 20))

        # Search bar
        search_container = tk.Frame(search_frame, bg=COLORS['card_bg'])
        search_container.pack(fill=tk.X)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.update_results())

        tk.Label(
            search_container,
            text="Search Location:",
            font=STYLES['text'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(side=tk.LEFT, padx=(0, 10))

        search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=STYLES['text'],
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=5)

    def create_results_section(self):
        self.results_frame = tk.Frame(self.container, bg=COLORS['secondary'])
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initial search
        self.update_results()

    def show_no_results(self):
        no_results_frame = tk.Frame(self.results_frame, bg=COLORS['card_bg'], padx=20, pady=20)
        no_results_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            no_results_frame,
            text="No stations found",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack()

    def show_error(self, error_msg):
        error_frame = tk.Frame(self.results_frame, bg=COLORS['card_bg'], padx=20, pady=20)
        error_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            error_frame,
            text=f"Error: {error_msg}",
            font=STYLES['text'],
            bg=COLORS['card_bg'],
            fg=COLORS['error']
        ).pack()

    def create_station_card(self, parent, station_data):
        name, charging_types, available_chargers, amenities, location, hours, rating, address = station_data
        
        card = tk.Frame(
            parent,
            bg=COLORS['card_bg'],
            relief="raised",
            bd=1
        )
        card.pack(fill=tk.X, padx=20, pady=10)

        # Left side - Station info
        info_frame = tk.Frame(card, bg=COLORS['card_bg'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Station name with rating
        header_frame = tk.Frame(info_frame, bg=COLORS['card_bg'])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text=name,
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(side=tk.LEFT)

        if rating:
            tk.Label(
                header_frame,
                text=f"★ {rating:.1f}",
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['warning']
            ).pack(side=tk.LEFT, padx=10)

        # Location and address
        tk.Label(
            info_frame,
            text=f"📍 {location}",
            font=STYLES['text'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(anchor='w')

        if address:
            tk.Label(
                info_frame,
                text=address,
                font=STYLES['small_text'],
                bg=COLORS['card_bg'],
                fg=COLORS['text_dark']
            ).pack(anchor='w')

        # Details frame
        details_frame = tk.Frame(info_frame, bg=COLORS['card_bg'])
        details_frame.pack(fill=tk.X, pady=5)

        # Charging types with icon
        charging_types_list = charging_types.split(',') if charging_types else []
        tk.Label(
            details_frame,
            text=f"🔌 {', '.join(charging_types_list)}",
            font=STYLES['small_text'],
            bg=COLORS['card_bg']
        ).pack(anchor='w')

        # Available chargers with icon
        tk.Label(
            details_frame,
            text=f"⚡ {available_chargers} Chargers Available",
            font=STYLES['small_text'],
            bg=COLORS['card_bg']
        ).pack(anchor='w')

        # Operating hours with icon
        tk.Label(
            details_frame,
            text=f"🕒 {hours}",
            font=STYLES['small_text'],
            bg=COLORS['card_bg']
        ).pack(anchor='w')

        # Amenities with icons
        if amenities:
            amenities_frame = tk.Frame(info_frame, bg=COLORS['card_bg'])
            amenities_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                amenities_frame,
                text="🏪 Amenities:",
                font=STYLES['small_text'],
                bg=COLORS['card_bg']
            ).pack(anchor='w')
            
            amenities_list = amenities.split(',')
            for amenity in amenities_list:
                tk.Label(
                    amenities_frame,
                    text=f"• {amenity.strip()}",
                    font=STYLES['small_text'],
                    bg=COLORS['card_bg']
                ).pack(anchor='w', padx=(20, 0))

        # Right side - Book Now button
        btn_frame = tk.Frame(card, bg=COLORS['card_bg'])
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="Book Now",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=lambda: self.book_station(station_data),
            width=12
        ).pack(pady=5)

    def view_station_details(self, station_data):
        name, charging_types, available_chargers, amenities, location, hours, rating, address = station_data
        
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Station Details - {name}")
        details_window.geometry("600x500")
        details_window.config(bg=COLORS['card_bg'])

        # Main content frame
        content = tk.Frame(details_window, bg=COLORS['card_bg'], padx=30, pady=20)
        content.pack(fill=tk.BOTH, expand=True)

        # Header with name and rating
        header_frame = tk.Frame(content, bg=COLORS['card_bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            header_frame,
            text=name,
            font=STYLES['title'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(side=tk.LEFT)

        if rating:
            tk.Label(
                header_frame,
                text=f"★ {rating:.1f}",
                font=('Arial', 24),
                bg=COLORS['card_bg'],
                fg=COLORS['warning']
            ).pack(side=tk.LEFT, padx=15)

        # Details sections
        sections = [
            ("📍 Location", location),
            ("🏢 Address", address),
            ("🕒 Operating Hours", hours),
            ("⚡ Available Chargers", f"{available_chargers} units"),
            ("🔌 Charging Types", charging_types),
            ("🏪 Amenities", amenities.replace(',', '\n• ') if amenities else "None")
        ]

        for label, value in sections:
            section_frame = tk.Frame(content, bg=COLORS['card_bg'])
            section_frame.pack(fill=tk.X, pady=10)

            tk.Label(
                section_frame,
                text=label,
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['text_dark']
            ).pack(anchor='w')

            tk.Label(
                section_frame,
                text=value,
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['accent'],
                justify=tk.LEFT
            ).pack(anchor='w', padx=20)

        # Action buttons at bottom
        button_frame = tk.Frame(content, bg=COLORS['card_bg'])
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Book Now",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=lambda: self.book_station(station_data),
            width=15
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="Close",
            font=STYLES['button'],
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            command=details_window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=10)

    def book_station(self, station_data):
        if self.username is None:
            messagebox.showerror("Error", "Please log in to book a station")
            return
            
        booking_window = tk.Toplevel(self.root)
        booking.main(booking_window, station_data, self.username)

    def get_compatible_vehicles(self, station_name):
        try:
            # Get station charging types from database
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Shardul203",
                database="ev_station"
            )
            cursor = conn.cursor()
            
            # Assuming we have a stations table with charging_types column
            cursor.execute("SELECT charging_types FROM stations WHERE name = %s", (station_name,))
            result = cursor.fetchone()
            
            if result:
                station_types = result[0].split(',')
                return [
                    vehicle for vehicle in self.user_vehicles 
                    if vehicle['charging_type'] in station_types
                ]
            
            cursor.close()
            conn.close()
            
        except Exception:
            return []
        
        return []

    def rank_stations(self, stations):
        """Rank stations based on compatibility and history"""
        ranked_stations = []
        
        for station in stations:
            score = 0
            compatible_vehicles = self.get_compatible_vehicles(station['name'])
            
            # Add points for compatibility
            score += len(compatible_vehicles) * 10
            
            # Add points for successful charging history
            for vehicle in compatible_vehicles:
                history = vehicle.get('charging_history', [])
                successful_charges = sum(1 for h in history if h['station_name'] == station['name'])
                score += successful_charges * 5
            
            station['compatibility_score'] = score
            ranked_stations.append(station)
        
        # Sort by score
        return sorted(ranked_stations, key=lambda x: x['compatibility_score'], reverse=True)

# Update the main function to accept username
def main(root, username=None):
    # Fire up the search page!
    SearchPage(root, username)

if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()