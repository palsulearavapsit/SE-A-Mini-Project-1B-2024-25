# Hey! This is our main dashboard for the EV Charging Station app.
# It's where users can manage their vehicles, find charging stations, and more.


import tkinter as tk
from tkinter import messagebox, ttk
import search, vehicle, booking, user_profile  # Our other pages
from datetime import datetime
import json, os

# Our app's look and feel - keeping it clean and modern
COLORS = {
    'primary': "#4CAF50",    # Nice green for main actions
    'secondary': "#2b2b2b",  # Dark theme background
    'accent': "#d77337",     # Orange pop for highlights
    'text_light': "#ffffff", # White text that stands out
    'text_dark': "#333333",  # Easy to read dark text
    'warning': "#FFA500",    # Yellow for heads-up messages
    'error': "#FF0000",      # Red for serious stuff
    'success': "#28a745",    # Green for good news
    'card_bg': "#ffffff",    # Clean white for our cards
    'border': "#E0E0E0",     # Subtle borders
    'hover': "#81C784"       # Soft green for hover effects
}

# Font styles - keeping everything consistent
STYLES = {
    'title': ('Arial', 24, 'bold'),    # Big headers that grab attention
    'subtitle': ('Arial', 18),         # For section titles
    'button': ('Arial', 16),           # Nice readable button text
    'text': ('Arial', 14),             # Regular text size
    'small_text': ('Arial', 12),       # For less important details
    'welcome': ('Arial', 16)           # Friendly welcome message
}

