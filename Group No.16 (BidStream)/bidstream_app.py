import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import random
from datetime import datetime, timedelta
import os
from PIL import Image, ImageTk
import base64
from io import BytesIO
from functools import partial

# Import our database modules
from db_connection import DatabaseConnection
from db_manager import BidStreamDBManager

# Import the BidStreamUI class from the original code
# For this implementation, I'll include the UI classes directly

class BidStreamUI:
    """Class containing UI styling constants and helper methods for BidStream"""
    
    PRIMARY_COLOR = "#2563eb"       # Royal blue
    SECONDARY_COLOR = "#0891b2"     # Teal
    ACCENT_COLOR = "#dc2626"        # Red
    SUCCESS_COLOR = "#16a34a"       # Green
    WARNING_COLOR = "#f59e0b"       # Amber
    BG_COLOR = "#f8fafc"            # Light gray
    CARD_BG = "#ffffff"             # White
    TEXT_COLOR = "#1e293b"          # Dark slate
    LIGHT_TEXT = "#64748b"          # Slate
    BORDER_COLOR = "#e2e8f0"        # Light gray border
    
    # Font configurations
    TITLE_FONT = ("Helvetica", 24, "bold")
    HEADER_FONT = ("Helvetica", 18, "bold")
    SUBHEADER_FONT = ("Helvetica", 14, "bold")
    BODY_FONT = ("Helvetica", 12)
    SMALL_FONT = ("Helvetica", 10)
    
    # Padding and spacing
    PADDING = 10
    LARGE_PADDING = 20
    
    @staticmethod
    def configure_styles():
        """Configure ttk styles for the application"""
        style = ttk.Style()
        
        # Use clam as base theme
        style.theme_use("clam")
        
        # Configure common elements
        style.configure("TFrame", background=BidStreamUI.BG_COLOR)
        style.configure("Card.TFrame", background=BidStreamUI.CARD_BG, relief="raised", borderwidth=1)
        style.configure("TLabel", background=BidStreamUI.BG_COLOR, foreground=BidStreamUI.TEXT_COLOR, font=BidStreamUI.BODY_FONT)
        style.configure("Header.TLabel", font=BidStreamUI.HEADER_FONT)
        style.configure("Subheader.TLabel", font=BidStreamUI.SUBHEADER_FONT)
        style.configure("Title.TLabel", font=BidStreamUI.TITLE_FONT)
        style.configure("Light.TLabel", foreground=BidStreamUI.LIGHT_TEXT)
        
        # Button styles with increased font size and padding for all buttons
        style.configure("TButton", 
                    background=BidStreamUI.PRIMARY_COLOR, 
                    foreground="white", 
                    font=("Helvetica", 13, "bold"),
                    padding=15)
        
        style.map("TButton",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.PRIMARY_COLOR))],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # Primary button (blue) with larger text
        style.configure("Primary.TButton", 
                    background=BidStreamUI.PRIMARY_COLOR, 
                    foreground="white",
                    font=("Helvetica", 14, "bold"))
        
        style.map("Primary.TButton",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.PRIMARY_COLOR))],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # Secondary button (teal)
        style.configure("Secondary.TButton", 
                    background=BidStreamUI.SECONDARY_COLOR, 
                    foreground="white",
                    font=("Helvetica", 14, "bold"))
        
        style.map("Secondary.TButton",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.SECONDARY_COLOR))],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # Accent button (red)
        style.configure("Accent.TButton", 
                    background=BidStreamUI.ACCENT_COLOR, 
                    foreground="white",
                    font=("Helvetica", 14, "bold"))
        
        style.map("Accent.TButton",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.ACCENT_COLOR))],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # Success button (green)
        style.configure("Success.TButton", 
                    background=BidStreamUI.SUCCESS_COLOR, 
                    foreground="white",
                    font=("Helvetica", 14, "bold"))
        
        style.map("Success.TButton",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.SUCCESS_COLOR))],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # Warning button (amber)
        style.configure("Warning.TButton", 
                    background=BidStreamUI.WARNING_COLOR, 
                    foreground="white",
                    font=("Helvetica", 14, "bold"))
        
        style.map("Warning.TButton",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.WARNING_COLOR))],
                  relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        
        # Outline button styles
        style.configure("Outline.TButton", 
                        background=BidStreamUI.CARD_BG,
                        foreground=BidStreamUI.PRIMARY_COLOR,
                        borderwidth=2,
                        font=("Helvetica", 13),
                        relief="solid")
        
        style.map("Outline.TButton",
                  background=[('active', '#f0f9ff')],
                  foreground=[('active', BidStreamUI.PRIMARY_COLOR)])
        
        # Entry style
        style.configure("TEntry", 
                        fieldbackground="white",
                        background="white",
                        padding=8,
                        relief="solid",
                        borderwidth=1)
        
        # Treeview style (for tables)
        style.configure("Treeview", 
                        background="white",
                        fieldbackground="white",
                        foreground=BidStreamUI.TEXT_COLOR,
                        font=BidStreamUI.BODY_FONT,
                        rowheight=40)
        
        style.configure("Treeview.Heading", 
                        background=BidStreamUI.PRIMARY_COLOR,
                        foreground="white",
                        font=BidStreamUI.SUBHEADER_FONT,
                        relief="flat")
        
        style.map("Treeview.Heading",
                  background=[('active', BidStreamUI.darken_color(BidStreamUI.PRIMARY_COLOR))])
        
        style.map("Treeview",
                  background=[('selected', '#dbeafe')],
                  foreground=[('selected', BidStreamUI.TEXT_COLOR)])
        
        # Combobox style
        style.configure("TCombobox", 
                        fieldbackground="white",
                        background="white",
                        padding=6)
        
        # Scrollbar style
        style.configure("TScrollbar", 
                        background=BidStreamUI.BG_COLOR,
                        troughcolor="white",
                        borderwidth=0,
                        arrowsize=14)
        
        # Notebook style (for tabs)
        style.configure("TNotebook", 
                        background=BidStreamUI.BG_COLOR,
                        tabmargins=[2, 5, 2, 0])
        
        style.configure("TNotebook.Tab", 
                        background="#dbeafe",
                        foreground=BidStreamUI.TEXT_COLOR,
                        padding=[12, 6],
                        font=BidStreamUI.BODY_FONT)
        
        style.map("TNotebook.Tab",
                  background=[('selected', BidStreamUI.PRIMARY_COLOR)],
                  foreground=[('selected', 'white')],
                  expand=[('selected', [1, 1, 1, 0])])
        
        # Separator style
        style.configure("TSeparator",
                        background=BidStreamUI.BORDER_COLOR)
        
        # LabelFrame style
        style.configure("TLabelframe",
                        background=BidStreamUI.CARD_BG,
                        foreground=BidStreamUI.TEXT_COLOR,
                        borderwidth=1,
                        relief="solid")
        
        style.configure("TLabelframe.Label",
                        background=BidStreamUI.CARD_BG,
                        foreground=BidStreamUI.PRIMARY_COLOR,
                        font=BidStreamUI.SUBHEADER_FONT)
        
        return style

    @staticmethod
    def create_card_frame(parent, padding=10, shadow=True):
        """Create a card-like frame with shadow effect"""
        # Main card frame
        card = ttk.Frame(parent, style="Card.TFrame", padding=padding)
        
        if shadow:
            # Apply a subtle border to simulate shadow
            card.configure(borderwidth=1, relief="solid")
        
        return card
    
    @staticmethod
    def create_badge(parent, text, bg_color=None, fg_color="white", font=None):
        """Create a badge label with rounded corners using Canvas"""
        if bg_color is None:
            bg_color = BidStreamUI.PRIMARY_COLOR
            
        if font is None:
            font = BidStreamUI.SMALL_FONT
            
        # Create a frame to hold the badge
        badge_frame = ttk.Frame(parent, style="TFrame")
        
        # Create a label with the badge text
        badge_label = ttk.Label(
            badge_frame, 
            text=f" {text} ", 
            background=bg_color,
            foreground=fg_color,
            font=font,
            padding=(8, 3)
        )
        badge_label.pack(padx=0, pady=0)
        
        return badge_frame
    
    @staticmethod
    def create_logo():
        """Create a simple logo for BidStream"""
        # Create a canvas for the logo
        logo_canvas = tk.Canvas(width=200, height=60, bg=BidStreamUI.BG_COLOR, highlightthickness=0)
        
        # Draw the logo text
        logo_canvas.create_text(
            100, 30, 
            text="BidStream", 
            fill=BidStreamUI.PRIMARY_COLOR, 
            font=("Helvetica", 28, "bold")
        )
        
        # Draw a small auction hammer icon
        logo_canvas.create_line(160, 25, 180, 25, width=3, fill=BidStreamUI.SECONDARY_COLOR)
        logo_canvas.create_line(170, 25, 170, 40, width=3, fill=BidStreamUI.SECONDARY_COLOR)
        logo_canvas.create_oval(165, 40, 175, 50, fill=BidStreamUI.SECONDARY_COLOR, outline="")
        
        return logo_canvas
    
    @staticmethod
    def darken_color(hex_color, factor=0.8):
        """Darken a hex color by a factor"""
        
        hex_color = hex_color.lstrip('#')
        
        # Convert to RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Darken
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def create_tooltip(widget, text):
        """Create a tooltip for a widget"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create a toplevel window
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(
                tooltip, 
                text=text, 
                background="#333333", 
                foreground="white",
                font=BidStreamUI.SMALL_FONT,
                padding=5
            )
            label.pack()
            
            widget.tooltip = tooltip
            
        def leave(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    @staticmethod
    def format_currency(amount):
        """Format a number as currency"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_time_remaining(end_time):
        """Format time remaining in a human-readable format"""
        now = datetime.now()
        time_left = end_time - now
        
        if time_left.total_seconds() <= 0:
            return "Ended"
        
        days = time_left.days
        hours = int(time_left.seconds / 3600)
        minutes = int((time_left.seconds % 3600) / 60)
        
        if days > 0:
            return f"{days}d {hours}h remaining"
        elif hours > 0:
            return f"{hours}h {minutes}m remaining"
        else:
            return f"{minutes}m remaining"
    
    @staticmethod
    def get_status_color(is_active):
        """Get the appropriate color for an auction status"""
        return BidStreamUI.SUCCESS_COLOR if is_active else BidStreamUI.ACCENT_COLOR
    
    @staticmethod
    def get_status_text(is_active):
        """Get the appropriate text for an auction status"""
        return "Active" if is_active else "Closed"

