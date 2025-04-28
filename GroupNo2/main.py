import tkinter as tk
from tkinter import ttk
from auth import LoginPage, RegistrationPage, PasswordRecoveryPage
from customer import AddCustomerPage
from vehicle import AddVehiclePage
from booking import RentVehiclePage, BookedVehicleDetailsPage, CancelBookingsPage
from feedback import FeedbackPage
from recommendation import VehicleRecommendationPage
from usage import AverageUsagePage
from dashboard import DashboardPage  # Import the new DashboardPage

def apply_style(root):
    """
    Apply consistent styling to the application UI components.
    
    Args:
        root: The root Tkinter window to apply styles to
    """
    style = ttk.Style()
    style.theme_use("clam")  # Use the 'clam' theme as base
    # Configure button style
    style.configure("TButton", 
                  padding=5, 
                  relief="flat", 
                  background="#4CAF50", 
                  foreground="white")
    # Button hover effect
    style.map("TButton", background=[("active", "#45a049")])
    # Label style
    style.configure("TLabel", padding=5, font=("Arial", 12))
    # Entry field style
    style.configure("TEntry", padding=5)
    # Frame background color
    style.configure("TFrame", background="#f2f2f2")

class RentAndRideApp:
    """
    Main application class for the Rent and Ride vehicle rental system.
    Handles window initialization and top-level navigation.
    """
    def __init__(self, root):
        """
        Initialize the main application window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Rent and Ride - Vehicle Rental System")
        self.root.geometry("1024x768")
        self.root.configure(bg="#f2f2f2")
        apply_style(self.root)  # Apply custom styling
        self.show_login_page()  # Start with login page

    def show_login_page(self):
        """Display the login page as the initial view."""
        self.clear_window()
        # Create login page with callback for successful login
        LoginPage(self.root, self.handle_login_success)

    def handle_login_success(self, username, role):
        """
        Handle successful login by showing the home page.
        
        Args:
            username: The username of the logged in user
            role: The user's role (admin/customer)
        """
        self.clear_window()
        # Create home page with user details
        HomePage(self.root, username, role, self.show_login_page)

    def clear_window(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

class HomePage:
    """
    Home page class that provides the main application interface
    with sidebar navigation and content area.
    """
    def __init__(self, root, username, role, on_logout):
        """
        Initialize the home page with user information.
        
        Args:
            root: The parent window
            username: The logged in username
            role: The user's role (admin/customer)
            on_logout: Callback function for logout action
        """
        self.root = root
        self.username = username
        self.role = role
        self.on_logout = on_logout
        
        # Create page layout
        self.create_sidebar()
        self.create_header()
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show dashboard by default
        self.show_dashboard()

    def create_sidebar(self):
        """
        Create the sidebar navigation menu with role-specific options.
        """
        sidebar_frame = tk.Frame(self.root, bg="#333", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Base navigation buttons for all users
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Find Your Vehicle", self.vehicle_recommendations),
            ("Rent Vehicle", self.rent_vehicle),
            ("My Bookings", self.booked_vehicle_details),
            ("Cancel Bookings", self.cancel_bookings),
            ("Submit Feedback", self.customer_feedback),
            ("Logout", self.logout),
        ]
        
        # Add admin-specific buttons if user is admin
        if self.role == 'admin':
            buttons.insert(1, ("Add Customer", self.add_customer))
            buttons.insert(2, ("Add Vehicle", self.add_vehicle))
            buttons.insert(-2, ("Average Vehicle Usage", self.average_usage))

        # Create styled buttons for each navigation option
        for text, command in buttons:
            ttk.Button(
                sidebar_frame, 
                text=text, 
                command=command, 
                style="TButton"
            ).pack(fill=tk.X, padx=10, pady=5)

    def create_header(self):
        """Create the header section with welcome message."""
        header_frame = tk.Frame(self.root, bg="#4CAF50", height=100)
        header_frame.pack(fill=tk.X)
        # Welcome message with username and role
        header_text = f"Welcome, {self.username}! ({self.role.capitalize()})"
        tk.Label(
            header_frame, 
            text=header_text, 
            font=("Arial", 24), 
            fg="white", 
            bg="#4CAF50"
        ).pack(pady=20)

    def show_dashboard(self):
        """Display the dashboard page in the content area."""
        self.clear_content_frame()
        try:
            DashboardPage(self.content_frame, role=self.role)
        except TypeError:
            # Fallback if DashboardPage doesn't accept role parameter
            DashboardPage(self.content_frame)

    def add_customer(self):
        """Display the Add Customer page (admin only)."""
        if self.role == 'admin':
            self.clear_content_frame()
            AddCustomerPage(self.content_frame, self.show_dashboard)

    def add_vehicle(self):
        """Display the Add Vehicle page (admin only)."""
        if self.role == 'admin':
            self.clear_content_frame()
            AddVehiclePage(self.content_frame, self.show_dashboard)

    def vehicle_recommendations(self):
        """Display the vehicle recommendation page."""
        self.clear_content_frame()
        VehicleRecommendationPage(self.content_frame, self.show_dashboard)

    def rent_vehicle(self):
        """Display the Rent Vehicle page."""
        self.clear_content_frame()
        RentVehiclePage(self.content_frame, self.show_dashboard)

    def booked_vehicle_details(self):
        """Display the My Bookings page."""
        self.clear_content_frame()
        BookedVehicleDetailsPage(self.content_frame, self.show_dashboard)

    def cancel_bookings(self):
        """Display the Cancel Bookings page."""
        self.clear_content_frame()
        CancelBookingsPage(self.content_frame, self.show_dashboard)

    def average_usage(self):
        """Display the Average Vehicle Usage page (admin only)."""
        if self.role == 'admin':
            self.clear_content_frame()
            AverageUsagePage(self.content_frame, self.show_dashboard)

    def customer_feedback(self):
        """Display the Submit Feedback page."""
        self.clear_content_frame()
        FeedbackPage(self.content_frame, self.show_dashboard)

    def logout(self):
        """Handle logout action by returning to login page."""
        self.on_logout()

    def clear_content_frame(self):
        """Clear the current content frame before loading a new page."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    # Create and run the application
    root = tk.Tk()
    app = RentAndRideApp(root)
    root.mainloop()