class MainPage:
    def __init__(self, root):
        # Setting up our main window - making it look nice and professional
        self.root = root
        self.root.title("EV Charging Station Dashboard")
        
        # Make it fullscreen and responsive
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')
        self.root.config(bg=COLORS['secondary'])
        
        self.username = None  # We'll get this when someone logs in

        # Add scrolling for smaller screens
        self.setup_scrollable_area()
        
        # Build our dashboard piece by piece
        self.create_header()
        self.create_welcome_section()
        self.setup_content_area()
        self.create_dashboard_cards()

    def setup_scrollable_area(self):
        # Making sure everything fits nicely on any screen size
        self.main_canvas = tk.Canvas(self.root, bg=COLORS['secondary'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg=COLORS['secondary'])
        
        # Wire up the scrolling
        self.scrollable_frame.bind("<Configure>", 
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack it all together
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Make the mousewheel work for scrolling
        self.main_canvas.bind_all("<MouseWheel>", 
            lambda e: self.main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def create_header(self):
        # Nice clean header with logo and logout button
        header_frame = tk.Frame(self.scrollable_frame, bg=COLORS['secondary'], height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add our app title with a cool lightning bolt icon
        title_frame = tk.Frame(header_frame, bg=COLORS['secondary'])
        title_frame.pack(side=tk.LEFT, padx=40)
        
        tk.Label(title_frame, text="⚡", font=('Arial', 40),
                bg=COLORS['secondary'], fg=COLORS['text_light']).pack(side=tk.LEFT)
        tk.Label(title_frame, text="EV Charging Station", font=STYLES['title'],
                bg=COLORS['secondary'], fg=COLORS['text_light']).pack(side=tk.LEFT)

        # Add a logout button that changes color on hover
        logout_btn = tk.Button(header_frame, text="Logout", command=self.logout,
                             **self.get_button_style(color='accent'))
        logout_btn.pack(side=tk.RIGHT, padx=40)
        
        # Make the logout button interactive
        self.add_hover_effect(logout_btn, COLORS['warning'], COLORS['accent'])

    def create_welcome_section(self):
        # Friendly welcome message with login time
        welcome_frame = tk.Frame(self.scrollable_frame, bg=COLORS['secondary'])
        welcome_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        current_time = datetime.now().strftime("%H:%M")
        tk.Label(welcome_frame, 
                text=f"Welcome back! You logged in at {current_time}",
                font=STYLES['welcome'],
                bg=COLORS['secondary'],
                fg=COLORS['text_light']).pack(side=tk.LEFT)

    def create_dashboard_cards(self):
        # Our main feature cards - keeping them organized in rows
        features = [
            ("Vehicle Management", "Manage your electric vehicles", "🚗", self.vehicle_page),
            ("Find Stations", "Find charging stations nearby", "🔍", self.search_page),
            ("Profile", "Manage your account", "👤", self.profile_page)
        ]
        
        # Create cards in rows of two
        for i in range(0, len(features), 2):
            row = tk.Frame(self.content, bg=COLORS['secondary'])
            row.pack(fill=tk.X, pady=10)
            
            for title, desc, icon, command in features[i:i+2]:
                self.create_card(row, title, desc, icon, command)

        # Show their vehicles if they have any
        self.create_vehicle_summary_card()

    def create_vehicle_summary_card(self):
        try:
            # Load vehicles data
            data_file = os.path.join(os.path.dirname(__file__), 'vehicles_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    vehicles = data.get('cars', []) + data.get('bikes', [])
                    
                    if vehicles:
                        summary_frame = tk.Frame(self.content, bg=COLORS['card_bg'])
                        summary_frame.pack(fill=tk.X, pady=10)
                        
                        tk.Label(
                            summary_frame,
                            text="Your Vehicles",
                            font=STYLES['subtitle'],
                            bg=COLORS['card_bg']
                        ).pack(pady=10)
                        
                        for vehicle in vehicles:
                            self.create_mini_vehicle_card(summary_frame, vehicle)
        except Exception:
            pass

    def create_mini_vehicle_card(self, parent, vehicle):
        card = tk.Frame(parent, bg=COLORS['card_bg'])
        card.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            card,
            text=vehicle['name'],
            font=STYLES['text'],
            bg=COLORS['card_bg']
        ).pack(side=tk.LEFT)
        
        if vehicle.get('charging_history'):
            last_charge = vehicle['charging_history'][-1]
            tk.Label(
                card,
                text=f"Last charged: {last_charge['date']}",
                font=STYLES['small_text'],
                bg=COLORS['card_bg']
            ).pack(side=tk.RIGHT)

    def create_card(self, parent, title, description, icon, command):
        # Create main card frame
        card = tk.Frame(
            parent,
            bg=COLORS['card_bg'],
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            padx=30,
            pady=30
        )
        card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        
        # Icon with background
        icon_frame = tk.Frame(
            card,
            bg=COLORS['primary'],
            width=80,
            height=80,
            relief='flat'
        )
        icon_frame.pack(pady=(0, 20))
        icon_frame.pack_propagate(False)
        
        tk.Label(
            icon_frame,
            text=icon,
            font=('Arial', 40),
            bg=COLORS['primary'],
            fg=COLORS['text_light']
        ).pack(expand=True)
        
        # Title
        tk.Label(
            card,
            text=title,
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 10))
        
        # Description
        tk.Label(
            card,
            text=description,
            font=STYLES['small_text'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark'],
            wraplength=200
        ).pack(pady=(0, 25))
        
        # Open button
        open_btn = tk.Button(
            card,
            text="Open",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            relief='flat',
            padx=25,
            pady=12,
            cursor='hand2',
            command=command
        )
        open_btn.pack(pady=(0, 20))

        # Add hover effects
        def on_enter(e):
            open_btn['bg'] = COLORS['hover']
            card.configure(highlightbackground=COLORS['primary'])
            icon_frame.configure(bg=COLORS['hover'])

        def on_leave(e):
            open_btn['bg'] = COLORS['primary']
            card.configure(highlightbackground=COLORS['border'])
            icon_frame.configure(bg=COLORS['primary'])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        open_btn.bind("<Enter>", on_enter)
        open_btn.bind("<Leave>", on_leave)

    def vehicle_page(self):
        def open_vehicle_window():
            window = tk.Toplevel(self.root)
            vehicle.VehicleSelectionPage(window)
        
        # Directly open the vehicle window without maintenance checks
        open_vehicle_window()

    def search_page(self):
        window = tk.Toplevel(self.root)
        search.main(window, self.username) 

    def booking_page(self):
        window = tk.Toplevel(self.root)
        booking.main(window, "Selected State", self.username)

    def profile_page(self):
        try:
            window = tk.Toplevel(self.root)
            if self.username is None:
                messagebox.showerror("Error", "User not logged in")
                window.destroy()
                return
                
            user_profile.main(window, self.username)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open profile: {str(e)}")
            window.destroy()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            import login_app
            root = tk.Tk()
            login_app.LoginApp(root)
            root.mainloop()

def main(username=None):
    # Fire up the dashboard!
    root = tk.Tk()
    dashboard = MainPage(root)
    dashboard.username = username
    root.mainloop()

if __name__ == "__main__":
    main()