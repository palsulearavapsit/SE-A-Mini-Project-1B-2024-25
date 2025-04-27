import customtkinter as ctk
from tkinter import messagebox, Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import requests
import webbrowser
import random
import winsound  # For Windows beep sounds
import platform  # To detect OS
import os        # For non-Windows sound options
from datetime import datetime, timedelta

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#1A1A1A")
        self.controller = controller
        
        # For direct execution testing - set mock attributes if they don't exist
        if not hasattr(controller, 'current_user'):
            controller.current_user = "Test User"
        
        if not hasattr(controller, 'show_dashboard_page'):
            controller.show_dashboard_page = lambda: print("Dashboard")
        if not hasattr(controller, 'show_mock_tests'):
            controller.show_mock_tests = lambda: print("Mock Tests")
        if not hasattr(controller, 'show_previous_year_questions'):
            controller.show_previous_year_questions = lambda: print("Previous Year Questions") 
        if not hasattr(controller, 'show_calendar'):
            controller.show_calendar = lambda: print("Calendar")
        if not hasattr(controller, 'show_reports'):
            controller.show_reports = lambda: print("Reports")
        if not hasattr(controller, 'show_news_page'):
            controller.show_news_page = lambda: print("News")
        
        # Sound notification settings
        self.notification_played = False
        self.notifications_enabled = True  # Default to enabled
        
        # Main container with dark background
        self.configure(fg_color="#1A1A1A")
        
        # Left sidebar
        sidebar_frame = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0, width=250)
        sidebar_frame.pack(side="left", fill="y")
        
        # Welcome message at top of sidebar with enhanced styling
        welcome_frame = ctk.CTkFrame(sidebar_frame, fg_color="#2D2D2D", corner_radius=10)
        welcome_frame.pack(fill="x", padx=10, pady=10)
        
        # Get the username from the controller
        username = self.controller.current_username if hasattr(self.controller, 'current_username') else "User"
        
        # Add profile icon - using a cleaner icon style
        profile_icon = ctk.CTkLabel(
            welcome_frame,
            text="👤",
            font=ctk.CTkFont(size=32),
            text_color="#2AB377"
        )
        profile_icon.pack(pady=(10, 0))
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text=f"Welcome back,\n{username}",
            font=ctk.CTkFont(size=16, weight="bold"),
            justify="center"
        )
        welcome_label.pack(pady=(5, 10))
        
        # Add current date below welcome message
        current_date = datetime.now().strftime("%d %b %Y")
        date_label = ctk.CTkLabel(
            welcome_frame,
            text=current_date,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        date_label.pack(pady=(0, 10))
        
        # Sidebar navigation buttons - updated with improved styling
        self.create_sidebar_button(sidebar_frame, "Dashboard", "🏠", self.controller.show_dashboard_page, True)
        self.create_sidebar_button(sidebar_frame, "Mock Tests", "📝", self.controller.show_mock_tests)
        self.create_sidebar_button(sidebar_frame, "Previous Year Questions", "📚", self.controller.show_previous_year_questions)
        self.create_sidebar_button(sidebar_frame, "Calendar", "📅", self.controller.show_calendar)
        self.create_sidebar_button(sidebar_frame, "Reports", "📊", self.controller.show_reports)
        self.create_sidebar_button(sidebar_frame, "News & Updates", "📰", self.controller.show_news_page)
        self.create_sidebar_button(sidebar_frame, "Logout", "🚪", self.logout)
        
        # Main content area with grid layout
        main_content = ctk.CTkFrame(self, fg_color="#1A1A1A", corner_radius=0)
        main_content.pack(fill="both", expand=True)
        
        # Configure the grid layout for better organization
        main_content.grid_columnconfigure(0, weight=2)  # Main area
        main_content.grid_columnconfigure(1, weight=1)  # Right sidebar
        main_content.grid_rowconfigure(0, weight=0)     # Stats bar
        main_content.grid_rowconfigure(1, weight=1)     # Exam cards
        
        # Add settings button in the top right
        settings_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        settings_frame.grid(row=0, column=1, sticky="ne", padx=25, pady=5)
        
        self.create_settings_button(settings_frame)
        
        # Stats bar at top with enhanced appearance
        stats_frame = ctk.CTkFrame(main_content, fg_color="#1A1A1A", corner_radius=15, height=180)
        stats_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        stats_frame.grid_propagate(False)
        
        # Configure grid for stats
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)
        
        # Store stat labels so we can update them later
        self.stat_labels = {}
        
        # Create stat boxes with custom icons
        self.create_stat_box(stats_frame, "Tests Taken", "0", 0, "tests")
        self.create_stat_box(stats_frame, "Average Score", "0%", 1, "average")
        self.create_stat_box(stats_frame, "Best Score", "0%", 2, "best")
        self.create_stat_box(stats_frame, "Study Streak", "0 days", 3, "streak")
        
        # Load stats from database
        self.load_user_stats()
        
        # Exam cards container
        cards_container = ctk.CTkFrame(main_content, fg_color="transparent")
        cards_container.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        
        # Configure grid for cards
        cards_container.grid_columnconfigure((0, 1), weight=1)
        cards_container.grid_rowconfigure((0, 1), weight=1)
        
        # Define start_exam if it doesn't exist
        if not hasattr(controller, 'start_exam'):
            controller.start_exam = lambda t: print(f"Starting {t} exam")
        
        # JEE Card with enhanced styling
        jee_card = self.create_exam_card(
            cards_container,
            "JEE",
            "Joint Entrance Examination",
            "Engineering entrance exam for top institutes",
            "📚"
        )
        jee_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # NEET Card
        neet_card = self.create_exam_card(
            cards_container,
            "NEET",
            "National Eligibility cum Entrance Test",
            "Medical entrance examination",
            "🏥"
        )
        neet_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # GATE Card
        gate_card = self.create_exam_card(
            cards_container,
            "GATE",
            "Graduate Aptitude Test in Engineering",
            "For M.Tech admissions and PSU jobs",
            "🎓"
        )
        gate_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # CET Card
        cet_card = self.create_exam_card(
            cards_container,
            "CET",
            "Common Entrance Test",
            "State-level engineering entrance",
            "📝"
        )
        cet_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Right sidebar for additional widgets
        right_sidebar = ctk.CTkFrame(main_content, fg_color="transparent")
        right_sidebar.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="nsew")
        
        # Add calendar reminder widget at the top of the right sidebar
        self.create_calendar_reminder_widget(right_sidebar)
        
        # Add upcoming tests widget
        self.create_upcoming_tests_widget(right_sidebar)
        
        # Add study tip of the day widget
        self.create_study_tip_widget(right_sidebar)
    
    def create_stat_box(self, parent, title, value, col, icon_type):
        """Create a statistics box for the dashboard with enhanced styling and numeric visualization"""
        frame = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=15)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        
        # Title with improved font
        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="center"
        )
        title_label.pack(pady=(15, 5))
        
        # Value with improved styling
        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#2AB377",
            anchor="center"
        )
        value_label.pack(pady=(0, 5))
        
        # Add a numeric visualization based on the type
        viz_frame = ctk.CTkFrame(frame, fg_color="transparent", height=45)
        viz_frame.pack(fill="x", padx=15, pady=(0, 10))
        viz_frame.pack_propagate(False)
        
        # Create the visualization based on the stat type
        if icon_type == "tests":
            # Tests taken - Show boxes for last 5 tests
            self.create_tests_viz(viz_frame)
        elif icon_type == "average":
            # Average score - Show percentage bar
            self.create_score_viz(viz_frame, "avg")
        elif icon_type == "best":
            # Best score - Show percentage bar with star
            self.create_score_viz(viz_frame, "best")
        elif icon_type == "streak":
            # Study streak - Show calendar dots
            self.create_streak_viz(viz_frame)
            
        # Store the label reference for later updates
        self.stat_labels[title] = value_label
        # Also store references to visualizations
        if not hasattr(self, 'viz_frames'):
            self.viz_frames = {}
        self.viz_frames[title] = viz_frame
        
        return frame
        
    def create_tests_viz(self, parent):
        """Create visualization for tests taken - small boxes for each recent test"""
        # Create a canvas for drawing the test indicators
        canvas = Canvas(parent, bg="#252525", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Store the canvas reference to update later
        self.tests_canvas = canvas
        
        # Initial drawing will be done when we load user stats
        
    def create_score_viz(self, parent, score_type):
        """Create visualization for score percentages"""
        # Create a canvas for drawing the score bar
        canvas = Canvas(parent, bg="#252525", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Store the canvas reference to update later
        if score_type == "avg":
            self.avg_canvas = canvas
        else:
            self.best_canvas = canvas
        
        # Initial drawing will be done when we load user stats
        
    def create_streak_viz(self, parent):
        """Create visualization for study streak - calendar style dots"""
        # Create a canvas for drawing the streak indicators
        canvas = Canvas(parent, bg="#252525", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Store the canvas reference to update later
        self.streak_canvas = canvas
        
        # Initial drawing will be done when we load user stats
        
    def update_visualizations(self):
        """Update all stat visualizations with current data"""
        try:
            if hasattr(self, 'tests_canvas') and self.tests_canvas.winfo_exists():
                self.update_tests_viz()
                
            if hasattr(self, 'avg_canvas') and self.avg_canvas.winfo_exists():
                self.update_avg_score_viz()
                
            if hasattr(self, 'best_canvas') and self.best_canvas.winfo_exists():
                self.update_best_score_viz()
                
            if hasattr(self, 'streak_canvas') and self.streak_canvas.winfo_exists():
                self.update_streak_viz()
        except Exception as e:
            print(f"Error updating visualizations: {e}")
            
    def update_tests_viz(self):
        """Update the tests taken visualization"""
        # Clear the canvas
        self.tests_canvas.delete("all")
        
        # Get number of tests from label value
        tests_value = self.stat_labels.get("Tests Taken").cget("text")
        try:
            num_tests = int(tests_value) if tests_value.isdigit() else 0
        except:
            num_tests = 0
            
        # Calculate the total width to display up to 10 tests
        total_width = self.tests_canvas.winfo_width() - 10
        if total_width <= 0:
            total_width = 150  # Fallback width
            
        # Draw boxes for each test (show max 10 recent tests)
        box_size = min(15, total_width / 12)
        gap = 5
        x = 5
        
        # Draw up to 10 boxes for recent tests
        for i in range(min(10, num_tests)):
            color = "#2AB377"  # Default color
            
            # Vary color based on imaginary scores for visual interest
            if i % 3 == 0:
                color = "#3498DB"  # Blue
            elif i % 4 == 0:
                color = "#F39C12"  # Orange
                
            self.tests_canvas.create_rectangle(
                x, 15,
                x + box_size, 15 + box_size,
                fill=color, outline=""
            )
            x += box_size + gap
            
        # If there are more tests than we display, add an indicator
        if num_tests > 10:
            self.tests_canvas.create_text(
                x + 10, 15 + box_size/2,
                text=f"+{num_tests - 10}",
                fill="white",
                font=("Arial", 10)
            )
            
    def update_avg_score_viz(self):
        """Update the average score visualization"""
        # Clear the canvas
        self.avg_canvas.delete("all")
        
        # Get score value from label
        score_text = self.stat_labels.get("Average Score").cget("text")
        try:
            score = int(score_text.replace("%", ""))
        except:
            score = 0
            
        # Draw a percentage bar
        total_width = self.avg_canvas.winfo_width() - 10
        if total_width <= 0:
            total_width = 150  # Fallback width
            
        # Background bar
        self.avg_canvas.create_rectangle(
            5, 15,
            5 + total_width, 30,
            fill="#444444", outline=""
        )
        
        # Calculate color based on score
        if score >= 80:
            color = "#2ecc71"  # Green
        elif score >= 60:
            color = "#3498db"  # Blue
        elif score >= 40:
            color = "#f39c12"  # Orange
        else:
            color = "#e74c3c"  # Red
        
        # Score bar
        progress_width = int((score / 100) * total_width)
        self.avg_canvas.create_rectangle(
            5, 15,
            5 + progress_width, 30,
            fill=color, outline=""
        )
        
        # Score text overlay
        self.avg_canvas.create_text(
            total_width / 2 + 5, 22,
            text=f"{score}%",
            fill="white",
            font=("Arial", 10, "bold")
        )
        
    def update_best_score_viz(self):
        """Update the best score visualization"""
        # Clear the canvas
        self.best_canvas.delete("all")
        
        # Get score value from label
        score_text = self.stat_labels.get("Best Score").cget("text")
        try:
            score = int(score_text.replace("%", ""))
        except:
            score = 0
            
        # Draw a percentage bar
        total_width = self.best_canvas.winfo_width() - 10
        if total_width <= 0:
            total_width = 150  # Fallback width
            
        # Background bar
        self.best_canvas.create_rectangle(
            5, 15,
            5 + total_width, 30,
            fill="#444444", outline=""
        )
        
        # Score bar
        progress_width = int((score / 100) * total_width)
        self.best_canvas.create_rectangle(
            5, 15,
            5 + progress_width, 30,
            fill="#f1c40f", outline=""  # Gold for best score
        )
        
        # Score text overlay
        self.best_canvas.create_text(
            total_width / 2 + 5, 22,
            text=f"{score}%",
            fill="#333",
            font=("Arial", 10, "bold")
        )
        
        # Add a star icon for best score
        self.best_canvas.create_text(
            5 + progress_width - 10, 15,
            text="★",
            fill="#fff",
            font=("Arial", 12, "bold"),
            anchor="n"
        )
        
    def update_streak_viz(self):
        """Update the study streak visualization"""
        # Clear the canvas
        self.streak_canvas.delete("all")
        
        # Get streak value from label
        streak_text = self.stat_labels.get("Study Streak").cget("text")
        try:
            streak = int(streak_text.split()[0])
        except:
            streak = 0
            
        # Draw calendar-style dots for the streak
        total_width = self.streak_canvas.winfo_width() - 10
        if total_width <= 0:
            total_width = 150  # Fallback width
            
        # Size and positioning
        dot_size = 10
        gap = 5
        x = 5
        
        # Draw dots for each day in the streak
        for i in range(min(streak, 14)):  # Show up to 14 days
            # Vary color slightly for visual interest
            intensity = min(100, 50 + (i * 3))
            color = f"#{intensity:02x}{160:02x}77"
            
            self.streak_canvas.create_oval(
                x, 15,
                x + dot_size, 15 + dot_size,
                fill=color, outline=""
            )
            x += dot_size + gap
        
        # If streak is longer than what we display, add indicator
        if streak > 14:
            self.streak_canvas.create_text(
                x + 10, 15 + dot_size/2,
                text=f"+{streak - 14}",
                fill="white",
                font=("Arial", 10)
            )
            
    def create_sidebar_button(self, parent, text, icon, command, is_active=False):
        """Create a styled sidebar button with icon"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Button with icon and text
        bg_color = "#2AB377" if is_active else "transparent"
        text_color = "white" if is_active else "gray90"
        hover_color = "#1C8A59" if is_active else "#2D2D2D"
        
        button = ctk.CTkButton(
            button_frame,
            text=f"{icon} {text}",
            fg_color=bg_color,
            text_color=text_color,
            hover_color=hover_color,
            anchor="w",
            height=40,
            corner_radius=10,
            command=command
        )
        button.pack(fill="x")
        
        return button
    
    def create_upcoming_tests_widget(self, parent):
        """Create widget showing upcoming scheduled tests"""
        widget_frame = ctk.CTkFrame(parent, fg_color="#2D2D2D", corner_radius=15)
        widget_frame.pack(fill="x", padx=10, pady=10)
        
        # Title with icon
        title_label = ctk.CTkLabel(
            widget_frame,
            text="📆 Upcoming Tests",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", padx=15, pady=(15, 10))
        
        # Upcoming tests (in a real app, this would come from the database)
        # For demonstration, we'll include a test for "today"
        current_date = datetime.now()
        today_str = "Today"
        tomorrow_str = "Tomorrow"
        in_two_days = (current_date + timedelta(days=2)).strftime("%d %b")
        in_a_week = (current_date + timedelta(days=7)).strftime("%d %b")
        
        upcoming_tests = [
            {"name": "Physics Mock Test", "date": today_str, "time": "10:00 AM", "is_today": True},
            {"name": "Chemistry Quiz", "date": tomorrow_str, "time": "2:30 PM", "is_today": False},
            {"name": "Full JEE Mock", "date": in_a_week, "time": "9:00 AM", "is_today": False}
        ]
        
        # Store tests for today to determine if we should play a notification
        self.today_tests = [test for test in upcoming_tests if test.get("is_today", False)]
        
        for test in upcoming_tests:
            test_frame = ctk.CTkFrame(widget_frame, fg_color="#1A1A1A", corner_radius=10)
            test_frame.pack(fill="x", padx=15, pady=5)
            
            # Add urgency indicator for tests happening today
            if test.get("is_today", False):
                test_frame.configure(fg_color="#442211")  # Slightly different background for today's tests
                
                reminder_button = ctk.CTkButton(
                    test_frame,
                    text="🔔",
                    width=30,
                    height=30,
                    fg_color="#F39C12",
                    hover_color="#E67E22",
                    corner_radius=15,
                    command=self.play_notification_sound
                )
                reminder_button.pack(side="right", padx=10, pady=10)
            
            test_name = ctk.CTkLabel(
                test_frame,
                text=test["name"],
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            test_name.pack(fill="x", padx=10, pady=(5, 0))
            
            time_color = "#FF9900" if test.get("is_today", False) else "gray"
            test_time = ctk.CTkLabel(
                test_frame,
                text=f"{test['date']} at {test['time']}",
                font=ctk.CTkFont(size=10),
                text_color=time_color,
                anchor="w"
            )
            test_time.pack(fill="x", padx=10, pady=(0, 5))
        
        # Show all button
        all_button = ctk.CTkButton(
            widget_frame,
            text="View Calendar",
            font=ctk.CTkFont(size=12),
            fg_color="#2AB377",
            hover_color="#1C8A59",
            height=25,
            corner_radius=15,
            command=self.controller.show_calendar
        )
        all_button.pack(padx=15, pady=15)
        
        # If there are tests for today, play notification after a delay
        if self.today_tests and not self.notification_played:
            self.after(2000, self.play_notification_sound)
            
    def create_settings_button(self, parent):
        """Create a settings button with sound notification toggle"""
        settings_button = ctk.CTkButton(
            parent,
            text="🔊",  # Sound icon
            width=40,
            height=40,
            fg_color="#333333",
            hover_color="#444444",
            corner_radius=20,
            command=self.toggle_sound_notifications
        )
        settings_button.pack(pady=5)
        
        # Store reference to update icon
        self.settings_button = settings_button
        
        # Show tooltip text
        tooltip_text = "Sound notifications: ON"
        tooltip = ctk.CTkLabel(
            parent,
            text=tooltip_text,
            font=ctk.CTkFont(size=10),
            fg_color="#333333",
            corner_radius=5,
            text_color="white"
        )
        tooltip.pack(pady=(0, 5))
        
        # Store tooltip reference
        self.tooltip = tooltip
        
    def toggle_sound_notifications(self):
        """Toggle sound notifications on/off"""
        self.notifications_enabled = not self.notifications_enabled
        
        # Update all sound buttons
        icon = "🔊" if self.notifications_enabled else "🔇"
        
        if hasattr(self, 'settings_button'):
            self.settings_button.configure(text=icon)
            
        if hasattr(self, 'sound_button'):
            self.sound_button.configure(text=icon)
            
        # Update tooltip if it exists
        if hasattr(self, 'tooltip'):
            status = "ON" if self.notifications_enabled else "OFF"
            self.tooltip.configure(text=f"Sound notifications: {status}")
        
        # Show confirmation message
        if self.notifications_enabled:
            messagebox.showinfo("Notifications", "Sound notifications have been enabled")
        else:
            messagebox.showinfo("Notifications", "Sound notifications have been disabled")
            
    def play_notification_sound(self):
        """Play a notification sound for upcoming tests"""
        self.notification_played = True
        
        # Only play sound if notifications are enabled
        if not self.notifications_enabled:
            return
            
        try:
            # Different sound methods depending on platform
            if platform.system() == "Windows":
                # Windows beep
                winsound.Beep(1000, 500)  # Frequency 1000Hz, duration 500ms
                
                # Show popup notification if there are tests today
                if hasattr(self, 'today_tests') and self.today_tests:
                    test_names = "\n".join([f"• {test['name']} at {test['time']}" for test in self.today_tests])
                    messagebox.showinfo(
                        "Upcoming Tests Today", 
                        f"You have the following tests scheduled for today:\n\n{test_names}"
                    )
            
            elif platform.system() == "Darwin":  # macOS
                # Mac uses system sound (requires terminal access, may not work in all environments)
                os.system("afplay /System/Library/Sounds/Ping.aiff")
            
            else:  # Linux and others
                # Try using the bell character for non-Windows platforms
                print("\a")  # Bell character
                self.bell()  # Tkinter's bell method
        
        except Exception as e:
            print(f"Error playing notification sound: {e}")
            # Fallback to Tkinter's bell
            self.bell()
    
    def create_study_tip_widget(self, parent):
        """Create widget showing random study tip of the day"""
        widget_frame = ctk.CTkFrame(parent, fg_color="#2D2D2D", corner_radius=15)
        widget_frame.pack(fill="x", padx=10, pady=10)
        
        # Title with icon
        title_label = ctk.CTkLabel(
            widget_frame,
            text="💡 Study Tip of the Day",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.pack(fill="x", padx=15, pady=(15, 10))
        
        # Random study tips
        study_tips = [
            "Use the Pomodoro Technique: 25 minutes of focus, 5 minutes break.",
            "Create mind maps to connect concepts visually.",
            "Teach what you've learned to someone else to reinforce your understanding.",
            "Review your notes within 24 hours of taking them to improve retention.",
            "Practice active recall instead of passive re-reading.",
            "Study in a dedicated space free from distractions.",
            "Take regular breaks to avoid burnout and maintain focus.",
            "Use spaced repetition for topics you find challenging.",
            "Get enough sleep - your brain consolidates memories during rest.",
            "Stay hydrated and maintain a balanced diet for optimal brain function."
        ]
        
        # Select a random tip
        tip = random.choice(study_tips)
        
        # Tip text
        tip_label = ctk.CTkLabel(
            widget_frame,
            text=tip,
            font=ctk.CTkFont(size=12),
            wraplength=250,
            justify="left"
        )
        tip_label.pack(fill="x", padx=15, pady=(5, 15))
    
    def logout(self):
        """Log out the current user and return to login page"""
        # Add logout confirmation
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.controller.current_user = None
            self.controller.show_login_page()

    def load_user_stats(self):
        """Load user statistics from database"""
        # First verify if we still exist before doing any updates
        try:
            if not self.winfo_exists():
                print("Dashboard no longer exists - skipping stats update")
                return
                
            # Check if database manager exists and user is logged in
            if hasattr(self.controller, 'db_manager') and hasattr(self.controller, 'current_user_id') and self.controller.current_user_id:
                try:
                    db = self.controller.db_manager
                    user_id = self.controller.current_user_id
                    
                    # Get tests taken count
                    tests_taken = db.get_tests_taken_count(user_id)
                    self.update_stat("Tests Taken", str(tests_taken))
                    
                    # Get average score
                    avg_score = db.get_average_score(user_id)
                    # Format with no decimal places if it's an integer
                    avg_score_display = f"{int(avg_score)}%" if avg_score == int(avg_score) else f"{avg_score:.1f}%"
                    self.update_stat("Average Score", avg_score_display)
                    
                    # Get best score
                    best_score = db.get_best_score(user_id)
                    # Format with no decimal places if it's an integer
                    best_score_display = f"{int(best_score)}%" if best_score == int(best_score) else f"{best_score:.1f}%"
                    self.update_stat("Best Score", best_score_display)
                    
                    # Get study streak
                    streak = db.get_study_streak(user_id)
                    streak_text = f"{streak} days" if streak != 1 else "1 day"
                    self.update_stat("Study Streak", streak_text)
                    
                    print(f"User stats loaded from database: Tests={tests_taken}, Avg={avg_score}, Best={best_score}, Streak={streak}")
                    
                    # Check for upcoming calendar events
                    self.after(1000, self.check_calendar_events)
                    
                except Exception as e:
                    print(f"Error loading user stats: {e}")
                    # Fall back to sample data if there's an error
                    self.update_stat("Tests Taken", "0")
                    self.update_stat("Average Score", "0%")
                    self.update_stat("Best Score", "0%")
                    self.update_stat("Study Streak", "0 days")
            else:
                # Use sample data if no database or user is not logged in
                self.update_stat("Tests Taken", "0")
                self.update_stat("Average Score", "0%")
                self.update_stat("Best Score", "0%")
                self.update_stat("Study Streak", "0 days")
                
            # Update the visualizations
            self.after(100, self.update_visualizations)
                
        except Exception as e:
            print(f"Error in load_user_stats: {e}")
            
    def check_calendar_events(self):
        """Check for upcoming calendar events and display notifications"""
        try:
            # Check if user is logged in and database manager exists
            if not hasattr(self.controller, 'db_manager') or not hasattr(self.controller, 'current_user_id') or not self.controller.current_user_id:
                return
                
            # In a real implementation, this would fetch from the calendar table in the database
            # For now, we'll simulate some test events
            current_date = datetime.now()
            current_hour = current_date.hour
            
            # Check for events within the next hour (or happening now)
            upcoming_events = self.get_upcoming_calendar_events()
            
            # Update the reminder widget
            self.update_reminder_widget()
            
            # If we have events coming up, show notification
            if upcoming_events and self.notifications_enabled and not hasattr(self, 'calendar_notification_shown'):
                self.calendar_notification_shown = True
                
                # Play a different sound for calendar events
                self.play_calendar_sound()
                
                # Show event notification
                events_text = "\n".join([f"• {event['title']} at {event['time']}" for event in upcoming_events])
                messagebox.showinfo(
                    "Upcoming Calendar Events", 
                    f"You have the following events coming up:\n\n{events_text}"
                )
        except Exception as e:
            print(f"Error checking calendar events: {e}")
            
    def get_upcoming_calendar_events(self):
        """Get upcoming calendar events from the database"""
        # In a real implementation, this would query the database
        # For now, we'll simulate some test events
        
        try:
            # If database connection exists, try to get real events
            if hasattr(self.controller, 'db_manager') and self.controller.db_manager:
                # This would be the actual database query in a real implementation
                # return self.controller.db_manager.get_upcoming_events(self.controller.current_user_id)
                pass
        except Exception as e:
            print(f"Error fetching calendar events: {e}")
        
        # For demonstration, create some sample events
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # Make an event that's coming up soon
        upcoming_minute = (current_minute + 5) % 60
        upcoming_hour = current_hour if upcoming_minute > current_minute else (current_hour + 1) % 24
        upcoming_time = f"{upcoming_hour:02d}:{upcoming_minute:02d}"
        
        events = [
            {"title": "Physics Study Session", "time": upcoming_time, "type": "study"},
            {"title": "Chemistry Revision", "time": f"{(current_hour + 1) % 24:02d}:00", "type": "revision"}
        ]
        
        return events
        
    def play_calendar_sound(self):
        """Play a notification sound for calendar events (different from test notifications)"""
        if not self.notifications_enabled:
            return
            
        try:
            # Different sound methods depending on platform
            if platform.system() == "Windows":
                # A slightly different tone for calendar events
                winsound.Beep(1500, 250)  # Higher pitch, shorter duration
                winsound.Beep(1700, 250)  # Second beep
            
            elif platform.system() == "Darwin":  # macOS
                os.system("afplay /System/Library/Sounds/Tink.aiff")
            
            else:  # Linux and others
                self.bell()
        
        except Exception as e:
            print(f"Error playing calendar sound: {e}")
            self.bell()

    def update_stat(self, title, value):
        """Update a specific stat value"""
        try:
            # Verify we still exist and the label exists
            if not self.winfo_exists():
                return
                
            if title in self.stat_labels and hasattr(self.stat_labels[title], 'winfo_exists'):
                if self.stat_labels[title].winfo_exists():
                    self.stat_labels[title].configure(text=value)
        except Exception as e:
            print(f"Error updating stat {title}: {e}")

    def create_exam_card(self, parent, title, subtitle, description, icon):
        """Create an exam card with enhanced styling"""
        card = ctk.CTkFrame(parent, fg_color="#2D2D2D", corner_radius=15)
        
        # Icon on the left with distinct color
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=36),
            text_color="#2AB377"
        )
        icon_label.place(relx=0.1, rely=0.2)
        
        # Title with bold font
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.place(relx=0.5, rely=0.2, anchor="center")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=12)
        )
        subtitle_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Description with smaller font
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        desc_label.place(relx=0.5, rely=0.6, anchor="center")
        
        # Prepare button with improved styling
        prepare_button = ctk.CTkButton(
            card,
            text="Prepare",
            font=ctk.CTkFont(size=12),
            fg_color="#2AB377",
            hover_color="#1C8A59",
            height=30,
            width=120,
            corner_radius=15,
            command=lambda t=title: self.controller.start_exam(t)
        )
        prepare_button.place(relx=0.5, rely=0.8, anchor="center")
        
        return card

    def create_calendar_reminder_widget(self, parent):
        """Create a widget displaying upcoming calendar events with reminders"""
        reminder_frame = ctk.CTkFrame(parent, fg_color="#2D2D2D", corner_radius=15)
        reminder_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Header with reminder icon
        header_frame = ctk.CTkFrame(reminder_frame, fg_color="#1A1A1A", corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Title with bell icon
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🔔 Today's Reminders",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#F39C12"
        )
        title_label.pack(side="left", padx=5)
        
        # Sound toggle button next to title
        sound_button = ctk.CTkButton(
            title_frame,
            text="🔊",
            width=30,
            height=30,
            fg_color="#F39C12",
            hover_color="#E67E22",
            corner_radius=15,
            command=self.toggle_sound_notifications
        )
        sound_button.pack(side="right", padx=5)
        self.sound_button = sound_button  # Store reference to update icon
        
        # Container for reminders
        self.reminders_container = ctk.CTkFrame(reminder_frame, fg_color="transparent")
        self.reminders_container.pack(fill="x", padx=10, pady=10)
        
        # Will be populated when check_calendar_events is called
        self.no_reminders_label = ctk.CTkLabel(
            self.reminders_container,
            text="No reminders for today",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            justify="center"
        )
        self.no_reminders_label.pack(pady=10)
        
    def update_reminder_widget(self):
        """Update the reminder widget with upcoming events"""
        # Clear existing reminders
        for widget in self.reminders_container.winfo_children():
            widget.destroy()
            
        # Get upcoming events
        events = self.get_upcoming_calendar_events()
        
        if not events:
            # Show no reminders label
            self.no_reminders_label = ctk.CTkLabel(
                self.reminders_container,
                text="No reminders for today",
                font=ctk.CTkFont(size=12),
                text_color="gray",
                justify="center"
            )
            self.no_reminders_label.pack(pady=10)
            return
            
        # Add each event to the container
        for event in events:
            event_frame = ctk.CTkFrame(self.reminders_container, fg_color="#1A1A1A", corner_radius=10)
            event_frame.pack(fill="x", pady=5)
            
            # Icon based on event type
            icon = "📚"  # Default study icon
            if event.get('type') == 'test':
                icon = "📝"
            elif event.get('type') == 'revision':
                icon = "📖"
            elif event.get('type') == 'meeting':
                icon = "👥"
                
            # Event title with icon
            title_label = ctk.CTkLabel(
                event_frame,
                text=f"{icon} {event['title']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            title_label.pack(fill="x", padx=10, pady=(5, 0))
            
            # Event time
            time_label = ctk.CTkLabel(
                event_frame,
                text=f"⏰ {event['time']}",
                font=ctk.CTkFont(size=10),
                text_color="#F39C12",
                anchor="w"
            )
            time_label.pack(fill="x", padx=10, pady=(0, 5))
            
        # Add a button to view calendar
        view_button = ctk.CTkButton(
            self.reminders_container,
            text="View All Events",
            font=ctk.CTkFont(size=12),
            fg_color="#2AB377",
            hover_color="#1C8A59",
            height=25,
            corner_radius=15,
            command=self.controller.show_calendar
        )
        view_button.pack(pady=10)

def main():
    # Example of how this might be used
    root = ctk.CTk()
    root.title("EduQuest Dashboard")
    root.geometry("1200x800")
    
    # Configure default theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Create a mock controller class to avoid attribute errors
    class MockController:
        def __init__(self):
            self.current_user = "Test User"
            self.current_username = "Test User"
            # Add mock methods for all sidebar buttons
            
    controller = MockController()
    
    dashboard = DashboardPage(root, controller)
    dashboard.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__":
    main()