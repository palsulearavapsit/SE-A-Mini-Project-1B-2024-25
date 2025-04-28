import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import calendar
import os

class CalendarPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0)
        self.master = master
        self.app = app
        
        # Initialize variables
        self.current_date = datetime.now().replace(day=1)  # First day of the month
        self.selected_date = datetime.now()  # Today's date
        self.events = {}  # Store events by date
        self.event_widgets = []
        self.event_memory = []  # In-memory storage to replace JSON files
        
        # Create UI elements
        self.create_ui()
        
        # Render the calendar
        self.render_calendar()
        
        # Load sample events for demonstration
        self.load_sample_events()
    
    def create_ui(self):
        """Create main UI components"""
        # Set the background color
        self.configure(fg_color="#191919")
        
        # Main container with two columns (fullscreen layout)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure columns for calendar and events
        self.main_container.columnconfigure(0, weight=3)  # Calendar takes 3/4 of space
        self.main_container.columnconfigure(1, weight=1)  # Events take 1/4 of space
        
        # Create calendar view on the left
        self.create_calendar_view()
        
        # Create events panel on the right
        self.create_events_panel()
    
    def create_calendar_view(self):
        """Create the calendar view with month navigation and date grid"""
        # Calendar container
        self.calendar_frame = ctk.CTkFrame(self.main_container, fg_color="#1e1e1e", corner_radius=15)
        self.calendar_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        
        # Header with navigation and gradient background
        self.setup_calendar_header()
        
        # Days of week with improved styling
        self.weekdays_frame = ctk.CTkFrame(self.calendar_frame, fg_color="#252525", corner_radius=12)
        self.weekdays_frame.pack(fill="x", padx=20, pady=(0, 10), ipady=8)
        
        # Configure grid columns for days of week
        for i in range(7):
            self.weekdays_frame.columnconfigure(i, weight=1)
        
        # Add weekday labels with improved styling
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(weekdays):
            day_label = ctk.CTkLabel(
                self.weekdays_frame,
                text=day,
                font=("Arial", 14, "bold"),
                text_color="#cccccc" if i < 5 else "#ff9500",  # Orange for weekends
                width=40,
                height=30
            )
            day_label.grid(row=0, column=i, padx=5, pady=5)
        
        # Calendar days grid with improved styling
        self.days_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
        # Configure grid for the calendar days
        for i in range(6):  # 6 rows for days
            self.days_frame.rowconfigure(i, weight=1)
        for i in range(7):  # 7 columns for days
            self.days_frame.columnconfigure(i, weight=1)
        
        # Render the calendar
        self.render_calendar()
    
    def setup_calendar_header(self):
        """Setup calendar navigation header with month/year display and controls"""
        header_frame = ctk.CTkFrame(self.calendar_frame, fg_color="#252525", corner_radius=10, height=60)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        # Home button to return to dashboard
        home_btn = ctk.CTkButton(
            header_frame, 
            text="Home",
            font=("Arial", 14),
            width=70,
            height=40,
            corner_radius=8,
            fg_color="#333333",
            hover_color="#444444",
            text_color="white",
            command=self.app.show_dashboard_page
        )
        home_btn.pack(side="left", padx=15)
        
        # Left navigation button
        prev_btn = ctk.CTkButton(
            header_frame, 
            text="←",
            font=("Arial", 16, "bold"),
            width=40,
            height=40,
            corner_radius=8,
            fg_color="#333333",
            hover_color="#444444",
            text_color="white",
            command=self.prev_month
        )
        prev_btn.pack(side="left", padx=5)
        
        # Month and year label with larger, bolder font
        self.month_year_label = ctk.CTkLabel(
            header_frame, 
            text="",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        self.month_year_label.pack(side="left", expand=True)
        
        # "Today" button
        today_btn = ctk.CTkButton(
            header_frame, 
            text="Today",
            font=("Arial", 14),
            width=70,
            height=40,
            corner_radius=8,
            fg_color="#4361ee",
            hover_color="#3a56d4",
            text_color="white",
            command=self.go_to_today
        )
        today_btn.pack(side="left", padx=10)
        
        # Right navigation button
        next_btn = ctk.CTkButton(
            header_frame, 
            text="→",
            font=("Arial", 16, "bold"),
            width=40,
            height=40,
            corner_radius=8,
            fg_color="#333333",
            hover_color="#444444",
            text_color="white",
            command=self.next_month
        )
        next_btn.pack(side="left", padx=15)
    
    def render_calendar(self):
        """Render the calendar days for the current month"""
        # Clear previous calendar days
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # Get the first day of the month and the number of days
        year = self.current_date.year
        month = self.current_date.month
        
        # Update month label
        self.month_year_label.configure(text=self.current_date.strftime("%B %Y"))
        
        # Get the calendar for the current month
        cal = calendar.monthcalendar(year, month)
        
        # Get current date for highlighting
        today = datetime.now().date()
        
        # Store the day buttons to update with events
        self.day_buttons = {}
        
        # Render the days
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                if day == 0:
                    # Empty cell for days not in this month
                    spacer = ctk.CTkFrame(self.days_frame, fg_color="transparent")
                    spacer.grid(row=week_idx, column=day_idx, padx=5, pady=5, sticky="nsew")
                else:
                    # Create day frame that will hold the button and event dots
                    day_frame = ctk.CTkFrame(self.days_frame, fg_color="transparent")
                    day_frame.grid(row=week_idx, column=day_idx, padx=5, pady=5, sticky="nsew")
                    
                    # Configure the day frame grid
                    day_frame.rowconfigure(0, weight=1)  # Button row
                    day_frame.rowconfigure(1, weight=0)  # Event dots row
                    day_frame.columnconfigure(0, weight=1)
                    
                    # Date for this button
                    date_obj = datetime(year, month, day).date()
                    
                    # Determine day appearance based on type
                    is_weekend = day_idx >= 5  # Saturday or Sunday
                    is_today = date_obj == today
                    is_selected = date_obj == self.selected_date.date()
                    
                    # Day button appearance
                    if is_selected:
                        fg_color = "#2ecc71"  # Green for selected day
                        text_color = "white"
                        border_width = 0
                        border_color = None
                    elif is_today:
                        fg_color = "#1e1e1e"  # Same as background
                        text_color = "white"
                        border_width = 2  # Add border
                        border_color = "#3498db"  # Blue border
                    elif is_weekend:
                        fg_color = "#252525"  # Slightly lighter for weekends
                        text_color = "#ff9500"  # Orange text for weekends
                        border_width = 0
                        border_color = None
                    else:
                        fg_color = "#252525"  # Slightly lighter for normal days
                        text_color = "white"
                        border_width = 0
                        border_color = None
                    
                    # Create the day button with improved styling
                    day_btn = ctk.CTkButton(
                        day_frame,
                        text=str(day),
                        width=70,
                        height=55,
                        fg_color=fg_color,
                        text_color=text_color,
                        hover_color="#2ecc71" if not is_selected else "#27ae60",  # Always green hover
                        corner_radius=12,
                        border_width=border_width,
                        border_color=border_color,
                        font=("Arial", 16),
                        command=lambda d=day: self.select_date(d)
                    )
                    day_btn.grid(row=0, column=0, sticky="nsew")
                    
                    # Store the button reference
                    date_key = date_obj.strftime("%Y-%m-%d")
                    self.day_buttons[date_key] = {
                        'button': day_btn,
                        'frame': day_frame
                    }
        
        # Add event indicators
        self.update_event_indicators()
    
    def update_event_indicators(self):
        """Update the event dots for days with events"""
        # Clear any previous indicators first
        for date_key, components in self.day_buttons.items():
            frame = components['frame']
            # Remove any existing event indicators (row 1)
            for widget in frame.grid_slaves(row=1):
                widget.destroy()
        
        # Add indicators for days with events
        for date_key, events_list in self.events.items():
            if date_key in self.day_buttons and events_list:
                frame = self.day_buttons[date_key]['frame']
                
                # Create a frame to hold the event dots
                dots_frame = ctk.CTkFrame(frame, fg_color="transparent", height=10)
                dots_frame.grid(row=1, column=0, sticky="ew", pady=(2, 0))
                
                # Add up to 3 event dots with improved styling
                max_dots = min(3, len(events_list))
                for i in range(max_dots):
                    event_color = events_list[i].get('color', '#4361ee')
                    dot = ctk.CTkFrame(
                        dots_frame,
                        width=8,
                        height=8,
                        fg_color=event_color,
                        corner_radius=4
                    )
                    dot.pack(side="left", padx=2)
    
    def prev_month(self):
        """Navigate to the previous month"""
        # Calculate the first day of the previous month
        if self.current_date.month == 1:
            # If January, go to December of the previous year
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12, day=1)
        else:
            # Otherwise, just go to the previous month
            self.current_date = self.current_date.replace(month=self.current_date.month - 1, day=1)
        
        # Re-render the calendar
        self.render_calendar()
        
        # Update events for the new month
        self.load_events()
    
    def next_month(self):
        """Navigate to the next month"""
        # Calculate the first day of the next month
        if self.current_date.month == 12:
            # If December, go to January of the next year
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1, day=1)
        else:
            # Otherwise, just go to the next month
            self.current_date = self.current_date.replace(month=self.current_date.month + 1, day=1)
        
        # Re-render the calendar
        self.render_calendar()
        
        # Update events for the new month
        self.load_events()
    
    def go_to_today(self):
        """Navigate to today's date"""
        today = datetime.now()
        self.current_date = today.replace(day=1)  # First day of the current month
        self.selected_date = today
        
        # Re-render the calendar
        self.render_calendar()
        
        # Update the selected date display
        self.selected_date_label.configure(text=self.selected_date.strftime("%A, %B %d, %Y"))
        
        # Update events for today
        self.display_events_for_date(self.selected_date.date())
    
    def select_date(self, day):
        """Handle date selection in the calendar"""
        # Create a datetime object for the selected date
        selected = self.current_date.replace(day=day)
        self.selected_date = selected
        
        # Update the selected date display
        self.selected_date_label.configure(text=self.selected_date.strftime("%A, %B %d, %Y"))
        
        # Re-render the calendar to update the selection
        self.render_calendar()
        
        # Display events for the selected date
        self.display_events_for_date(selected.date())
    
    def load_events(self):
        """Load events from memory for the current month view"""
        try:
            # Clear current events
            self.events = {}
            
            # Calculate start and end date for the month view
            year = self.current_date.year
            month = self.current_date.month
            
            # Start from the beginning of the month
            start_date = datetime(year, month, 1).date()
            
            # End at the end of the month (calculate next month and go back a day)
            if month == 12:
                next_month = datetime(year + 1, 1, 1).date()
            else:
                next_month = datetime(year, month + 1, 1).date()
            end_date = next_month - timedelta(days=1)
            
            # Filter events for the current month view
            user_id = getattr(self.app, 'current_user_id', 1)  # Default to user_id 1 if not set
            
            for event in self.event_memory:
                if event.get('user_id') == user_id:
                    event_date = event.get('event_date')
                    # Check if event is within current month view
                    if start_date.strftime("%Y-%m-%d") <= event_date <= end_date.strftime("%Y-%m-%d"):
                        # Add event to the events dictionary
                        date_key = event_date
                        if date_key not in self.events:
                            self.events[date_key] = []
                        self.events[date_key].append(event)
            
            # Update the calendar with event indicators
            self.update_event_indicators()
            
            # Display events for the selected date
            self.display_events_for_date(self.selected_date.date())
        except Exception as err:
            print(f"Error loading events: {err}")
    
    def display_events_for_date(self, date):
        """Display events for the selected date"""
        # Clear previous event widgets
        for widget in self.events_list_frame.winfo_children():
            if widget != self.no_events_label:
                widget.destroy()
        
        # Get the date key
        date_key = date.strftime("%Y-%m-%d")
        
        # Get events for this date
        events_list = self.events.get(date_key, [])
        
        # Show or hide the "No events" label
        if not events_list:
            self.no_events_label.pack(pady=30)
        else:
            self.no_events_label.pack_forget()
            
            # Display each event
            for event in events_list:
                self.create_event_card(event)
    
    def create_event_card(self, event):
        """Create a card to display an event"""
        # Event card container with improved styling
        event_card = ctk.CTkFrame(self.events_list_frame, fg_color="#252525", corner_radius=12)
        event_card.pack(fill="x", pady=7, padx=5, ipady=8)
        
        # Add a colored indicator bar with improved styling
        color_bar = ctk.CTkFrame(
            event_card, 
            width=8, 
            fg_color=event.get('color', '#4361ee'),
            corner_radius=4
        )
        color_bar.pack(side="left", fill="y", padx=(8, 0), pady=10)
        
        # Event content
        content_frame = ctk.CTkFrame(event_card, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Event title with improved styling
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack(fill="x", anchor="w")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=event.get('title', 'Untitled Event'),
            font=("Arial", 16, "bold"),
            text_color="white",
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Category badge with improved styling
        category = event.get('category', 'Study')
        category_colors = {
            "Study": "#4361ee",  # Blue
            "Exam": "#e74c3c",   # Red
            "Revision": "#f39c12", # Orange
            "Break": "#2ecc71",  # Green
            "Other": "#9b59b6"   # Purple
        }
        
        category_label = ctk.CTkLabel(
            title_frame,
            text=category,
            font=("Arial", 11, "bold"),
            fg_color=category_colors.get(category, "#555555"),
            text_color="white",
            corner_radius=4,
            width=30,
            height=22
        )
        category_label.pack(side="left", padx=10)
        
        # Time information with improved styling
        if event.get('start_time'):
            time_text = f"⏱️ {event.get('start_time', '')}"
            if event.get('end_time'):
                time_text += f" - {event.get('end_time', '')}"
                
            time_label = ctk.CTkLabel(
                content_frame,
                text=time_text,
                font=("Arial", 13),
                text_color="#cccccc",
                anchor="w"
            )
            time_label.pack(fill="x", pady=(5, 0))
        
        # Description (if available) with improved styling
        if event.get('description'):
            desc_label = ctk.CTkLabel(
                content_frame,
                text=event.get('description', ''),
                font=("Arial", 13),
                justify="left",
                anchor="w",
                wraplength=250,
                text_color="#dddddd"
            )
            desc_label.pack(fill="x", pady=(5, 0))
        
        # Actions frame
        actions_frame = ctk.CTkFrame(event_card, fg_color="transparent", width=50)
        actions_frame.pack(side="right", fill="y", padx=5)
        
        # Delete button with improved styling
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="✕",
            width=30,
            height=30,
            fg_color="#cc3333",
            hover_color="#992222",
            text_color="white",
            corner_radius=15,
            command=lambda eid=event.get('id'): self.delete_event(eid)
        )
        delete_btn.pack(padx=10, pady=5)
    
    def show_add_event_dialog(self):
        """Show the Add Event dialog"""
        self.setup_add_event_dialog()
    
    def setup_add_event_dialog(self):
        """Set up the Add Event dialog"""
        self.event_dialog = ctk.CTkToplevel(self)
        self.event_dialog.title("Add Event")
        self.event_dialog.geometry("500x600")
        self.event_dialog.transient(self)
        self.event_dialog.protocol("WM_DELETE_WINDOW", self.close_event_dialog)
        
        # Event Dialog Title
        title_label = ctk.CTkLabel(
            self.event_dialog,
            text="Add New Event",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Event Title
        title_frame = ctk.CTkFrame(self.event_dialog, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Event Title",
            font=ctk.CTkFont(size=14)
        )
        title_label.pack(anchor="w")
        
        self.event_title_entry = ctk.CTkEntry(
            title_frame,
            width=440,
            height=35,
            placeholder_text="Enter event title"
        )
        self.event_title_entry.pack(pady=(5, 0))
        
        # Date and Time Frame
        datetime_frame = ctk.CTkFrame(self.event_dialog, fg_color="transparent")
        datetime_frame.pack(fill="x", padx=30, pady=10)
        
        # Date
        date_label = ctk.CTkLabel(
            datetime_frame,
            text="Date",
            font=ctk.CTkFont(size=14)
        )
        date_label.grid(row=0, column=0, sticky="w")
        
        self.event_date_entry = ctk.CTkEntry(
            datetime_frame,
            width=210,
            height=35,
            placeholder_text="YYYY-MM-DD"
        )
        # Set default date to currently selected date
        today = datetime.now().strftime("%Y-%m-%d")
        self.event_date_entry.insert(0, today)
        self.event_date_entry.grid(row=1, column=0, padx=(0, 10))
        
        # Time
        time_label = ctk.CTkLabel(
            datetime_frame,
            text="Time",
            font=ctk.CTkFont(size=14)
        )
        time_label.grid(row=0, column=1, sticky="w")
        
        time_frame = ctk.CTkFrame(datetime_frame, fg_color="transparent")
        time_frame.grid(row=1, column=1)
        
        self.event_start_time = ctk.CTkEntry(
            time_frame,
            width=100,
            height=35,
            placeholder_text="HH:MM"
        )
        self.event_start_time.insert(0, "10:00")
        self.event_start_time.pack(side="left")
        
        to_label = ctk.CTkLabel(time_frame, text="to", width=30)
        to_label.pack(side="left")
        
        self.event_end_time = ctk.CTkEntry(
            time_frame,
            width=100,
            height=35,
            placeholder_text="HH:MM"
        )
        self.event_end_time.insert(0, "11:00")
        self.event_end_time.pack(side="left")
        
        # Category
        category_frame = ctk.CTkFrame(self.event_dialog, fg_color="transparent")
        category_frame.pack(fill="x", padx=30, pady=10)
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="Category",
            font=ctk.CTkFont(size=14)
        )
        category_label.pack(anchor="w")
        
        self.event_category = ctk.CTkComboBox(
            category_frame,
            width=440,
            height=35,
            values=["Study", "Exam", "Assignment", "Meeting", "Other"]
        )
        self.event_category.set("Study")
        self.event_category.pack(pady=(5, 0))
        
        # Color
        color_frame = ctk.CTkFrame(self.event_dialog, fg_color="transparent")
        color_frame.pack(fill="x", padx=30, pady=10)
        
        color_label = ctk.CTkLabel(
            color_frame,
            text="Color",
            font=ctk.CTkFont(size=14)
        )
        color_label.pack(anchor="w", pady=(0, 10))
        
        colors_frame = ctk.CTkFrame(color_frame, fg_color="transparent")
        colors_frame.pack(fill="x")
        
        self.color_var = ctk.StringVar(value="blue")
        
        colors = [
            ("Blue", "#3a86ff", "blue"),
            ("Green", "#2ecc71", "green"),
            ("Red", "#e63946", "red"),
            ("Orange", "#ff9f1c", "orange"),
            ("Purple", "#8338ec", "purple")
        ]
        
        for i, (color_name, color_hex, color_value) in enumerate(colors):
            color_radio = ctk.CTkRadioButton(
                colors_frame,
                text=color_name,
                variable=self.color_var,
                value=color_value,
                fg_color=color_hex,
                border_color=color_hex
            )
            color_radio.pack(side="left", padx=10)
        
        # Description
        desc_frame = ctk.CTkFrame(self.event_dialog, fg_color="transparent")
        desc_frame.pack(fill="x", padx=30, pady=10)
        
        desc_label = ctk.CTkLabel(
            desc_frame,
            text="Description",
            font=ctk.CTkFont(size=14)
        )
        desc_label.pack(anchor="w")
        
        self.event_description = ctk.CTkTextbox(
            desc_frame,
            width=440,
            height=100
        )
        self.event_description.pack(pady=(5, 0))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.event_dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            height=35,
            fg_color="#555555",
            hover_color="#333333",
            command=self.close_event_dialog
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Event",
            width=100,
            height=35,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=self.save_event
        )
        save_btn.pack(side="right")
        
        # Center the dialog
        self.event_dialog.update_idletasks()
        width = self.event_dialog.winfo_width()
        height = self.event_dialog.winfo_height()
        x = (self.event_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.event_dialog.winfo_screenheight() // 2) - (height // 2)
        self.event_dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Make dialog modal
        self.event_dialog.grab_set()
    
    def close_event_dialog(self):
        """Close the event dialog"""
        self.event_dialog.grab_release()
        self.event_dialog.destroy()
    
    def save_event(self):
        """Save event to memory storage"""
        try:
            # Validate required fields
            event_title = self.event_title_entry.get().strip()
            event_date = self.event_date_entry.get().strip()
            
            if not event_title:
                messagebox.showerror("Error", "Event title is required")
                return
            
            if not event_date:
                messagebox.showerror("Error", "Event date is required")
                return
            
            # Validate date format
            if not self.validate_date(event_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Validate time formats if provided
            start_time = self.event_start_time.get().strip()
            end_time = self.event_end_time.get().strip()
            
            if start_time and not self.validate_time(start_time):
                messagebox.showerror("Error", "Invalid start time format. Use HH:MM")
                return
            
            if end_time and not self.validate_time(end_time):
                messagebox.showerror("Error", "Invalid end time format. Use HH:MM")
                return
            
            # Get user ID (default to 1 if not set)
            user_id = getattr(self.app, 'current_user_id', 1)
            
            # Get other event details
            description = self.event_description.get("1.0", "end-1c").strip()
            category = self.event_category.get()
            color = self.color_var.get()
            
            # Generate next ID
            next_id = 1
            if self.event_memory:
                next_id = max(event.get('id', 0) for event in self.event_memory) + 1
            
            # Create new event
            new_event = {
                'id': next_id,
                'user_id': user_id,
                'title': event_title,
                'description': description,
                'event_date': event_date,
                'start_time': start_time,
                'end_time': end_time,
                'category': category,
                'color': color,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add to events list
            self.event_memory.append(new_event)
            
            # Close the dialog
            self.close_event_dialog()
            
            # Reload events
            self.load_events()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save event: {e}")
    
    def validate_date(self, date_str):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def validate_time(self, time_str):
        """Validate time format HH:MM"""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    def update_calendar(self):
        """Update calendar display with loaded events"""
        # First make sure self.events is a dictionary
        if not isinstance(self.events, dict):
            print("Error: self.events is not a dictionary")
            self.events = {}
            return
        
        # Clear existing event indicators
        self.update_event_indicators()
        
        try:
            # Display events for the current month
            for date_key, events_list in self.events.items():
                for event in events_list:
                    # Make sure event is a dictionary before accessing keys
                    if not isinstance(event, dict):
                        print(f"Error: event is not a dictionary: {event}")
                        continue
                        
                    try:
                        # The date is already in the date_key
                        event_date = datetime.strptime(date_key, "%Y-%m-%d")
                        
                        # Check if event belongs to current month view
                        if event_date.month == self.current_date.month and event_date.year == self.current_date.year:
                            # Get day of month
                            day = event_date.day
                            
                            # Event is already displayed in the calendar through update_event_indicators
                            print(f"Found event: {event['title']} on day {day}")
                    except KeyError as e:
                        print(f"KeyError in event: {e}, event: {event}")
                    except ValueError as e:
                        print(f"ValueError parsing date: {e}, date: {date_key}")
        except Exception as e:
            print(f"Error updating calendar: {e}")
    
    def delete_event(self, event_id):
        """Delete an event"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?"):
            try:
                # Filter out the event to delete
                self.event_memory = [event for event in self.event_memory if event.get('id') != event_id]
                    
                # Reload events
                self.load_events()
            except Exception as err:
                messagebox.showerror("Error", f"Failed to delete event: {err}")

    def create_events_panel(self):
        """Create the panel for displaying and managing events"""
        # Events container with improved styling
        self.events_frame = ctk.CTkFrame(self.main_container, fg_color="#1e1e1e", corner_radius=15)
        self.events_frame.grid(row=0, column=1, sticky="nsew", pady=0)
        
        # Events header with improved styling
        self.events_header = ctk.CTkFrame(self.events_frame, fg_color="#252525", corner_radius=10, height=60)
        self.events_header.pack(fill="x", pady=(0, 15))
        self.events_header.pack_propagate(False)
        
        # Events title with improved font
        self.events_title = ctk.CTkLabel(
            self.events_header,
            text="Events",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        self.events_title.pack(side="left", padx=20, pady=15)
        
        # Add event button with improved styling
        self.add_event_btn = ctk.CTkButton(
            self.events_header,
            text="+",
            width=40,
            height=40,
            command=self.show_add_event_dialog,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            text_color="white",
            font=("Arial", 20, "bold"),
            corner_radius=8
        )
        self.add_event_btn.pack(side="right", padx=20, pady=15)
        
        # Selected date display with improved styling
        self.selected_date_frame = ctk.CTkFrame(self.events_frame, fg_color="#252525", corner_radius=10, height=60)
        self.selected_date_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.selected_date_frame.pack_propagate(False)
        
        self.selected_date_label = ctk.CTkLabel(
            self.selected_date_frame,
            text=self.selected_date.strftime("%A, %B %d, %Y"),
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        self.selected_date_label.pack(pady=15)
        
        # Events list with scrollable container
        self.events_list_frame = ctk.CTkScrollableFrame(
            self.events_frame, 
            fg_color="transparent",
            corner_radius=10,
            scrollbar_fg_color="#333333",
            scrollbar_button_color="#555555",
            scrollbar_button_hover_color="#666666"
        )
        self.events_list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # No events label with improved styling
        self.no_events_label = ctk.CTkLabel(
            self.events_list_frame,
            text="No events for this day",
            font=("Arial", 16),
            text_color="#aaaaaa"
        )
        self.no_events_label.pack(pady=50)
        
        # Back to top button container (will be added to events list when needed)
        self.top_button_frame = ctk.CTkFrame(self.events_frame, fg_color="transparent", height=50)
        self.top_button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.back_to_top_btn = ctk.CTkButton(
            self.top_button_frame,
            text="↑ Back to Top",
            font=("Arial", 14),
            height=40,
            corner_radius=8,
            fg_color="#333333",
            hover_color="#444444",
            text_color="white",
            command=self.scroll_to_top
        )
        self.back_to_top_btn.pack(fill="x")
    
    def scroll_to_top(self):
        """Scroll the events list to the top"""
        # Reset the canvas scroll position
        if hasattr(self.events_list_frame, '_parent_canvas'):
            self.events_list_frame._parent_canvas.yview_moveto(0.0) 
    
    def load_sample_events(self):
        """Load some sample events for demonstration"""
        if not self.event_memory:
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            yesterday = today - timedelta(days=1)
            
            sample_events = [
                {
                    'id': 1,
                    'user_id': 1,
                    'title': 'Physics Test',
                    'description': 'Chapter 5 - Electromagnetism',
                    'event_date': today.strftime("%Y-%m-%d"),
                    'start_time': '10:00',
                    'end_time': '12:00',
                    'category': 'Exam',
                    'color': '#e74c3c',
                    'created_at': yesterday.strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    'id': 2,
                    'user_id': 1,
                    'title': 'Study Group',
                    'description': 'JEE Advanced preparation with friends',
                    'event_date': tomorrow.strftime("%Y-%m-%d"),
                    'start_time': '14:00',
                    'end_time': '16:00',
                    'category': 'Study',
                    'color': '#4361ee',
                    'created_at': yesterday.strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    'id': 3,
                    'user_id': 1,
                    'title': 'Math Revision',
                    'description': 'Calculus and Integration',
                    'event_date': yesterday.strftime("%Y-%m-%d"),
                    'start_time': '09:00',
                    'end_time': '11:00',
                    'category': 'Revision',
                    'color': '#f39c12',
                    'created_at': yesterday.strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            
            self.event_memory.extend(sample_events)
            self.load_events() 