class EmbeddedImageViewer:
    """An embedded image viewer that displays within the current interface"""
    def __init__(self, parent_app, parent_frame, images_data, return_callback, standard_size=(800, 600)):
        """
        Initialize the embedded image viewer
        
        Args:
            parent_app: The main application instance
            parent_frame: The frame where the viewer will be embedded
            images_data: List of base64 encoded image data
            return_callback: Function to call when returning to the previous screen
            standard_size: Standard size for all images (width, height)
        """
        self.parent_app = parent_app
        self.parent_frame = parent_frame
        self.images_data = images_data
        self.return_callback = return_callback
        self.standard_size = standard_size
        self.current_index = 0
        self.image_refs = []  # Store references to prevent garbage collection
        self.total_images = len(images_data)
        
        # Clear the parent frame
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create a main container with proper padding
        self.main_container = ttk.Frame(self.parent_frame, style="TFrame")
        self.main_container.pack(fill="both", expand=True)
        
        # Create a header frame for title and back button
        header_frame = ttk.Frame(self.main_container, style="TFrame", padding=(20, 10, 20, 10))
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Add Back button in the top left corner with moderate size
        back_button = ttk.Button(
            header_frame, 
            text="Back", 
            command=self.return_to_previous, 
            style="Secondary.TButton",
            padding=(10, 5)
        )
        back_button.pack(side="left", padx=10)
        
        # Add title in the center
        ttk.Label(
            header_frame, 
            text="Image Gallery", 
            style="Header.TLabel"
        ).pack(side="top", pady=5, expand=True)
        
        # Create a frame for the image and side navigation buttons
        gallery_frame = ttk.Frame(self.main_container, style="TFrame")
        gallery_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid for the gallery frame to position elements
        gallery_frame.columnconfigure(0, weight=0)  # Left button column
        gallery_frame.columnconfigure(1, weight=1)  # Center image column
        gallery_frame.columnconfigure(2, weight=0)  # Right button column
        gallery_frame.rowconfigure(0, weight=1)     # Center row
        
        # Previous button on the left side - smaller size
        self.prev_button = ttk.Button(
            gallery_frame, 
            text="<", 
            command=self.prev_image, 
            style="Primary.TButton",
            width=3,
            padding=(10, 5)
        )
        self.prev_button.grid(row=0, column=0, padx=10, sticky="ns")
        
        # Create image display area
        img_frame = BidStreamUI.create_card_frame(gallery_frame, padding=10)
        img_frame.grid(row=0, column=1, sticky="nsew")
        
        # Create a container for the image with fixed size
        self.img_container = ttk.Frame(img_frame, style="TFrame", width=standard_size[0], height=standard_size[1])
        self.img_container.pack(pady=10, padx=10)
        self.img_container.pack_propagate(False)  # Prevent the frame from resizing to fit contents
        
        # Image label to display the current image
        self.img_label = ttk.Label(self.img_container)
        self.img_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Next button on the right side - smaller size
        self.next_button = ttk.Button(
            gallery_frame, 
            text=">", 
            command=self.next_image, 
            style="Primary.TButton",
            width=3,
            padding=(10, 5)
        )
        self.next_button.grid(row=0, column=2, padx=10, sticky="ns")
        
        # Create a footer frame for the image counter
        footer_frame = ttk.Frame(self.main_container, style="TFrame")
        footer_frame.pack(fill="x", pady=10)
        
        # Image counter in the footer
        self.counter_label = ttk.Label(
            footer_frame, 
            text=f"Image 1/{self.total_images}",
            font=BidStreamUI.SUBHEADER_FONT
        )
        self.counter_label.pack(anchor="center")
        
        # Load and standardize all images
        self.load_images()
        
        # Display the first image and update button states
        self.show_image()
        self.update_button_states()

    def load_images(self):
        """Load and standardize all images"""
        for img_data in self.images_data:
            try:
                # Decode the base64 image data
                image_data = base64.b64decode(img_data)
                img = Image.open(BytesIO(image_data))
                
                # Calculate scaling to maintain aspect ratio
                img_width, img_height = img.size
                ratio = min(self.standard_size[0]/img_width, self.standard_size[1]/img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                
                # Resize the image while maintaining aspect ratio using high-quality scaling
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create a new blank image with the standard size and white background
                standardized_img = Image.new("RGB", self.standard_size, (255, 255, 255))
                
                # Calculate position to center the image
                left = (self.standard_size[0] - new_width) // 2
                top = (self.standard_size[1] - new_height) // 2
                
                # Paste the resized image onto the standardized canvas
                standardized_img.paste(resized_img, (left, top))
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(standardized_img)
                self.image_refs.append(photo)
            except Exception as e:
                print(f"Error loading image: {e}")
                # If image fails to load, add a placeholder
                self.image_refs.append(None)
    
    def show_image(self):
        """Display the current image"""
        if self.image_refs and self.current_index < len(self.image_refs) and self.image_refs[self.current_index]:
            self.img_label.config(image=self.image_refs[self.current_index])
            self.counter_label.config(text=f"Image {self.current_index+1}/{len(self.image_refs)}")
        else:
            self.img_label.config(image="", text="Image Error")
        
        # Update button states after changing the image
        self.update_button_states()
    
    def update_button_states(self):
        """Update the state of navigation buttons based on current index"""
        # Disable Previous button on first image
        if self.current_index == 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")
        
        # Disable Next button on last image
        if self.current_index == len(self.image_refs) - 1:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")
    
    def prev_image(self):
        """Show the previous image"""
        if self.image_refs and self.current_index > 0:
            self.current_index -= 1
            self.show_image()
    
    def next_image(self):
        """Show the next image"""
        if self.image_refs and self.current_index < len(self.image_refs) - 1:
            self.current_index += 1
            self.show_image()
    
    def return_to_previous(self):
        """Return to the previous screen"""
        # Reset window size if needed
        if hasattr(self.parent_app, 'root'):
            self.parent_app.root.geometry("1000x750")  # Reset to original size
            
        if self.return_callback:
            self.return_callback()

class BiddingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BidStream")
        self.root.geometry("1000x750")  # Increased size for better layout
        
        # Configure the UI styles
        self.style = BidStreamUI.configure_styles()
        
        # Set the background color for the root window
        self.root.configure(bg=BidStreamUI.BG_COLOR)
        
        # Create the logo once and store it
        self.logo = BidStreamUI.create_logo()
        
        # Initialize database connection
        self.db = DatabaseConnection(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="1234",  # Replace with your MySQL password
            database="bidstream"  # This database should exist
        )
        
        if not self.db.connect():
            messagebox.showerror("Database Error", "Failed to connect to database")
            self.root.destroy()
            return
        
        # Create database manager
        self.db_manager = BidStreamDBManager(self.db)
        
        self.current_user = None
        
        # Create images directory if it doesn't exist
        self.images_dir = "item_images"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        # Create a main container frame
        self.main_container = ttk.Frame(self.root, style="TFrame", padding=BidStreamUI.PADDING)
        self.main_container.pack(expand=True, fill="both")
        
        # Create a header frame for app title and logo
        self.header_frame = ttk.Frame(self.main_container, style="TFrame")
        self.header_frame.pack(fill="x", pady=(0, BidStreamUI.PADDING))
        
        # Create the main content frame
        self.main_frame = ttk.Frame(self.main_container, style="TFrame", padding=BidStreamUI.PADDING)
        self.main_frame.pack(expand=True, fill="both")
        
        # Temporary storage for item data between pages
        self.temp_item_data = {
            "name": "",
            "price": "",
            "description": "",
            "images_data": []
        }
        
        # Create a loading indicator
        self.loading_var = tk.BooleanVar(value=False)
        self.create_loading_indicator()

        # Start with the selection screen
        self.show_selection_screen()

    def create_loading_indicator(self):
        """Create a loading indicator overlay"""
        self.loading_frame = ttk.Frame(self.root, style="TFrame")
        self.loading_label = ttk.Label(
            self.loading_frame, 
            text="Loading...", 
            font=BidStreamUI.HEADER_FONT,
            foreground=BidStreamUI.PRIMARY_COLOR,
            background=BidStreamUI.BG_COLOR
        )
        self.loading_label.pack(pady=20)
        
        # Bind the loading variable to show/hide the loading frame
        self.loading_var.trace_add("write", self.update_loading_indicator)
    
    def update_loading_indicator(self, *args):
        """Update the loading indicator based on the loading variable"""
        if self.loading_var.get():
            # Show loading indicator
            self.loading_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.root.update()
        else:
            # Hide loading indicator
            self.loading_frame.place_forget()
            self.root.update()
    
    def show_loading(self, show=True):
        """Show or hide the loading indicator"""
        self.loading_var.set(show)
        
    def update_header(self, title_text=None):
        """Update the header with the given title"""
        # Clear existing header content
        for widget in self.header_frame.winfo_children():
            widget.destroy()
            
        # Create a frame for the logo and title
        logo_title_frame = ttk.Frame(self.header_frame, style="TFrame")
        logo_title_frame.pack(side="left", fill="y")
        
        # Add logo (reuse the stored logo)
        self.logo.pack(side="left", padx=(0, 20))
        
        if title_text:
            # Add title
            ttk.Label(
                logo_title_frame, 
                text=title_text, 
                style="Subheader.TLabel"
            ).pack(side="left", pady=BidStreamUI.PADDING)
        
        # Add user info if logged in
        if self.current_user:
            user_frame = ttk.Frame(self.header_frame, style="TFrame")
            user_frame.pack(side="right", fill="y", padx=BidStreamUI.PADDING)
            
            user_type = "Admin" if self.db_manager.is_admin(self.current_user) else "User"
            
            # Create a badge for the user type
            badge_color = BidStreamUI.PRIMARY_COLOR if user_type == "Admin" else BidStreamUI.SECONDARY_COLOR
            user_badge = BidStreamUI.create_badge(user_frame, user_type, badge_color)
            user_badge.pack(side="right", padx=(10, 0))
            
            ttk.Label(
                user_frame,
                text=f"Logged in as: {self.current_user}",
                style="Light.TLabel"
            ).pack(side="right")
            
        # Add a separator
        separator = ttk.Separator(self.header_frame, orient="horizontal")
        separator.pack(fill="x", pady=(BidStreamUI.PADDING, 0))

    def show_selection_screen(self):
        """Show initial screen to select between admin and user login"""
        self.clear_frame()
        
        # Update header
        self.update_header("Welcome")
        
        # Create a centered container for the content
        content_frame = ttk.Frame(self.main_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Welcome message
        ttk.Label(
            content_frame, 
            text="Welcome to BidStream", 
            style="Title.TLabel"
        ).pack(pady=(0, 10))
        
        # Create a card for the login options
        login_card = BidStreamUI.create_card_frame(content_frame, padding=BidStreamUI.LARGE_PADDING)
        login_card.pack(pady=BidStreamUI.LARGE_PADDING, padx=BidStreamUI.LARGE_PADDING)
        
        # Admin login button
        admin_button = ttk.Button(
            login_card, 
            text="Admin Login", 
            command=self.show_admin_login, 
            style="Primary.TButton"
        )
        admin_button.pack(pady=BidStreamUI.LARGE_PADDING, padx=BidStreamUI.LARGE_PADDING, ipady=10, ipadx=20, fill="x")
        BidStreamUI.create_tooltip(admin_button, "Login as an administrator to manage auctions")
        
        # User login button
        user_button = ttk.Button(
            login_card, 
            text="User Login", 
            command=self.show_user_login, 
            style="Secondary.TButton"
        )
        user_button.pack(pady=BidStreamUI.LARGE_PADDING, padx=BidStreamUI.LARGE_PADDING, ipady=10, ipadx=20, fill="x")
        BidStreamUI.create_tooltip(user_button, "Login as a user to bid on items or list your own")

    def show_admin_login(self):
        """Show admin login screen"""
        self.clear_frame()
        
        self.update_header("Admin Login")
        
        # Create a centered container for the login form
        content_frame = ttk.Frame(self.main_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a card for the login form
        login_card = BidStreamUI.create_card_frame(content_frame, padding=BidStreamUI.LARGE_PADDING)
        login_card.pack(pady=BidStreamUI.PADDING)
        
        # Username field
        username_frame = ttk.Frame(login_card, style="TFrame")
        username_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(username_frame, text="Username:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.admin_username_entry = ttk.Entry(username_frame, width=30, font=BidStreamUI.BODY_FONT)
        self.admin_username_entry.pack(fill="x", ipady=5)
        
        # Password field
        password_frame = ttk.Frame(login_card, style="TFrame")
        password_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(password_frame, text="Password:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.admin_password_entry = ttk.Entry(password_frame, show="*", width=30, font=BidStreamUI.BODY_FONT)
        self.admin_password_entry.pack(fill="x", ipady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_card, style="TFrame")
        button_frame.pack(fill="x", pady=BidStreamUI.LARGE_PADDING)
        
        ttk.Button(
            button_frame, 
            text="Login", 
            command=self.admin_login, 
            style="Primary.TButton"
        ).pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        ttk.Button(
            button_frame, 
            text="Back", 
            command=self.show_selection_screen, 
            style="Secondary.TButton"
        ).pack(side="right", padx=(5, 0), expand=True, fill="x")

    def show_user_login(self):
        """Show user login screen"""
        self.clear_frame()
        self.update_header("User Login")
        
        # Create a centered container for the login form
        content_frame = ttk.Frame(self.main_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a card for the login form
        login_card = BidStreamUI.create_card_frame(content_frame, padding=BidStreamUI.LARGE_PADDING)
        login_card.pack(pady=BidStreamUI.PADDING)
        
        # Username field
        username_frame = ttk.Frame(login_card, style="TFrame")
        username_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(username_frame, text="Username:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.username_entry = ttk.Entry(username_frame, width=30, font=BidStreamUI.BODY_FONT)
        self.username_entry.pack(fill="x", ipady=5)
        
        # Password field
        password_frame = ttk.Frame(login_card, style="TFrame")
        password_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(password_frame, text="Password:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.password_entry = ttk.Entry(password_frame, show="*", width=30, font=BidStreamUI.BODY_FONT)
        self.password_entry.pack(fill="x", ipady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_card, style="TFrame")
        button_frame.pack(fill="x", pady=BidStreamUI.LARGE_PADDING)
        
        ttk.Button(
            button_frame, 
            text="Login", 
            command=self.user_login, 
            style="Primary.TButton"
        ).pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        ttk.Button(
            button_frame, 
            text="Register", 
            command=self.show_registration, 
            style="Secondary.TButton"
        ).pack(side="right", padx=(5, 0), expand=True, fill="x")
        
        # Back button
        ttk.Button(
            content_frame, 
            text="Back to Selection", 
            command=self.show_selection_screen, 
            style="Outline.TButton"
        ).pack(pady=BidStreamUI.PADDING)

    def show_registration(self):
        self.clear_frame()
        self.update_header("User Registration")
        
        # Create a centered container for the registration form
        content_frame = ttk.Frame(self.main_frame, style="TFrame")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create a card for the registration form
        reg_card = BidStreamUI.create_card_frame(content_frame, padding=BidStreamUI.LARGE_PADDING)
        reg_card.pack(pady=BidStreamUI.PADDING)
        
        # Username field
        username_frame = ttk.Frame(reg_card, style="TFrame")
        username_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(username_frame, text="Username:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.reg_username_entry = ttk.Entry(username_frame, width=30, font=BidStreamUI.BODY_FONT)
        self.reg_username_entry.pack(fill="x", ipady=5)
        
        # Email field
        email_frame = ttk.Frame(reg_card, style="TFrame")
        email_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(email_frame, text="Email:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.reg_email_entry = ttk.Entry(email_frame, width=30, font=BidStreamUI.BODY_FONT)
        self.reg_email_entry.pack(fill="x", ipady=5)
        
        # Password field
        password_frame = ttk.Frame(reg_card, style="TFrame")
        password_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(password_frame, text="Password:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.reg_password_entry = ttk.Entry(password_frame, show="*", width=30, font=BidStreamUI.BODY_FONT)
        self.reg_password_entry.pack(fill="x", ipady=5)
        
        # Buttons
        button_frame = ttk.Frame(reg_card, style="TFrame")
        button_frame.pack(fill="x", pady=BidStreamUI.LARGE_PADDING)
        
        ttk.Button(
            button_frame, 
            text="Register", 
            command=self.register, 
            style="Primary.TButton"
        ).pack(side="left", padx=(0, 5), expand=True, fill="x")
        
        ttk.Button(
            button_frame, 
            text="Back to Login", 
            command=self.show_user_login, 
            style="Secondary.TButton"
        ).pack(side="right", padx=(5, 0), expand=True, fill="x")

    def register(self):
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()

        # Email validation using regex
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if username and email and password:
            # Validate email format
            if not re.match(email_pattern, email):
                messagebox.showerror("Error", "Invalid email format. Please enter a valid email.")
                return
                
            self.show_loading(True)
            
            # Register user in database
            success, result = self.db_manager.register_user(username, email, password)
            
            self.show_loading(False)
            
            if success:
                messagebox.showinfo("Success", "Registration successful")
                self.show_user_login()
            else:
                messagebox.showerror("Error", f"Registration failed: {result}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def admin_login(self):
        """Handle admin login"""
        self.show_loading(True)
        username = self.admin_username_entry.get()
        password = self.admin_password_entry.get()

        # Authenticate with database
        success, result = self.db_manager.authenticate_user(username, password)
        
        if success and self.db_manager.is_admin(username):
            self.current_user = username
            self.show_loading(False)
            self.show_admin_dashboard()
        else:
            self.show_loading(False)
            messagebox.showerror("Error", "Invalid admin credentials")

    def user_login(self):
        """Handle user login"""
        self.show_loading(True)
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Authenticate with database
        success, result = self.db_manager.authenticate_user(username, password)
        
        if success:
            self.current_user = username
            self.show_loading(False)
            self.show_user_dashboard()
            self.check_won_auctions()
        else:
            self.show_loading(False)
            messagebox.showerror("Error", "Invalid username or password")

    def show_user_dashboard(self):
        self.clear_frame()
        self.update_header("Dashboard")
        
        # Create a welcome banner with proper padding
        welcome_frame = ttk.Frame(self.main_frame, style="TFrame", padding=(20, 10))
        welcome_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(
            welcome_frame, 
            text=f"Welcome back, {self.current_user}!", 
            style="Header.TLabel"
        ).pack(anchor="w")
        
        ttk.Label(
            welcome_frame, 
            text="Manage your auctions and bids from your personal dashboard", 
            style="Light.TLabel"
        ).pack(anchor="w", pady=(5, 0))
        
        # Create a centered container for the dashboard with proper padding
        content_frame = ttk.Frame(self.main_frame, style="TFrame", padding=(20, 10))
        content_frame.pack(expand=True, fill="both")
        
        # Configure grid with proper weights and spacing
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # Card 1: List Item
        list_card = BidStreamUI.create_card_frame(content_frame, padding=30)
        list_card.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        ttk.Label(list_card, text="List Item for Auction", style="Header.TLabel").pack(anchor="center", pady=(0, 15))
        ttk.Label(list_card, text="Create a new auction listing", style="Light.TLabel").pack(anchor="center", pady=(0, 20))
        
        ttk.Button(
            list_card, 
            text="List New Item", 
            command=self.show_list_item_details, 
            style="Primary.TButton"
        ).pack(pady=(30, 15), padx=30, ipady=10, ipadx=20, fill="x")
        
        # Card 2: View Items
        view_card = BidStreamUI.create_card_frame(content_frame, padding=30)
        view_card.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        ttk.Label(view_card, text="Available Items", style="Header.TLabel").pack(anchor="center", pady=(0, 15))
        ttk.Label(view_card, text="Browse and bid on available items", style="Light.TLabel").pack(anchor="center", pady=(0, 20))
        
        ttk.Button(
            view_card, 
            text="View Auction Items", 
            command=self.show_available_items, 
            style="Secondary.TButton"
        ).pack(pady=(30, 15), padx=30, ipady=10, ipadx=20, fill="x")
        
        # Card 3: Previous Bids
        bids_card = BidStreamUI.create_card_frame(content_frame, padding=30)
        bids_card.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        
        ttk.Label(bids_card, text="My Listed Items", style="Header.TLabel").pack(anchor="center", pady=(0, 15))
        ttk.Label(bids_card, text="View your listed items and their status", style="Light.TLabel").pack(anchor="center", pady=(0, 20))
        
        ttk.Button(
            bids_card, 
            text="View My Items", 
            command=self.show_previous_bidded_items, 
            style="Success.TButton"
        ).pack(pady=(30, 15), padx=30, ipady=10, ipadx=20, fill="x")
        
        # Card 4: Logout
        logout_card = BidStreamUI.create_card_frame(content_frame, padding=30)
        logout_card.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        
        ttk.Label(logout_card, text="Account Options", style="Header.TLabel").pack(anchor="center", pady=(0, 15))
        ttk.Label(logout_card, text="Manage your account settings", style="Light.TLabel").pack(anchor="center", pady=(0, 20))
        
        ttk.Button(
            logout_card, 
            text="Logout", 
            command=self.logout, 
            style="Accent.TButton"
        ).pack(pady=(30, 15), padx=30, ipady=10, ipadx=20, fill="x")

    def show_admin_dashboard(self):
        self.clear_frame()
        self.update_header("Admin Dashboard")
        
        # Create a welcome banner
        welcome_frame = ttk.Frame(self.main_frame, style="TFrame")
        welcome_frame.pack(fill="x", pady=(0, BidStreamUI.LARGE_PADDING))
        
        ttk.Label(
            welcome_frame, 
            text=f"Welcome, Administrator", 
            style="Header.TLabel"
        ).pack(anchor="w")
        
        ttk.Label(
            welcome_frame, 
            text="Manage all auctions and view platform statistics", 
            style="Light.TLabel"
        ).pack(anchor="w", pady=(5, 0))
        
        # Create a centered container for the dashboard
        content_frame = ttk.Frame(self.main_frame, style="TFrame")
        content_frame.pack(expand=True, fill="both", pady=BidStreamUI.PADDING)
        
        # Create a grid layout for dashboard cards
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Card 1: View All Items
        items_card = BidStreamUI.create_card_frame(content_frame, padding=BidStreamUI.LARGE_PADDING)
        items_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(items_card, text="Manage Auctions", style="Header.TLabel").pack(anchor="center", pady=(0, 10))
        ttk.Label(items_card, text="View and manage all auction items", style="Light.TLabel").pack(anchor="center", pady=(0, 15))
        
        # Add an icon or image for the card
        canvas = tk.Canvas(items_card, width=64, height=64, bg=BidStreamUI.CARD_BG, highlightthickness=0)
        canvas.pack(pady=10)
        
        # Draw a simple icon
        canvas.create_rectangle(10, 15, 54, 49, fill=BidStreamUI.PRIMARY_COLOR, outline="")
        canvas.create_line(20, 25, 44, 25, width=2, fill="white")
        canvas.create_line(20, 35, 44, 35, width=2, fill="white")
        canvas.create_line(20, 45, 44, 45, width=2, fill="white")
        
        ttk.Button(
            items_card, 
            text="View All Items", 
            command=self.show_all_items, 
            style="Primary.TButton"
        ).pack(pady=10, padx=20, ipady=10, fill="x")
        
        # Card 2: Bid Report
        report_card = BidStreamUI.create_card_frame(content_frame, padding=BidStreamUI.LARGE_PADDING)
        report_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ttk.Label(report_card, text="Auction Analytics", style="Header.TLabel").pack(anchor="center", pady=(0, 10))
        ttk.Label(report_card, text="View detailed bidding statistics and reports", style="Light.TLabel").pack(anchor="center", pady=(0, 15))
        
        # Add an icon or image for the card
        canvas = tk.Canvas(report_card, width=64, height=64, bg=BidStreamUI.CARD_BG, highlightthickness=0)
        canvas.pack(pady=10)
        
        # Draw a simple chart icon
        canvas.create_rectangle(10, 45, 20, 49, fill=BidStreamUI.SECONDARY_COLOR, outline="")
        canvas.create_rectangle(25, 35, 35, 49, fill=BidStreamUI.SECONDARY_COLOR, outline="")
        canvas.create_rectangle(40, 25, 50, 49, fill=BidStreamUI.SECONDARY_COLOR, outline="")
        canvas.create_line(10, 20, 50, 20, width=1, fill=BidStreamUI.SECONDARY_COLOR)
        
        ttk.Button(
            report_card, 
            text="View Analytics", 
            command=self.show_bid_report, 
            style="Secondary.TButton"
        ).pack(pady=10, padx=20, ipady=10, fill="x")
        
        # Logout button at the bottom
        logout_frame = ttk.Frame(self.main_frame, style="TFrame")
        logout_frame.pack(pady=BidStreamUI.LARGE_PADDING)
        
        ttk.Button(
            logout_frame, 
            text="Logout", 
            command=self.logout, 
            style="Accent.TButton"
        ).pack(pady=10, padx=20, ipady=5, ipadx=20)

    def logout(self):
        """Handle logout for both admin and users"""
        self.show_loading(True)
        
        # Simulate network delay
        self.root.after(500, self._complete_logout)
    
    def _complete_logout(self):
        """Complete the logout process after loading"""
        self.current_user = None
        self.show_loading(False)
        self.show_selection_screen()

    def show_list_item_details(self):
        """Show the first page of listing an item - details entry"""
        self.clear_frame()
        self.update_header("List Item for Auction")
        
        # Create a main container frame with proper padding
        main_container = ttk.Frame(self.main_frame, style="TFrame", padding=(20, 10))
        main_container.pack(fill="both", expand=True)
        
        # Configure grid for center alignment
        main_container.columnconfigure(0, weight=1)  # Left margin
        main_container.columnconfigure(1, weight=0)  # Content column
        main_container.columnconfigure(2, weight=1)  # Right margin
        main_container.rowconfigure(0, weight=1)     # Top margin
        main_container.rowconfigure(1, weight=0)     # Content row
        main_container.rowconfigure(2, weight=1)     # Bottom margin
        
        # Create centered content container
        centered_content = ttk.Frame(main_container, style="TFrame")
        centered_content.grid(row=1, column=1)
        
        # Create a card for the form
        form_card = BidStreamUI.create_card_frame(centered_content, padding=BidStreamUI.LARGE_PADDING)
        form_card.pack(pady=BidStreamUI.PADDING)
        
        # Form title
        ttk.Label(
            form_card, 
            text="Create New Auction Listing", 
            style="Header.TLabel"
        ).pack(anchor="center", pady=(0, BidStreamUI.LARGE_PADDING))
        
        # Item name field - centered
        name_frame = ttk.Frame(form_card, style="TFrame")
        name_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(name_frame, text="Item Name:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.item_name_entry = ttk.Entry(name_frame, width=50, font=BidStreamUI.BODY_FONT)
        self.item_name_entry.pack(fill="x", ipady=5)
        
        # Starting price field - centered
        price_frame = ttk.Frame(form_card, style="TFrame")
        price_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(price_frame, text="Starting Price:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        self.item_price_entry = ttk.Entry(price_frame, width=50, font=BidStreamUI.BODY_FONT)
        self.item_price_entry.pack(fill="x", ipady=5)
        
        # Description field - centered
        desc_frame = ttk.Frame(form_card, style="TFrame")
        desc_frame.pack(fill="x", pady=BidStreamUI.PADDING)
        
        ttk.Label(desc_frame, text="Item Description:", style="Subheader.TLabel").pack(anchor="w", pady=(0, 5))
        
        # Use ScrolledText for multiline input with scrollbars
        self.item_description_text = scrolledtext.ScrolledText(
            desc_frame, 
            wrap=tk.WORD,
            width=50, 
            height=10,
            font=BidStreamUI.BODY_FONT,
            background="white"
        )
        self.item_description_text.pack(fill="x", pady=5)
        
        # Navigation buttons - centered
        button_frame = ttk.Frame(form_card, style="TFrame")
        button_frame.pack(pady=20, anchor="center")
        
        # Create a container for buttons to center them
        buttons_container = ttk.Frame(button_frame, style="TFrame")
        buttons_container.pack(anchor="center")
        
        ttk.Button(
            buttons_container, 
            text="Next", 
            command=self.save_details_and_show_image_upload,
            style="Primary.TButton"
        ).pack(side="left", padx=10)
        
        ttk.Button(
            buttons_container, 
            text="Back", 
            command=self.show_user_dashboard,
            style="Secondary.TButton"
        ).pack(side="left", padx=10)
        
        # Pre-fill fields if we're coming back from the image upload page
        if self.temp_item_data["name"]:
            self.item_name_entry.insert(0, self.temp_item_data["name"])
        if self.temp_item_data["price"]:
            self.item_price_entry.insert(0, self.temp_item_data["price"])
        if self.temp_item_data["description"]:
            self.item_description_text.insert("1.0", self.temp_item_data["description"])

    def save_details_and_show_image_upload(self):
        # Save the current details to temp storage
        self.temp_item_data["name"] = self.item_name_entry.get()
        self.temp_item_data["price"] = self.item_price_entry.get()
        self.temp_item_data["description"] = self.item_description_text.get("1.0", tk.END).strip()
        
        # Validate required fields
        if not self.temp_item_data["name"] or not self.temp_item_data["price"]:
            messagebox.showerror("Error", "Please fill in Item Name and Starting Price")
            return
        
        # Show the image upload page
        self.show_image_upload_page()

    def show_image_upload_page(self):
        """Show the second page of listing an item - image upload"""
        self.clear_frame()
        self.update_header("Upload Item Images")
        
        # Create a main container frame with proper padding
        main_container = ttk.Frame(self.main_frame, style="TFrame", padding=(20, 10))
        main_container.pack(fill="both", expand=True)
        
        # Configure grid for center alignment
        main_container.columnconfigure(0, weight=1)  # Left margin
        main_container.columnconfigure(1, weight=0)  # Content column
        main_container.columnconfigure(2, weight=1)  # Right margin
        main_container.rowconfigure(0, weight=1)     # Top margin
        main_container.rowconfigure(1, weight=0)     # Content row
        main_container.rowconfigure(2, weight=1)     # Bottom margin
        
        # Create centered content container
        centered_content = ttk.Frame(main_container, style="TFrame")
        centered_content.grid(row=1, column=1)
        
        # Create a card for the form
        form_card = BidStreamUI.create_card_frame(centered_content, padding=BidStreamUI.LARGE_PADDING)
        form_card.pack(pady=BidStreamUI.PADDING)
        
        # Title - centered
        ttk.Label(
            form_card, 
            text="Upload Item Images", 
            style="Header.TLabel"
        ).pack(anchor="center", pady=(0, BidStreamUI.LARGE_PADDING))
        
        # Item image upload section - centered
        upload_frame = ttk.Frame(form_card, style="TFrame")
        upload_frame.pack(pady=10, anchor="center")
        
        ttk.Button(
            upload_frame, 
            text="Upload Images", 
            command=self.upload_images,
            style="Primary.TButton"
        ).pack(anchor="center", pady=10, ipady=5, ipadx=10)
        
        # Create a frame for image preview with navigation - centered
        self.preview_frame = ttk.Frame(form_card, style="TFrame")
        self.preview_frame.pack(anchor="center", pady=20)
        
        # Image preview label - centered
        self.image_preview_label = ttk.Label(self.preview_frame, text="No images selected")
        self.image_preview_label.pack(anchor="center", pady=5)
        
        # Navigation buttons frame - centered
        self.nav_buttons_frame = ttk.Frame(self.preview_frame, style="TFrame")
        self.nav_buttons_frame.pack(anchor="center", pady=5)
        
        # Initialize image preview variables
        self.current_preview_index = 0
        self.image_previews = []
        
        # If we have images from previous upload, show them
        if self.temp_item_data["images_data"]:
            self.load_image_previews()
        
        # Navigation buttons - centered
        button_frame = ttk.Frame(form_card, style="TFrame")
        button_frame.pack(pady=20, anchor="center")
        
        # Create a container for buttons to center them
        buttons_container = ttk.Frame(button_frame, style="TFrame")
        buttons_container.pack(anchor="center")
        
        ttk.Button(
            buttons_container, 
            text="Back", 
            command=self.show_list_item_details,
            style="Secondary.TButton"
        ).pack(side="left", padx=10)
        
        ttk.Button(
            buttons_container, 
            text="List Item", 
            command=self.list_item,
            style="Success.TButton"
        ).pack(side="left", padx=10)

    def load_image_previews(self):
        """Load image previews from the temp_item_data"""
        self.image_previews = []
        for img_data in self.temp_item_data["images_data"]:
            try:
                # Decode the base64 image data
                image_data = base64.b64decode(img_data)
                img = Image.open(BytesIO(image_data))
                
                # Resize for preview
                img = img.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_previews.append(photo)
            except Exception as e:
                print(f"Error loading image preview: {e}")
        
        # Update the preview display
        if self.image_previews:
            self.update_image_preview()
            self.update_navigation_buttons()
        else:
            self.image_preview_label.config(image="", text="No images selected")
            # Hide navigation buttons if no images
            for widget in self.nav_buttons_frame.winfo_children():
                widget.destroy()

    def upload_images(self):
        file_types = [("Image files", "*.jpg *.jpeg *.png")]
        file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=file_types)
        
        if file_paths:
            self.show_loading(True)
            
            # Process images in a separate function to allow UI updates
            self.root.after(100, lambda: self._process_uploaded_images(file_paths))
    
    def _process_uploaded_images(self, file_paths):
        """Process uploaded images after showing loading indicator"""
        try:
            # Clear previous images
            self.temp_item_data["images_data"] = []
            self.image_previews = []
            self.current_preview_index = 0
            
            for file_path in file_paths:
                try:
                    # Open and resize the image for preview
                    with Image.open(file_path) as img:
                        img = img.resize((100, 100), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.image_previews.append(photo)
                        
                        # Store the image data as base64 for later use
                        with open(file_path, "rb") as img_file:
                            encoded_data = base64.b64encode(img_file.read()).decode('utf-8')
                            self.temp_item_data["images_data"].append(encoded_data)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to upload image {file_path}: {str(e)}")
                    continue
            
            # Update navigation buttons if there are images
            if self.image_previews:
                self.update_image_preview()
                self.update_navigation_buttons()
                messagebox.showinfo("Success", f"{len(self.image_previews)} images uploaded successfully")
            else:
                self.image_preview_label.config(image="", text="No images selected")
                # Hide navigation buttons if no images
                for widget in self.nav_buttons_frame.winfo_children():
                    widget.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process images: {str(e)}")
        finally:
            self.show_loading(False)

    def update_image_preview(self):
        """Update the image preview based on current index"""
        if self.image_previews:
            self.image_preview_label.config(
                image=self.image_previews[self.current_preview_index], 
                text=""
            )
        else:
            self.image_preview_label.config(image="", text="No images selected")

    def update_navigation_buttons(self):
        """Update navigation buttons based on number of images"""
        # Clear existing buttons
        for widget in self.nav_buttons_frame.winfo_children():
            widget.destroy()
            
        if len(self.image_previews) > 1:
            ttk.Button(
                self.nav_buttons_frame, 
                text="Previous", 
                command=self.show_previous_image,
                style="Primary.TButton"
            ).pack(side="left", padx=5)
            
            # Add image counter label
            self.counter_label = ttk.Label(
                self.nav_buttons_frame, 
                text=f"Image {self.current_preview_index + 1}/{len(self.image_previews)}"
            )
            self.counter_label.pack(side="left", padx=10)
            
            ttk.Button(
                self.nav_buttons_frame, 
                text="Next", 
                command=self.show_next_image,
                style="Primary.TButton"
            ).pack(side="left", padx=5)

    def show_previous_image(self):
        """Show the previous image in the preview"""
        if self.image_previews:
            self.current_preview_index = (self.current_preview_index - 1) % len(self.image_previews)
            self.update_image_preview()
            self.counter_label.config(text=f"Image {self.current_preview_index + 1}/{len(self.image_previews)}")

    def show_next_image(self):
        """Show the next image in the preview"""
        if self.image_previews:
            self.current_preview_index = (self.current_preview_index + 1) % len(self.image_previews)
            self.update_image_preview()
            self.counter_label.config(text=f"Image {self.current_preview_index + 1}/{len(self.image_previews)}")

    def list_item(self):
        """Final step to list the item after collecting all details"""
        name = self.temp_item_data["name"]
        price = self.temp_item_data["price"]
        description = self.temp_item_data["description"]
        images_data = self.temp_item_data["images_data"]

        if name and price and images_data:
            try:
                price = float(price)
                self.show_loading(True)
                
                # List item in database
                success, item_id = self.db_manager.list_item(
                    self.current_user, name, price, description, images_data
                )
                
                self.show_loading(False)
                
                if success:
                    messagebox.showinfo("Success", f"Item '{name}' listed successfully with ID: {item_id}")
                    
                    # Reset temporary storage
                    self.temp_item_data = {
                        "name": "",
                        "price": "",
                        "description": "",
                        "images_data": []
                    }
                    
                    self.show_user_dashboard()
                else:
                    messagebox.showerror("Error", f"Failed to list item: {item_id}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid price")
        else:
            if not images_data:
                messagebox.showerror("Error", "Please upload at least one image")
            else:
                messagebox.showerror("Error", "Please fill in all required fields")

    def create_image_gallery(self, parent_frame, images_data, size=100, return_callback=None):
        """Create an image gallery with navigation buttons and clickable images"""
        try:
            # Create a frame for the image and navigation
            gallery_frame = BidStreamUI.create_card_frame(parent_frame, padding=10)
            gallery_frame.pack(padx=10, pady=10, anchor="center")
            
            # Create image display with fixed size container
            img_container = ttk.Frame(gallery_frame, width=size+20, height=size+20, style="TFrame")
            img_container.pack(pady=5)
            img_container.pack_propagate(False)  # Prevent resizing
            
            # Create a loading label that will be shown while images load
            loading_label = ttk.Label(
                img_container,
                text="Loading...",
                style="Subheader.TLabel"
            )
            
            # Create the image label separately
            img_label = ttk.Label(img_container, cursor="hand2")  # Add hand cursor to indicate clickable
            
            # Initialize variables
            current_index = [0]  # Use list for mutable reference
            image_refs = []  # Store references to prevent garbage collection
            
            # Show loading label initially
            loading_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Load all images
            for img_data in images_data:
                try:
                    # Decode the base64 image data
                    image_data = base64.b64decode(img_data)
                    img = Image.open(BytesIO(image_data))
                    
                    # Calculate scaling to maintain aspect ratio
                    img_width, img_height = img.size
                    ratio = min((size-10)/img_width, (size-10)/img_height)
                    new_width = int(img_width * ratio)
                    new_height = int(img_height * ratio)
                    
                    # Resize the image while maintaining aspect ratio using high-quality scaling
                    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Create a new blank image with the standard size and white background
                    standardized_img = Image.new("RGB", (size, size), (255, 255, 255))
                    
                    # Calculate position to center the image
                    left = (size - new_width) // 2
                    top = (size - new_height) // 2
                    
                    # Paste the resized image onto the standardized canvas
                    standardized_img.paste(resized_img, (left, top))
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(standardized_img)
                    image_refs.append(photo)
                except Exception as e:
                    print(f"Error loading image: {e}")
                    # If image fails to load, add a placeholder
                    image_refs.append(None)
            
            # Remove loading label after images are loaded
            loading_label.destroy()
            
            # Place the image label in the center
            img_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Function to update displayed image
            def update_image():
                if image_refs and current_index[0] < len(image_refs) and image_refs[current_index[0]]:
                    img_label.config(image=image_refs[current_index[0]])
                    counter_label.config(text=f"{current_index[0]+1}/{len(image_refs)}")
                else:
                    img_label.config(image="", text="Image Error")
            
            # Function to open the embedded viewer
            def open_viewer(event=None):
                if images_data:
                    # Create the embedded viewer with the current index
                    viewer = EmbeddedImageViewer(
                        self, 
                        self.main_frame, 
                        images_data, 
                        return_callback,  # Use the provided return callback
                        standard_size=(800, 600)  # Larger standard size for all images
                    )
                    viewer.current_index = current_index[0]
                    viewer.show_image()
            
            # Bind click event to open viewer
            img_label.bind("<Button-1>", open_viewer)
            
            # Navigation functions
            def prev_image():
                if image_refs:
                    current_index[0] = (current_index[0] - 1) % len(image_refs)
                    update_image()
                    counter_label.config(text=f"{current_index[0]+1}/{len(image_refs)}")
                    
            def next_image():
                if image_refs:
                    current_index[0] = (current_index[0] + 1) % len(image_refs)
                    update_image()
                    counter_label.config(text=f"{current_index[0]+1}/{len(image_refs)}")
            
            # Add navigation buttons if there are multiple images
            buttons_container = ttk.Frame(gallery_frame, style="TFrame")
            buttons_container.pack(anchor="center")
            
            if len(image_refs) > 1:
                prev_btn = ttk.Button(
                    buttons_container, 
                    text="<", 
                    command=prev_image, 
                    style="Primary.TButton",
                    width=3,
                    padding=(5, 2)
                )
                prev_btn.pack(side="left", padx=5)
                
                counter_label = ttk.Label(buttons_container, text=f"1/{len(image_refs)}")
                counter_label.pack(side="left", padx=10)
                
                next_btn = ttk.Button(
                    buttons_container, 
                    text=">", 
                    command=next_image, 
                    style="Primary.TButton",
                    width=3,
                    padding=(5, 2)
                )
                next_btn.pack(side="left", padx=5)
            else:
                # Just show image count if only one image
                counter_label = ttk.Label(buttons_container, text="1/1")
                counter_label.pack(side="left", padx=10)
            
            # Display the first image
            update_image()
            
            # Store references in the frame to prevent garbage collection
            gallery_frame.image_refs = image_refs
            
            return gallery_frame
            
        except Exception as e:
            print(f"Error creating image gallery: {e}")
            # Return a basic frame if gallery creation fails
            error_frame = ttk.Frame(parent_frame, style="TFrame")
            ttk.Label(error_frame, text="Error loading gallery").pack()
            return error_frame

    def show_available_items(self):
        self.clear_frame()
        self.update_header("Available Auctions")
        
        self.show_loading(True)
        
        # Get available items from database
        available_items = self.db_manager.get_available_items(exclude_seller=self.current_user)
        
        # Simulate network delay for loading items
        self.root.after(800, lambda: self._display_available_items(available_items))
    
    def _display_available_items(self, available_items):
        """Display available items after loading"""
        # Create a canvas with scrollbar for many items
        canvas = tk.Canvas(self.main_frame, bg=BidStreamUI.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        
        # Configure scrolling
        def _on_mousewheel(event):
            # Only scroll if the canvas exists and has items
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            # Bind mousewheel only when mouse enters the canvas
            if canvas.winfo_exists():
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                
        def _unbind_mousewheel(event):
            # Unbind mousewheel when mouse leaves the canvas
            if canvas.winfo_exists():
                canvas.unbind_all("<MouseWheel>")
        
        # Bind mousewheel events to the canvas instead of binding globally
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        
        def _on_frame_configure(event):
            if canvas.winfo_exists():
                canvas.configure(scrollregion=canvas.bbox("all"))
                # Set a fixed width for the scrollable frame to prevent content from expanding
                canvas.itemconfig(frame_window, width=canvas.winfo_width())
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        
        # Create window in canvas with fixed width
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas to expand horizontally but maintain a fixed width for content
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure main frame grid
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Check if there are any available items
        if not available_items:
            # No items available message
            no_items_frame = ttk.Frame(scrollable_frame, style="TFrame", padding=BidStreamUI.LARGE_PADDING)
            no_items_frame.pack(pady=BidStreamUI.LARGE_PADDING, padx=BidStreamUI.LARGE_PADDING, fill="x")
            
            ttk.Label(
                no_items_frame, 
                text="No items available for bidding", 
                style="Header.TLabel"
            ).pack(anchor="center", pady=BidStreamUI.LARGE_PADDING)
            
            ttk.Label(
                no_items_frame, 
                text="Check back later or list your own items for others to bid on", 
                style="Light.TLabel"
            ).pack(anchor="center", pady=BidStreamUI.PADDING)
        else:
            # Display available items
            for item_id, item in available_items:
                # Create a card for each item
                item_card = BidStreamUI.create_card_frame(scrollable_frame, padding=BidStreamUI.PADDING)
                item_card.pack(pady=10, padx=20, fill="x")
                
                # Create a container for the item content
                item_content = ttk.Frame(item_card, style="TFrame")
                item_content.pack(fill="x", expand=True)
                
                # Create a frame for the image gallery
                img_gallery_frame = ttk.Frame(item_content, style="TFrame")
                img_gallery_frame.pack(side="left", padx=10, pady=10)
                
                # Display the first image if available
                if item.get("images_data") and len(item["images_data"]) > 0:
                    # Create image display with navigation, passing the return callback
                    self.create_image_gallery(img_gallery_frame, item["images_data"], 120, self.show_available_items)
                else:
                    ttk.Label(img_gallery_frame, text="No Image").pack()
                
                # Item details
                details_frame = ttk.Frame(item_content, style="TFrame")
                details_frame.pack(side="left", padx=10, fill="x", expand=True)
                
                # Item name with badge for time remaining
                name_frame = ttk.Frame(details_frame, style="TFrame")
                name_frame.pack(anchor="w", fill="x", pady=(0, 5))
                
                ttk.Label(name_frame, text=f"{item['name']}", style="Header.TLabel").pack(side="left")
                
                # Time remaining badge
                time_remaining = BidStreamUI.format_time_remaining(item['end_time'])
                time_badge = BidStreamUI.create_badge(
                    name_frame, 
                    time_remaining, 
                    BidStreamUI.SUCCESS_COLOR
                )
                time_badge.pack(side="left", padx=(10, 0))
                
                # Current bid with highlighted price
                ttk.Label(
                    details_frame, 
                    text=f"Current Bid: {BidStreamUI.format_currency(item['highest_bid'])}", 
                    style="Subheader.TLabel",
                    foreground=BidStreamUI.PRIMARY_COLOR
                ).pack(anchor="w", pady=2)
                
                # Display description if available (truncated if too long)
                if item.get("description"):
                    description = item["description"]
                    if len(description) > 100:
                        # Truncate long descriptions and add ellipsis
                        description = description[:100] + "..."
                    ttk.Label(details_frame, text=f"{description}", wraplength=400).pack(anchor="w", pady=5)
                
                # Time information
                time_frame = ttk.Frame(details_frame, style="TFrame")
                time_frame.pack(anchor="w", pady=5, fill="x")
                
                ttk.Label(time_frame, text=f"Started: {item['start_time'].strftime('%Y-%m-%d %H:%M')}", style="Light.TLabel").pack(anchor="w")
                
                # Calculate time remaining
                now = datetime.now()
                time_left = item['end_time'] - now
                hours_left = int(time_left.total_seconds() / 3600)
                minutes_left = int((time_left.total_seconds() % 3600) / 60)
                
                ttk.Label(
                    time_frame, 
                    text=f"Ends: {item['end_time'].strftime('%Y-%m-%d %H:%M')}", 
                    style="Light.TLabel"
                ).pack(anchor="w")
                
                # Bid button
                button_frame = ttk.Frame(item_content, style="TFrame")
                button_frame.pack(side="right", padx=15, pady=15, anchor="center")
                
                ttk.Button(
                    button_frame, 
                    text="Place Bid", 
                    command=lambda id=item_id: self.show_bid_screen(id),
                    style="Primary.TButton"
                ).pack(pady=5, ipady=10, ipadx=20, fill="x")

        # Back button at the bottom
        back_frame = ttk.Frame(self.main_frame, style="TFrame")
        back_frame.pack(side="bottom", fill="x", pady=10)
        
        ttk.Button(
            back_frame, 
            text="Back to Dashboard", 
            command=self.show_user_dashboard,
            style="Secondary.TButton"
        ).pack(side="left", padx=20, pady=10)
        
        # Cleanup function for mouse wheel binding when frame is destroyed
        def _cleanup():
            if canvas.winfo_exists():
                canvas.unbind_all("<MouseWheel>")
                canvas.unbind('<Enter>')
                canvas.unbind('<Leave>')
        
        # Bind cleanup to frame destruction
        self.main_frame.bind("<Destroy>", lambda e: _cleanup())
        
        self.show_loading(False)

    def show_bid_screen(self, item_id):
        """Show the bid screen with scrollable content"""
        self.clear_frame()
        
        self.update_header("Bid on Item")
        
        self.show_loading(True)
        
        # Get item details from database
        item = self.db_manager.get_item(item_id)
        
        # Simulate network delay for loading bid details
        self.root.after(600, lambda: self._display_bid_screen(item_id, item))

    def _display_bid_screen(self, item_id, item):
        """Display the bid screen with an enlarged item detail box"""
        self.clear_frame()
        self.update_header("Bid on Item")
        
        # Create a main container frame with proper padding
        main_container = ttk.Frame(self.main_frame, style="TFrame", padding=(20, 10))
        main_container.pack(fill="both", expand=True)
        
        # Create a canvas with scrollbar for scrolling content
        canvas = tk.Canvas(main_container, bg=BidStreamUI.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        
        # Configure scrolling
        def _on_mousewheel(event):
            # Only scroll if the canvas exists and has items
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            # Bind mousewheel only when mouse enters the canvas
            if canvas.winfo_exists():
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                
        def _unbind_mousewheel(event):
            # Unbind mousewheel when mouse leaves the canvas
            if canvas.winfo_exists():
                canvas.unbind_all("<MouseWheel>")
        
        # Bind mousewheel events to the canvas instead of binding globally
        canvas.bind('<Enter>', _bind_mousewheel)
        canvas.bind('<Leave>', _unbind_mousewheel)
        
        def _on_frame_configure(event):
            if canvas.winfo_exists():
                canvas.configure(scrollregion=canvas.bbox("all"))
                # Set a fixed width for the scrollable frame to prevent content from expanding
                canvas.itemconfig(frame_window, width=canvas.winfo_width())
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        
        # Create window in canvas with fixed width
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Configure canvas to expand horizontally but maintain a fixed width for content
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure main_container grid
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Create a navigation buttons frame at the top
        nav_buttons_frame = ttk.Frame(scrollable_frame, style="TFrame")
        nav_buttons_frame.pack(fill="x", pady=(0, 20))
        
        # Back button at the top left
        back_button = ttk.Button(
            nav_buttons_frame,
            text="Back",
            command=self.show_available_items,
            style="Secondary.TButton"
        )
        back_button.pack(side="left")
        
        # Create a frame to center the item detail box
        center_frame = ttk.Frame(scrollable_frame, style="TFrame")
        center_frame.pack(fill="both", expand=True)
        
        # Configure the center frame to center its contents
        center_frame.columnconfigure(0, weight=1)
        center_frame.columnconfigure(1, weight=0)
        center_frame.columnconfigure(2, weight=1)
        center_frame.rowconfigure(0, weight=1)
        center_frame.rowconfigure(1, weight=0)
        center_frame.rowconfigure(2, weight=1)
        
        # Create a larger item detail box
        item_detail_box = BidStreamUI.create_card_frame(center_frame, padding=30)  # Increased padding
        item_detail_box.grid(row=1, column=1)
        
        # Set a fixed width for the item detail box to make it larger
        item_detail_box.config(width=1000)  # Increased width from 800 to 1000
        
        # Item header with status badge
        header_frame = ttk.Frame(item_detail_box, style="Card.TFrame")
        header_frame.pack(fill="x", pady=(0, 25), padx=15)  # Increased padding
        
        # Item name with larger font
        item_name_label = ttk.Label(
            header_frame, 
            text=item['name'], 
            style="Header.TLabel",
            font=("Helvetica", 32, "bold")  # Increased font size from 26 to 32
        )
        item_name_label.pack(side="left", pady=15)  # Increased padding
        
        # Status badge
        status_badge = BidStreamUI.create_badge(
            header_frame, 
            "Active Auction", 
            BidStreamUI.SUCCESS_COLOR,
            font=("Helvetica", 16)  # Increased font size from 14 to 16
        )
        status_badge.pack(side="right", pady=15, padx=15)  # Increased padding
        
        # Image gallery section with larger images
        gallery_frame = ttk.Frame(item_detail_box, style="Card.TFrame")
        gallery_frame.pack(pady=(0, 30), anchor="center", padx=25)  # Increased padding
        
        # Create image gallery with larger images and proper return callback
        if item.get("images_data"):
            self.create_image_gallery(
                gallery_frame, 
                item["images_data"], 
                500,  # Increased image size from 400 to 500
                lambda: self.show_bid_screen(item_id)  # Return to this specific bid screen
            )
        
        # Current bid information
        bid_info_frame = ttk.Frame(item_detail_box, style="Card.TFrame")
        bid_info_frame.pack(pady=(0, 30), anchor="center", padx=25, fill="x")  # Increased padding
        
        # Larger bid text
        ttk.Label(
            bid_info_frame, 
            text=f"Current Highest Bid: {BidStreamUI.format_currency(item['highest_bid'])}", 
            style="Header.TLabel",
            foreground=BidStreamUI.PRIMARY_COLOR,
            font=("Helvetica", 28, "bold")  # Increased font size from 22 to 28
        ).pack(pady=20, anchor="center")  # Increased padding
        
        # Time remaining information
        time_remaining = BidStreamUI.format_time_remaining(item['end_time'])
        ttk.Label(
            bid_info_frame,
            text=f"Time Remaining: {time_remaining}",
            style="Subheader.TLabel",
            font=("Helvetica", 22)  # Increased font size from 18 to 22
        ).pack(pady=20, anchor="center")  # Increased padding

        # Description section with scrollable text
        if item.get("description"):
            desc_frame = ttk.LabelFrame(item_detail_box, text="Item Description", style="TLabelframe")
            desc_frame.pack(pady=(0, 20), fill="x", anchor="center", padx=25)
            
            desc_text = scrolledtext.ScrolledText(
                desc_frame, 
                wrap=tk.WORD, 
                height=6, 
                width=60, 
                font=BidStreamUI.BODY_FONT,
                background="white"
            )
            desc_text.insert("1.0", item["description"])
            desc_text.config(state="disabled")  # Make it read-only
            desc_text.pack(pady=10, padx=10, fill="both", expand=True)

        # Bidding section
        bid_section = ttk.Frame(item_detail_box, style="Card.TFrame")
        bid_section.pack(pady=(0, 20), anchor="center", padx=25, fill="x")
        
        # Create a container for the bid input
        bid_input_container = ttk.Frame(bid_section, style="TFrame")
        bid_input_container.pack(anchor="center", pady=10)
        
        ttk.Label(bid_input_container, text="Your Bid:", style="Subheader.TLabel").pack(side="left", padx=5)
        self.bid_entry = ttk.Entry(bid_input_container, width=20, font=BidStreamUI.BODY_FONT)
        self.bid_entry.pack(side="left", padx=5)
        
        # Minimum bid hint
        min_bid = item['highest_bid'] + 0.01
        ttk.Label(
            bid_section,
            text=f"Minimum bid: {BidStreamUI.format_currency(min_bid)}",
            style="Light.TLabel"
        ).pack(anchor="center")
        
        # Place Bid button
        ttk.Button(
            bid_section,
            text="Place Bid",
            command=lambda: self.place_bid(item_id),
            style="Primary.TButton",
            padding=(20, 10)  # Increased padding for larger button
        ).pack(pady=(10, 0))
        
        # Seller information
        seller_frame = ttk.Frame(item_detail_box, style="Card.TFrame")
        seller_frame.pack(pady=(0, 30), anchor="center", padx=25, fill="x")  # Increased padding
        
        ttk.Label(
            seller_frame,
            text=f"Seller: {item['seller']}",
            style="Subheader.TLabel",
            font=("Helvetica", 20)  # Increased font size from 16 to 20
        ).pack(pady=20, anchor="center")  # Increased padding
        
        # Cleanup function for mouse wheel binding when frame is destroyed
        def _cleanup():
            canvas.unbind_all("<MouseWheel>")
        
        # Bind cleanup to frame destruction
        self.main_frame.bind("<Destroy>", lambda e: _cleanup())
        
        self.show_loading(False)

    def place_bid(self, item_id):
        """Handle placing a bid on an item"""
        bid = self.bid_entry.get()

        if bid:
            try:
                bid = float(bid)
                self.show_loading(True)
                
                # Place bid in database
                success, result = self.db_manager.place_bid(item_id, self.current_user, bid)
                
                self.show_loading(False)
                
                if success:
                    messagebox.showinfo("Success", f"Your bid of {BidStreamUI.format_currency(bid)} has been placed successfully!")
                    self.show_available_items()
                else:
                    messagebox.showerror("Error", f"Failed to place bid: {result}")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid bid amount")
        else:
            messagebox.showerror("Error", "Please enter a bid amount")

    def show_all_items(self):
        self.clear_frame()
        self.update_header("Manage All Auctions")
        
        self.show_loading(True)
        
        # Get all items from database
        all_items = self.db_manager.get_all_items()
        
        # Simulate network delay for loading items
        self.root.after(800, lambda: self._display_all_items(all_items))
    
    def _display_all_items(self, all_items):
        """Display all items after loading"""
        # Create a canvas with scrollbar for many items
        canvas = tk.Canvas(self.main_frame, bg=BidStreamUI.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not all_items:
            # No items message
            no_items_frame = ttk.Frame(scrollable_frame, style="TFrame", padding=BidStreamUI.LARGE_PADDING)
            no_items_frame.pack(pady=BidStreamUI.LARGE_PADDING, padx=BidStreamUI.LARGE_PADDING, fill="x")
            
            ttk.Label(
                no_items_frame, 
                text="No items available", 
                style="Header.TLabel"
            ).pack(anchor="center", pady=BidStreamUI.LARGE_PADDING)
        else:
            # Display all items
            for item_id, item in all_items:
                # Create a card for each item
                item_card = BidStreamUI.create_card_frame(scrollable_frame, padding=BidStreamUI.PADDING)
                item_card.pack(pady=10, padx=20, fill="x")
                
                # Create a container for the item content
                item_content = ttk.Frame(item_card, style="TFrame")
                item_content.pack(fill="x", expand=True)
                
                # Create a frame for the image gallery
                img_gallery_frame = ttk.Frame(item_content, style="TFrame")
                img_gallery_frame.pack(side="left", padx=10, pady=10)
                
                # Display images if available with proper return callback
                if item.get("images_data") and len(item["images_data"]) > 0:
                    self.create_image_gallery(img_gallery_frame, item["images_data"], 100, self.show_all_items)
                else:
                    ttk.Label(img_gallery_frame, text="No Image").pack()
                
                # Item details
                details_frame = ttk.Frame(item_content, style="TFrame")
                details_frame.pack(side="left", padx=10, fill="x", expand=True)
                
                # Item ID and name
                id_name_frame = ttk.Frame(details_frame, style="TFrame")
                id_name_frame.pack(anchor="w", fill="x")
                
                ttk.Label(id_name_frame, text=f"ID: {item_id}", style="Light.TLabel").pack(side="left")
                
                # Status badge
                status_text = BidStreamUI.get_status_text(item["is_active"])
                status_color = BidStreamUI.get_status_color(item["is_active"])
                status_badge = BidStreamUI.create_badge(id_name_frame, status_text, status_color)
                status_badge.pack(side="right")
                
                ttk.Label(details_frame, text=f"{item['name']}", style="Header.TLabel").pack(anchor="w", pady=(5, 10))
                ttk.Label(details_frame, text=f"Seller: {item['seller']}").pack(anchor="w", pady=(5, 10))
                
                # Bid information with highlighted price
                ttk.Label(
                    details_frame, 
                    text=f"Highest Bid: {BidStreamUI.format_currency(item['highest_bid'])}", 
                    style="Subheader.TLabel",
                    foreground=BidStreamUI.PRIMARY_COLOR
                ).pack(anchor="w", pady=2)
                
                ttk.Label(details_frame, text=f"Highest Bidder: {item['highest_bidder'] or 'N/A'}").pack(anchor="w")
                
                # Display description if available (truncated)
                if item.get("description"):
                    description = item["description"]
                    if len(description) > 50:
                        description = description[:50] + "..."
                    ttk.Label(details_frame, text=f"Description: {description}").pack(anchor="w")
                
                # Time information
                time_frame = ttk.Frame(details_frame, style="TFrame")
                time_frame.pack(anchor="w", pady=5, fill="x")
                
                ttk.Label(time_frame, text=f"Start: {item['start_time'].strftime('%Y-%m-%d %H:%M')}", style="Light.TLabel").pack(anchor="w")
                ttk.Label(time_frame, text=f"End: {item['end_time'].strftime('%Y-%m-%d %H:%M')}", style="Light.TLabel").pack(anchor="w")
                
                # View full description button
                if item.get("description"):
                    ttk.Button(
                        details_frame, 
                        text="View Full Description", 
                        command=lambda id=item_id: self.show_item_description(id, "all_items"),
                        style="Outline.TButton"
                    ).pack(anchor="w", pady=2)
                
                # Action button
                button_frame = ttk.Frame(item_content, style="TFrame")
                button_frame.pack(side="right", padx=15, pady=15, anchor="center")
                
                if item["is_active"]:
                    ttk.Button(
                        button_frame, 
                        text="Close Auction", 
                        command=lambda id=item_id: self.close_bid(id),
                        style="Accent.TButton"
                    ).pack(pady=5, ipady=5, ipadx=10)
                else:
                    status_label = ttk.Label(
                        button_frame, 
                        text="CLOSED", 
                        background=BidStreamUI.ACCENT_COLOR,
                        foreground="white",
                        padding=10
                    )
                    status_label.pack(pady=5)

        # Back button at the bottom
        back_frame = ttk.Frame(self.main_frame, style="TFrame")
        back_frame.pack(side="bottom", fill="x", pady=10)
        
        ttk.Button(
            back_frame, 
            text="Back to Dashboard", 
            command=self.show_admin_dashboard,
            style="Secondary.TButton"
        ).pack(side="left", padx=20, pady=10)
        
        self.show_loading(False)
    
    def show_item_description(self, item_id, return_page=None):
        """Show a popup with the full item description"""
        item = self.db_manager.get_item(item_id)
        if not item or not item.get("description"):
            return
        
        # Store the current frame content
        self.clear_frame()
        self.update_header(f"Item Description: {item['name']}")
        
        # Create main container
        main_container = ttk.Frame(self.main_frame, style="TFrame", padding=20)
        main_container.pack(fill="both", expand=True)
        
        # Add a back button at the top
        back_frame = ttk.Frame(main_container, style="TFrame")
        back_frame.pack(fill="x", pady=(0, 20))
        
        # Determine which page to return to
        def go_back():
            if return_page == "all_items":
                self.show_all_items()
            elif return_page == "previous_bidded":
                self.show_previous_bidded_items()
            elif return_page == "available_items":
                self.show_available_items()
            else:
                self.show_user_dashboard()
        
        ttk.Button(
            back_frame,
            text="Back",
            command=go_back,
            style="Secondary.TButton"
        ).pack(side="left")
        
        # Add description content
        content_frame = BidStreamUI.create_card_frame(main_container, padding=20)
        content_frame.pack(fill="both", expand=True)
        
        # Item name and details
        ttk.Label(
            content_frame,
            text=item['name'],
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 10))
        
        # Add a scrolled text widget to display the description
        desc_text = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD,
            font=BidStreamUI.BODY_FONT,
            bg="white",
            height=20
        )
        desc_text.pack(fill="both", expand=True)
        
        # Insert the description
        desc_text.insert("1.0", item["description"])
        desc_text.config(state="disabled")  # Make it read-only

    def show_bid_report(self):
        """Show the bid report table with statistics"""
        self.clear_frame()
        self.update_header("Auction Analytics")
        
        self.show_loading(True)
        
        # Simulate network delay for loading report data
        self.root.after(1000, self._display_bid_report)
    
    def _display_bid_report(self):
        """Display the bid report after loading"""
        # Create a main container
        main_container = ttk.Frame(self.main_frame, style="TFrame")
        main_container.pack(fill="both", expand=True, pady=10)
        
        # Add a title and back button section
        title_section = ttk.Frame(main_container, style="TFrame")
        title_section.pack(fill="x", pady=(0, 15))
        
        # Add back button
        ttk.Button(
            title_section,
            text="Back",
            command=self.show_admin_dashboard,
            style="Secondary.TButton"
        ).pack(side="left", anchor="w")

        # Create filter and sort controls
        control_frame = ttk.Frame(main_container, style="TFrame")
        control_frame.pack(fill="x", pady=10)
        
        # Filter controls
        filter_frame = ttk.Frame(control_frame, style="TFrame")
        filter_frame.pack(side="left", padx=10)
        
        ttk.Label(filter_frame, text="Filter:").pack(side="left", padx=5)
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                    values=["All", "Active", "Closed"], width=10, 
                                    state="readonly")
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind("<<ComboboxSelected>>", self.update_report_table)
        
        # Sort controls
        sort_frame = ttk.Frame(control_frame, style="TFrame")
        sort_frame.pack(side="right", padx=10)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side="left", padx=5)
        self.sort_var = tk.StringVar(value="Item ID")
        sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var, 
                                  values=["Item ID", "Item Name", "Starting Price", "Highest Bid"], width=15,
                                  state="readonly")
        sort_combo.pack(side="left", padx=5)
        sort_combo.bind("<<ComboboxSelected>>", self.update_report_table)
        
        # Create table frame with proper expansion
        table_frame = ttk.Frame(main_container, style="TFrame")
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Create Treeview for the table
        columns = ("item_id", "item_name", "starting_price", "highest_bid", 
                   "highest_bidder", "status", "start_time", "end_time")
        
        self.report_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define column headings
        self.report_tree.heading("item_id", text="Item ID")
        self.report_tree.heading("item_name", text="Item Name")
        self.report_tree.heading("starting_price", text="Starting Price")
        self.report_tree.heading("highest_bid", text="Highest Bid")
        self.report_tree.heading("highest_bidder", text="Highest Bidder")
        self.report_tree.heading("status", text="Status")
        self.report_tree.heading("start_time", text="Start Time")
        self.report_tree.heading("end_time", text="End Time")
        
        # Define column widths
        self.report_tree.column("item_id", width=70, anchor="center")
        self.report_tree.column("item_name", width=150)
        self.report_tree.column("starting_price", width=100, anchor="center")
        self.report_tree.column("highest_bid", width=100, anchor="center")
        self.report_tree.column("highest_bidder", width=100, anchor="center")
        self.report_tree.column("status", width=80, anchor="center")
        self.report_tree.column("start_time", width=150, anchor="center")
        self.report_tree.column("end_time", width=150, anchor="center")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.report_tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.report_tree.xview)
        self.report_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for table and scrollbars
        self.report_tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Back button frame at the bottom
        button_frame = ttk.Frame(main_container, style="TFrame")
        button_frame.pack(fill="x", pady=(10, 0), padx=20)

        # Back to Dashboard button - right-aligned, blue color, larger size
        ttk.Button(
            button_frame, 
            text="Back to Dashboard", 
            command=self.show_admin_dashboard,
            style="Primary.TButton",
            padding=(20, 10)  # Increased padding for larger button
        ).pack(side="right")

        # Back button - right-aligned, secondary color
        ttk.Button(
            button_frame, 
            text="Back", 
            command=self.show_admin_dashboard,
            style="Secondary.TButton",
            padding=(10, 5)  # Smaller padding for secondary button
        ).pack(side="right", padx=(0, 10))
        
        # Populate the table initially
        self.update_report_table()
        
        self.show_loading(False)
        
    def update_report_table(self, event=None):
        """Update the report table based on filter and sort settings"""
        # Clear existing items
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        
        # Get filter and sort settings
        filter_value = self.filter_var.get()
        sort_value = self.sort_var.get()
        
        # Convert filter value to database format
        filter_status = None
        if filter_value == "Active":
            filter_status = "active"
        elif filter_value == "Closed":
            filter_status = "closed"
        
        # Get report data from database
        report_data = self.db_manager.get_bid_report(filter_status, sort_value)
        
        # Insert items into the table
        for item in report_data:
            status = "Active" if item["status"] == "active" else "Closed"
            start_time = item["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            end_time = item["closed_at"].strftime("%Y-%m-%d %H:%M:%S") if item["closed_at"] else "N/A"
            
            self.report_tree.insert("", "end", iid=str(item["id"]), values=(
                item["id"],
                item["title"],
                BidStreamUI.format_currency(float(item["starting_price"])),
                BidStreamUI.format_currency(float(item["current_price"])),
                item["highest_bidder"] or "N/A",
                status,
                start_time,
                end_time
            ))
    
    def close_bid(self, item_id):
        self.show_loading(True)
        
        # Close auction in database
        success, result = self.db_manager.close_auction(item_id)
        
        self.show_loading(False)
        
        if success:
            messagebox.showinfo("Auction Closed", "The auction has been closed successfully")
            
            # Return to the appropriate screen based on user type
            if self.db_manager.is_admin(self.current_user):
                self.show_all_items()
            else:
                self.show_previous_bidded_items()
        else:
            messagebox.showerror("Error", f"Failed to close auction: {result}")

    def check_auction_status(self):
        """Check for expired auctions and close them"""
        try:
            # Check expired auctions in database
            closed_count = self.db_manager.check_expired_auctions()
            if closed_count > 0:
                print(f"Automatically closed {closed_count} expired auctions")
        except Exception as e:
            print(f"Error in check_auction_status: {e}")
        finally:
            # Always schedule the next check
            self.root.after(10000, self.check_auction_status)  # Check every 10 seconds

    def show_previous_bidded_items(self):
        self.clear_frame()
        self.update_header("My Listed Items")
        
        self.show_loading(True)
        
        # Get user's items from database
        user_items = self.db_manager.get_user_items(self.current_user)
        
        # Simulate network delay for loading items
        self.root.after(800, lambda: self._display_previous_bidded_items(user_items))
    
    def _display_previous_bidded_items(self, user_items):
        """Display previous bidded items after loading"""
        # Create a canvas with scrollbar for many items
        canvas = tk.Canvas(self.main_frame, bg=BidStreamUI.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if not user_items:
            # No items message
            no_items_frame = ttk.Frame(scrollable_frame, style="TFrame", padding=BidStreamUI.LARGE_PADDING)
            no_items_frame.pack(pady=BidStreamUI.LARGE_PADDING, padx=BidStreamUI.LARGE_PADDING, fill="x")
            
            ttk.Label(
                no_items_frame, 
                text="You haven't listed any items yet", 
                style="Header.TLabel"
            ).pack(anchor="center", pady=BidStreamUI.LARGE_PADDING)
            
            ttk.Button(
                no_items_frame,
                text="List an Item Now",
                command=self.show_list_item_details,
                style="Primary.TButton"
            ).pack(pady=BidStreamUI.PADDING, ipady=5, ipadx=20)
        else:
            # Display user's items
            for item_id, item in user_items:
                # Create a card for each item
                item_card = BidStreamUI.create_card_frame(scrollable_frame, padding=BidStreamUI.PADDING)
                item_card.pack(pady=10, padx=20, fill="x")
                
                # Create a container for the item content
                item_content = ttk.Frame(item_card, style="TFrame")
                item_content.pack(fill="x", expand=True)
                
                # Create a frame for the image gallery
                img_gallery_frame = ttk.Frame(item_content, style="TFrame")
                img_gallery_frame.pack(side="left", padx=10, pady=10)
                
                # Display images if available with proper return callback
                if item.get("images_data") and len(item["images_data"]) > 0:
                    self.create_image_gallery(img_gallery_frame, item["images_data"], 100, self.show_previous_bidded_items)
                else:
                    ttk.Label(img_gallery_frame, text="No Image").pack()
                
                # Item details
                details_frame = ttk.Frame(item_content, style="TFrame")
                details_frame.pack(side="left", padx=10, fill="x", expand=True)
                
                # Item name with status badge
                name_frame = ttk.Frame(details_frame, style="TFrame")
                name_frame.pack(anchor="w", fill="x", pady=(0, 5))
                
                ttk.Label(name_frame, text=f"{item['name']}", style="Header.TLabel").pack(side="left")
                
                # Status badge
                status_text = BidStreamUI.get_status_text(item["is_active"])
                status_color = BidStreamUI.get_status_color(item["is_active"])
                status_badge = BidStreamUI.create_badge(name_frame, status_text, status_color)
                status_badge.pack(side="left", padx=(10, 0))
                
                ttk.Label(details_frame, text=f"Starting Price: {BidStreamUI.format_currency(item['price'])}").pack(anchor="w")
                
                # Current bid with highlighted price
                ttk.Label(
                    details_frame, 
                    text=f"Current Bid: {BidStreamUI.format_currency(item['highest_bid'])}", 
                    style="Subheader.TLabel",
                    foreground=BidStreamUI.PRIMARY_COLOR
                ).pack(anchor="w", pady=2)
                
                # Display description if available (truncated)
                if item.get("description"):
                    description = item["description"]
                    if len(description) > 50:
                        description = description[:50] + "..."
                    ttk.Label(details_frame, text=f"Description: {description}").pack(anchor="w")
                
                # Time information
                time_frame = ttk.Frame(details_frame, style="TFrame")
                time_frame.pack(anchor="w", pady=5, fill="x")
                
                ttk.Label(time_frame, text=f"Started: {item['start_time'].strftime('%Y-%m-%d %H:%M')}", style="Light.TLabel").pack(anchor="w")
                
                # Time remaining or end time
                if item["is_active"]:
                    time_remaining = BidStreamUI.format_time_remaining(item['end_time'])
                    ttk.Label(time_frame, text=f"Time Remaining: {time_remaining}", style="Light.TLabel").pack(anchor="w")
                else:
                    ttk.Label(time_frame, text=f"Ended: {item['end_time'].strftime('%Y-%m-%d %H:%M')}", style="Light.TLabel").pack(anchor="w")
                
                # View full description button
                if item.get("description"):
                    ttk.Button(
                        details_frame, 
                        text="View Full Description", 
                        command=lambda id=item_id: self.show_item_description(id, "previous_bidded"),
                        style="Outline.TButton"
                    ).pack(anchor="w", pady=2)

        # Back button at the bottom
        back_frame = ttk.Frame(self.main_frame, style="TFrame")
        back_frame.pack(side="bottom", fill="x", pady=10)
        
        ttk.Button(
            back_frame, 
            text="Back to Dashboard", 
            command=self.show_user_dashboard,
            style="Secondary.TButton"
        ).pack(side="left", padx=20, pady=10)
        
        self.show_loading(False)

    def check_won_auctions(self):
        """Check for auctions won by the current user"""
        won_auctions = self.db_manager.get_won_auctions(self.current_user)
        
        if won_auctions:
            message = "Congratulations! You have won the following auctions:\n\n"
            for auction in won_auctions:
                message += f"• {auction['title']} for {BidStreamUI.format_currency(float(auction['winning_price']))}\n"
            messagebox.showinfo("Auction Won", message)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BiddingApp(root)
    app.check_auction_status()  # Start checking auction status
    root.mainloop()

