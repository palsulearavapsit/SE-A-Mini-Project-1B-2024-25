import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import time
from datetime import datetime
import webbrowser

class JEESubjectsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0)
        self.master = master
        self.app = app
        
        # Initialize storage for test results and responses
        self.test_results = []
        self.question_responses = {}
        
        # Create subject cards and UI elements
        self.create_ui()
    
    def create_ui(self):
        # Clear any existing content
        for widget in self.winfo_children():
            widget.destroy()
            
        # Set background color
        self.configure(fg_color="#1a1a1a")
        
        # Create a header frame
        header_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Back button
        back_button = ctk.CTkButton(
            header_frame, 
            text="← Back to Dashboard",
            command=self.app.show_dashboard_page,
            width=150,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            corner_radius=8
        )
        back_button.pack(side="left", padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="JEE Preparation",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Main content container with scrolling
        content_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section
        title_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_section.pack(fill="x", pady=(0, 20))
        
        main_title = ctk.CTkLabel(
            title_section,
            text="Joint Entrance Examination",
            font=("Arial", 28, "bold"),
            text_color="white"
        )
        main_title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_section,
            text="Select a subject to begin your preparation",
            font=("Arial", 16),
            text_color="#cccccc"
        )
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # Subject cards container
        cards_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        cards_container.pack(fill="both", expand=True, pady=10)
        
        # Configure grid for 3 cards
        cards_container.columnconfigure(0, weight=1)
        cards_container.columnconfigure(1, weight=1)
        cards_container.columnconfigure(2, weight=1)
        
        # Subject data
        subjects = [
            {
                "name": "Physics",
                "icon": "🔭",
                "color": "#4361ee",
                "hover_color": "#3a56d4",
                "topics": [
                    "Mechanics", "Electromagnetism", "Optics", 
                    "Modern Physics", "Thermodynamics"
                ],
                "description": "Study of matter, energy, and the interaction between them"
            },
            {
                "name": "Chemistry",
                "icon": "🧪",
                "color": "#f72585",
                "hover_color": "#e31c79",
                "topics": [
                    "Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry", 
                    "Analytical Chemistry", "Coordination Chemistry"
                ],
                "description": "Study of substances, their properties, structure, and transformations"
            },
            {
                "name": "Mathematics",
                "icon": "📊",
                "color": "#4cc9f0",
                "hover_color": "#37b4e3",
                "topics": [
                    "Algebra", "Calculus", "Coordinate Geometry", 
                    "Trigonometry", "Vectors and 3D Geometry"
                ],
                "description": "Study of numbers, quantity, structure, space, and change"
            }
        ]
        
        # Create a card for each subject
        for i, subject in enumerate(subjects):
            self.create_subject_card(cards_container, subject, i)
        
        # Recent questions section
        recent_section = ctk.CTkFrame(content_frame, fg_color="#2c2c2c", corner_radius=10)
        recent_section.pack(fill="x", pady=20, ipady=15)
        
        recent_title = ctk.CTkLabel(
            recent_section,
            text="Recent JEE Questions",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        recent_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Sample recent questions
        recent_questions = [
            {
                "question": "A particle is projected with a speed of 20 m/s at an angle of 60° to the horizontal. What is the maximum height reached by the particle?",
                "subject": "Physics",
                "year": "2022"
            },
            {
                "question": "Calculate the pH of a buffer solution containing 0.2 M CH₃COOH and 0.3 M CH₃COONa. (pKa of CH₃COOH = 4.74)",
                "subject": "Chemistry",
                "year": "2022"
            },
            {
                "question": "If z = x + iy, where x and y are real, then the value of |z|² + |z̄|² is:",
                "subject": "Mathematics",
                "year": "2021"
            }
        ]
        
        # Display recent questions
        for q in recent_questions:
            q_frame = ctk.CTkFrame(recent_section, fg_color="#383838", corner_radius=5)
            q_frame.pack(fill="x", padx=20, pady=5, ipady=5)
            
            subject_tag = ctk.CTkLabel(
                q_frame,
                text=q["subject"],
                font=("Arial", 12),
                text_color="white",
                fg_color=self.get_subject_color(q["subject"]),
                corner_radius=5,
                width=80
            )
            subject_tag.pack(side="left", padx=(10, 5), pady=10)
            
            year_tag = ctk.CTkLabel(
                q_frame,
                text=q["year"],
                font=("Arial", 12),
                text_color="white",
                fg_color="#555555",
                corner_radius=5,
                width=50
            )
            year_tag.pack(side="left", padx=5, pady=10)
            
            question_text = ctk.CTkLabel(
                q_frame,
                text=q["question"],
                font=("Arial", 14),
                text_color="white",
                justify="left",
                wraplength=800
            )
            question_text.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Study resources section
        resources_section = ctk.CTkFrame(content_frame, fg_color="#2c2c2c", corner_radius=10)
        resources_section.pack(fill="x", pady=10, ipady=15)
        
        resources_title = ctk.CTkLabel(
            resources_section,
            text="Study Resources",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        resources_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Resources grid - now with only 2 resources instead of 4
        resources_grid = ctk.CTkFrame(resources_section, fg_color="transparent")
        resources_grid.pack(fill="x", padx=20, pady=10)
        
        # Modified resources list - removed Practice Tests and Solved Examples
        resources = [
            {"name": "Video Lectures", "icon": "🎬"},
            {"name": "Formula Sheets", "icon": "📄"}
        ]
        
        # Configure grid columns (only 2 columns now)
        resources_grid.columnconfigure(0, weight=1)
        resources_grid.columnconfigure(1, weight=1)
        
        # Create resource buttons
        for i, resource in enumerate(resources):
            resource_btn = ctk.CTkButton(
                resources_grid,
                text=f"{resource['icon']} {resource['name']}",
                font=("Arial", 14),
                fg_color="#3d3d3d",
                hover_color="#4d4d4d",
                height=50,
                corner_radius=8,
                command=lambda name=resource["name"]: self.show_resource(name)
            )
            resource_btn.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
    
    def create_subject_card(self, parent, subject_data, index):
        # Create card frame
        card = ctk.CTkFrame(parent, fg_color=subject_data["color"], corner_radius=10)
        card.grid(row=0, column=index, padx=10, pady=10, sticky="nsew")
        
        # Card content
        # Header with icon and subject name
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        icon_label = ctk.CTkLabel(
            header_frame,
            text=subject_data["icon"],
            font=("Arial", 36)
        )
        icon_label.pack(side="left")
        
        subject_label = ctk.CTkLabel(
            header_frame,
            text=subject_data["name"],
            font=("Arial", 24, "bold"),
            text_color="white"
        )
        subject_label.pack(side="left", padx=10)
        
        # Description
        desc_label = ctk.CTkLabel(
            card,
            text=subject_data["description"],
            font=("Arial", 14),
            text_color="white",
            justify="left",
            wraplength=250
        )
        desc_label.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Topics
        topics_frame = ctk.CTkFrame(card, fg_color="transparent")
        topics_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        topics_label = ctk.CTkLabel(
            topics_frame,
            text="Key Topics:",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        topics_label.pack(anchor="w", pady=(0, 5))
        
        for topic in subject_data["topics"]:
            topic_label = ctk.CTkLabel(
                topics_frame,
                text=f"• {topic}",
                font=("Arial", 12),
                text_color="white",
                justify="left"
            )
            topic_label.pack(anchor="w", pady=1)
            
        # Study button
        study_button = ctk.CTkButton(
            card,
            text="Study Now",
            font=("Arial", 14, "bold"),
            fg_color="white",
            text_color=subject_data["color"],
            hover_color="#f0f0f0",
            height=40,
            corner_radius=8,
            command=lambda subj=subject_data["name"]: self.start_subject_study(subj)
        )
        study_button.pack(padx=20, pady=(10, 20), fill="x")
        
        # Make the entire card clickable
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda e, subj=subject_data["name"]: self.start_subject_study(subj))
            for subwidget in widget.winfo_children():
                subwidget.bind("<Button-1>", lambda e, subj=subject_data["name"]: self.start_subject_study(subj))
        
        card.bind("<Button-1>", lambda e, subj=subject_data["name"]: self.start_subject_study(subj))
        
        # Hover effect
        card.bind("<Enter>", lambda e, c=card, color=subject_data["hover_color"]: c.configure(fg_color=color))
        card.bind("<Leave>", lambda e, c=card, color=subject_data["color"]: c.configure(fg_color=color))
    
    def start_subject_study(self, subject):
        if subject == "Physics":
            self.load_physics_section()
        elif subject == "Chemistry":
            self.load_chemistry_section()
        elif subject == "Mathematics":
            self.load_mathematics_section()
        else:
            messagebox.showinfo("Study Subject", f"Starting {subject} study session...")
            
    def show_resource(self, resource_name):
        """Show the selected resource"""
        if resource_name == "Video Lectures":
            self.open_video_lectures()
        elif resource_name == "Formula Sheets":
            self.open_formula_sheets()
        else:
            messagebox.showinfo("Resources", f"Opening {resource_name}...")
    
    def get_subject_color(self, subject):
        """Return color for subject tag"""
        colors = {
            "Physics": "#4361ee",
            "Chemistry": "#f72585",
            "Mathematics": "#4cc9f0"
        }
        return colors.get(subject, "#888888")

    def load_physics_section(self):
        try:
            # Attempt to load physics questions
            questions = self.load_physics_questions()
            if not questions:
                print("No questions found for the physics section.")
                messagebox.showinfo("Error", "No physics questions available.")
            else:
                # If questions are loaded, display the mock test interface
                self.display_mock_test("Physics", questions)
        except Exception as e:
            print(f"Error loading physics section: {e}")
            messagebox.showerror("Error", f"Failed to load physics section: {e}")

    def load_physics_questions(self):
        # This is a sample implementation - you would fetch from your database
        questions = []
        for i in range(1, 31):  # Create 30 sample questions
            questions.append({
                "id": i,
                "question": "At time t = 0 s particle starts moving along the x-axis. If its kinetic energy increases uniformly with time 't', the net force acting on it must be proportional to",
                "options": [
                    "A. √t",
                    "B. constant",
                    "C. t",
                    "D. 1/√t"
                ],
                "answer": "A",
                "topic": "Mechanics"
            })
        return questions

    def display_mock_test(self, subject, questions):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        self.configure(fg_color="#1a1a1a")
        
        # Store questions for reference
        self.questions = questions[:30]  # Limit to 30 questions
        self.current_question_index = 0
        self.user_answers = {}
        self.marked_for_review = set()
        self.answered_questions = set()
        
        # Create header with candidate info and timer
        header_frame = ctk.CTkFrame(self, fg_color="#2c2c2c")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Back to Dashboard",
            command=self.create_ui,
            fg_color="transparent",
            hover_color="#3d3d3d",
            anchor="w",
        )
        back_btn.pack(anchor="w", padx=10, pady=5)
        
        # Candidate info
        info_frame = ctk.CTkFrame(header_frame, fg_color="#333333")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        # Add profile icon
        profile_frame = ctk.CTkFrame(info_frame, width=50, height=50, fg_color="#444444")
        profile_frame.pack(side="left", padx=10, pady=10)
        
        profile_icon = ctk.CTkLabel(profile_frame, text="👤", font=("Arial", 24))
        profile_icon.pack(expand=True)
        
        # Candidate details
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(details_frame, text="Candidate Name: User", anchor="w").pack(anchor="w")
        ctk.CTkLabel(details_frame, text=f"Exam Name: {subject}", anchor="w").pack(anchor="w")
        ctk.CTkLabel(details_frame, text=f"Subject Name: {subject}", anchor="w").pack(anchor="w")
        
        # Timer
        self.time_remaining = 60 * 60  # 1 hour in seconds
        self.timer_label = ctk.CTkLabel(
            info_frame,
            text=self.format_time(self.time_remaining),
            font=("Arial", 24, "bold"),
            text_color="#3498db"
        )
        self.timer_label.pack(side="right", padx=20)
        
        ctk.CTkLabel(info_frame, text="Remaining Time", font=("Arial", 12)).pack(side="right")
        
        self.start_timer()
        
        # Create main content area with question and navigation
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10)
        
        # Question area (left side)
        question_area = ctk.CTkFrame(content_frame, fg_color="#2c2c2c")
        question_area.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Question number
        self.question_number_label = ctk.CTkLabel(
            question_area,
            text="Question 1/30",
            font=("Arial", 14),
            anchor="w"
        )
        self.question_number_label.pack(anchor="w", padx=20, pady=10)
        
        # Question frame
        self.question_frame = ctk.CTkFrame(question_area, fg_color="transparent")
        self.question_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Add navigation buttons frame at the bottom
        nav_buttons_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", height=60)
        nav_buttons_frame.pack(fill="x", padx=10, pady=10, side="bottom")
        
        # Previous button
        prev_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="← Previous",
            command=self.previous_question,
            fg_color="#444444",
            hover_color="#555555",
            width=120,
            height=40,
            corner_radius=5
        )
        prev_btn.pack(side="left", padx=20, pady=10)
        
        # Submit test button - added in the center
        submit_test_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="Submit Test",
            command=self.confirm_submit_test,
            fg_color="#e74c3c",  # Red color for submit button
            hover_color="#c0392b",
            width=150,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=5
        )
        submit_test_btn.pack(side="left", padx=(200, 200), pady=10)  # Centered with padding
        
        # Next button
        next_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="Next →",
            command=self.next_question,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=120,
            height=40,
            corner_radius=5
        )
        next_btn.pack(side="right", padx=20, pady=10)
        
        # Question navigation panel (right side)
        nav_panel = ctk.CTkFrame(content_frame, fg_color="#2c2c2c", width=200)
        nav_panel.pack(side="right", fill="y")
        nav_panel.pack_propagate(False)
        
        # Question status indicators
        status_frame = ctk.CTkFrame(nav_panel, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=10)
        
        statuses = [
            {"text": "Not Visited", "count": "1", "color": "#666666"},
            {"text": "Not Answered", "count": "0", "color": "#e74c3c"},
            {"text": "Answered", "count": "0", "color": "#2ecc71"},
            {"text": "Marked for Review", "count": "0", "color": "#f1c40f"},
            {"text": "Answered & Marked for Review", "count": "0", "color": "#9b59b6"}
        ]
        
        for status in statuses:
            status_item = ctk.CTkFrame(status_frame, fg_color="transparent")
            status_item.pack(fill="x", pady=2)
            
            count_label = ctk.CTkLabel(
                status_item,
                text=status["count"],
                width=30,
                fg_color=status["color"],
                corner_radius=5
            )
            count_label.pack(side="left", padx=5)
            
            text_label = ctk.CTkLabel(status_item, text=status["text"], anchor="w")
            text_label.pack(side="left", padx=5)
        
        # Question number grid
        grid_frame = ctk.CTkFrame(nav_panel, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.question_buttons = []
        cols = 4
        rows = 8
        
        for i in range(30):
            row = i // cols
            col = i % cols
            
            btn = ctk.CTkButton(
                grid_frame,
                text=str(i + 1),
                width=35,
                height=35,
                fg_color="#444444",
                hover_color="#555555",
                command=lambda idx=i: self.show_question(idx)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.question_buttons.append(btn)
        
        # Display first question
        self.show_question(0)

    def show_question(self, index):
        if 0 <= index < len(self.questions):
            self.current_question_index = index
            
            # Clear the question frame
            for widget in self.question_frame.winfo_children():
                widget.destroy()
            
            # Update question number
            self.question_number_label.configure(text=f"Question {index + 1}/30")
            
            # Get current question
            question = self.questions[index]
            
            # Question text
            question_text = ctk.CTkLabel(
                self.question_frame,
                text=question["question"],
                font=("Arial", 14),
                wraplength=700,
                justify="left"
            )
            question_text.pack(anchor="w", pady=(0, 20))
            
            # Options
            self.selected_option = ctk.StringVar()
            if index in self.user_answers:
                self.selected_option.set(self.user_answers[index])
            
            for option_text in question["options"]:
                option = option_text.split(".")[0]
                option_radio = ctk.CTkRadioButton(
                    self.question_frame,
                    text=option_text,
                    variable=self.selected_option,
                    value=option,
                    font=("Arial", 13),
                    command=lambda idx=index: self.save_answer(idx)
                )
                option_radio.pack(anchor="w", pady=10)
            
            # Update question button colors
            self.update_question_buttons()

    def save_answer(self, question_index):
        """Save the user's answer for the current question"""
        answer = self.selected_option.get()
        if answer:
            self.user_answers[question_index] = answer
            self.answered_questions.add(question_index)
            self.update_question_buttons()

    def toggle_mark_for_review(self):
        """Toggle marking the current question for review"""
        if self.current_question_index in self.marked_for_review:
            self.marked_for_review.remove(self.current_question_index)
        else:
            self.marked_for_review.add(self.current_question_index)
        self.update_question_buttons()

    def clear_response(self):
        """Clear the response for the current question"""
        if self.current_question_index in self.user_answers:
            del self.user_answers[self.current_question_index]
        if self.current_question_index in self.answered_questions:
            self.answered_questions.remove(self.current_question_index)
        self.selected_option.set("")
        self.update_question_buttons()

    def update_question_buttons(self):
        """Update the color of all question buttons based on their status"""
        for i, btn in enumerate(self.question_buttons):
            if i == self.current_question_index:
                btn.configure(fg_color="#2ecc71")  # Current question (green)
            elif i in self.answered_questions and i in self.marked_for_review:
                btn.configure(fg_color="#9b59b6")  # Answered and marked (purple)
            elif i in self.marked_for_review:
                btn.configure(fg_color="#f39c12")  # Marked for review (orange)
            elif i in self.answered_questions:
                btn.configure(fg_color="#3498db")  # Answered (blue)
            else:
                btn.configure(fg_color="#333333")  # Not visited (dark gray)

    def next_question(self):
        """Navigate to the next question"""
        if self.current_question_index < len(self.questions) - 1:
            self.show_question(self.current_question_index + 1)

    def previous_question(self):
        """Navigate to the previous question"""
        if self.current_question_index > 0:
            self.show_question(self.current_question_index - 1)

    def format_time(self, seconds):
        """Format seconds into HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def start_timer(self):
        """Start the countdown timer"""
        def update_timer():
            if self.time_remaining > 0:
                self.time_remaining -= 1
                # Check if timer_label still exists and hasn't been destroyed
                try:
                    if self.winfo_exists() and hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                        self.timer_label.configure(text=self.format_time(self.time_remaining))
                        self.after(1000, update_timer)
                    else:
                        # Widget has been destroyed, stop the timer
                        print("Timer stopped: widget no longer exists")
                except Exception as e:
                    # Handle any errors that might occur when checking widget existence
                    print(f"Error updating timer: {e}")
            else:
                # Time's up - check if the widget still exists before submitting
                if self.winfo_exists():
                    self.submit_test()
        
        self.after(1000, update_timer)

    def confirm_submit_test(self):
        """Show confirmation dialog before submitting test"""
        # Count answered and unanswered questions
        answered = len(self.user_answers)
        unanswered = len(self.questions) - answered
        
        confirm = messagebox.askyesno(
            "Confirm Submission",
            f"Are you sure you want to submit your test?\n\n"
            f"Total Questions: {len(self.questions)}\n"
            f"Answered: {answered}\n"
            f"Not Answered: {unanswered}\n\n"
            "Once submitted, you cannot return to the test."
        )
        
        if confirm:
            self.submit_test()

    def submit_test(self):
        """Submit the test, save results to memory, and display results"""
        try:
            # Check if the widget still exists
            if not self.winfo_exists():
                print("Test widget no longer exists - cannot submit test")
                return
                
            # Cancel any pending timer updates
            self.after_cancel_all_timer_callbacks()
                
            # Calculate score
            correct_answers = 0
            for q_idx, user_ans in self.user_answers.items():
                if user_ans == self.questions[q_idx]["answer"]:
                    correct_answers += 1
            
            total_attempted = len(self.user_answers)
            score_percentage = (correct_answers / len(self.questions)) * 100
            
            # Get current user ID (assuming it's stored in app)
            user_id = getattr(self.app, 'current_user_id', 1)  # Default to 1 if not set
            
            # Save test results to memory
            test_id = self.save_test_results(user_id, correct_answers, total_attempted, score_percentage)
            
            # Save individual question responses
            self.save_question_responses(test_id)
            
            # Create and show results window
            self.show_results_window(correct_answers, total_attempted, score_percentage, test_id)
            
        except Exception as e:
            print(f"Error submitting test: {e}")
            messagebox.showerror("Error", "An error occurred while submitting your test.")
            
    def after_cancel_all_timer_callbacks(self):
        """Cancel any pending timer callbacks to prevent errors"""
        try:
            # Get all pending after callbacks
            for after_id in self.tk.call('after', 'info'):
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
        except Exception as e:
            print(f"Error canceling timer callbacks: {e}")

    def save_test_results(self, user_id, correct_answers, total_attempted, score_percentage):
        """Save overall test results to memory"""
        try:
            # Calculate time taken (in seconds)
            time_spent = 3600 - self.time_remaining  # Assuming 1-hour test
            
            # Generate a unique test ID
            test_id = int(datetime.now().timestamp())
            
            # Create test data
            test_data = {
                "id": test_id,
                "user_id": user_id,
                "subject": "Physics",
                "total_questions": len(self.questions),
                "attempted": total_attempted,
                "correct": correct_answers,
                "score_percentage": score_percentage,
                "test_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_taken": time_spent
            }
            
            # Store in memory
            if not hasattr(self, 'test_results'):
                self.test_results = []
            self.test_results.append(test_data)
            
            print(f"Test results stored with ID: {test_id}")
            
        except Exception as e:
            print(f"Error saving test results: {e}")
            messagebox.showerror("Error", "Could not save test results.")
        
        return test_id

    def save_question_responses(self, test_id):
        """Save individual question responses to memory"""
        if not test_id:
            return
        
        try:
            # Prepare responses
            responses = []
            
            # Insert each question response
            for q_idx in range(len(self.questions)):
                question = self.questions[q_idx]
                user_answer = self.user_answers.get(q_idx, "")
                is_correct = user_answer == question["answer"] if user_answer else False
                
                response_data = {
                    "test_id": test_id,
                    "question_number": q_idx + 1,
                    "question_text": question["question"],
                    "user_answer": user_answer,
                    "correct_answer": question["answer"],
                    "is_correct": is_correct
                }
                
                responses.append(response_data)
            
            # Store in memory
            if not hasattr(self, 'question_responses'):
                self.question_responses = {}
            self.question_responses[test_id] = responses
            
            print(f"Question responses stored for test ID: {test_id}")
            
        except Exception as e:
            print(f"Error saving responses: {e}")
            messagebox.showerror("Error", "Could not save question responses.")

    def show_results_window(self, correct_answers, total_attempted, score_percentage, test_id):
        """Display test results in a new window"""
        # Create results window
        results_window = ctk.CTkToplevel(self)
        results_window.title("Test Results")
        results_window.geometry("600x500")
        results_window.configure(fg_color="#1a1a1a")
        
        # Make window modal
        results_window.transient(self)
        results_window.grab_set()
        
        # Results header
        header = ctk.CTkLabel(
            results_window,
            text="Test Completed!",
            font=("Arial", 24, "bold"),
            text_color="#2ecc71"
        )
        header.pack(pady=(30, 20))
        
        # Results frame
        results_frame = ctk.CTkFrame(results_window, fg_color="#2c2c2c")
        results_frame.pack(padx=40, pady=20, fill="both", expand=True)
        
        # Add test ID for reference
        if test_id:
            test_id_label = ctk.CTkLabel(
                results_frame,
                text=f"Test ID: {test_id}",
                font=("Arial", 12),
                text_color="#aaaaaa"
            )
            test_id_label.pack(anchor="e", padx=20, pady=(10, 0))
        
        # Results details
        ctk.CTkLabel(
            results_frame,
            text=f"Total Questions: {len(self.questions)}",
            font=("Arial", 16),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=(30, 10))
        
        ctk.CTkLabel(
            results_frame,
            text=f"Answered: {total_attempted}",
            font=("Arial", 16),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        ctk.CTkLabel(
            results_frame,
            text=f"Correct Answers: {correct_answers}",
            font=("Arial", 16),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        # Score with color based on performance
        score_color = "#e74c3c"  # Red for poor
        if score_percentage >= 70:
            score_color = "#2ecc71"  # Green for good
        elif score_percentage >= 40:
            score_color = "#f39c12"  # Orange for average
        
        ctk.CTkLabel(
            results_frame,
            text=f"Score: {score_percentage:.1f}%",
            font=("Arial", 22, "bold"),
            text_color=score_color,
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        # Add time taken
        time_spent = 3600 - self.time_remaining
        mins, secs = divmod(time_spent, 60)
        hours, mins = divmod(mins, 60)
        
        ctk.CTkLabel(
            results_frame,
            text=f"Time Taken: {hours:02d}:{mins:02d}:{secs:02d}",
            font=("Arial", 16),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        # Button frame
        button_frame = ctk.CTkFrame(results_window, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        # View detailed report button
        report_btn = ctk.CTkButton(
            button_frame,
            text="View Detailed Report",
            command=lambda: self.view_detailed_report(test_id),
            font=("Arial", 14),
            fg_color="#3498db",
            hover_color="#2980b9",
            width=180,
            height=40,
            corner_radius=5
        )
        report_btn.pack(side="left", padx=40)
        
        # Back to dashboard button
        back_btn = ctk.CTkButton(
            button_frame,
            text="Return to Dashboard",
            command=lambda: [results_window.destroy(), self.create_ui()],
            font=("Arial", 14),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=180,
            height=40,
            corner_radius=5
        )
        back_btn.pack(side="right", padx=40)

    def view_detailed_report(self, test_id):
        """Show detailed test report with all questions and answers"""
        if not test_id:
            messagebox.showerror("Error", "Test data not available.")
            return
        
        test_data = None
        responses = []
        
        # Try to get data from memory
        if hasattr(self, 'test_results'):
            for test in self.test_results:
                if test.get('id') == test_id:
                    test_data = test
                    break
        
        if hasattr(self, 'question_responses') and test_id in self.question_responses:
            responses = self.question_responses[test_id]
        
        # If data not found, use sample data
        if not test_data:
            # Create sample test data for display
            test_data = {
                "id": test_id,
                "user_id": 1,
                "subject": "Physics",
                "total_questions": 30,
                "attempted": 25,
                "correct": 20,
                "score_percentage": 66.7,
                "test_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_taken": 1800
            }
        
        if not responses:
            # Create sample responses for display
            responses = [
                {
                    "test_id": test_id,
                    "question_number": 1,
                    "question_text": "What is Newton's First Law?",
                    "user_answer": "A",
                    "correct_answer": "A",
                    "is_correct": True
                },
                {
                    "test_id": test_id,
                    "question_number": 2,
                    "question_text": "What is the SI unit of force?",
                    "user_answer": "B",
                    "correct_answer": "C",
                    "is_correct": False
                }
            ]
        
        # Create a Row-like object for consistent access
        class DictRow:
            def __init__(self, data):
                self.data = data
            def __getitem__(self, key):
                return self.data.get(key)
        
        # Convert to DictRow objects
        test_data_row = DictRow(test_data)
        response_rows = [DictRow(item) for item in responses]
        
        # Continue with the detailed report display
        # Create a detailed report window...

    def load_chemistry_section(self):
        try:
            # Attempt to load chemistry questions
            questions = self.load_chemistry_questions()
            if not questions:
                print("No questions found for the chemistry section.")
                messagebox.showinfo("Error", "No chemistry questions available.")
            else:
                # If questions are loaded, display the mock test interface
                self.display_mock_test("Chemistry", questions)
        except Exception as e:
            print(f"Error loading chemistry section: {e}")
            messagebox.showerror("Error", f"Failed to load chemistry section: {e}")

    def load_chemistry_questions(self):
        # This is a sample implementation - you would fetch from your database
        questions = []
        
        # Chemistry topics
        topics = ["Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry", 
                  "Analytical Chemistry", "Coordination Chemistry"]
        
        # Sample chemistry questions
        chem_questions = [
            {
                "question": "Calculate the pH of a buffer solution containing 0.2 M CH₃COOH and 0.3 M CH₃COONa. (pKa of CH₃COOH = 4.74)",
                "options": [
                    "A. 4.22",
                    "B. 4.74",
                    "C. 5.00",
                    "D. 5.26"
                ],
                "answer": "D",
                "topic": "Physical Chemistry"
            },
            {
                "question": "Which of the following is not a characteristic property of ionic compounds?",
                "options": [
                    "A. High melting point",
                    "B. Low electrical conductivity in solid state",
                    "C. High electrical conductivity in molten state",
                    "D. Solubility in polar solvents"
                ],
                "answer": "B",
                "topic": "Inorganic Chemistry"
            },
            {
                "question": "The IUPAC name of the compound CH₃-CH=CH-CHO is:",
                "options": [
                    "A. 1-Butanal",
                    "B. 2-Butenal",
                    "C. But-2-enal",
                    "D. 3-Butenal"
                ],
                "answer": "C",
                "topic": "Organic Chemistry"
            }
        ]
        
        # Create 30 questions by cycling through the sample questions and varying them slightly
        for i in range(1, 31):
            # Choose a base question from the samples
            base_q = chem_questions[(i-1) % len(chem_questions)]
            topic = topics[(i-1) % len(topics)]
            
            # Create a variation of the question
            question = {
                "id": i,
                "question": base_q["question"],
                "options": base_q["options"],
                "answer": base_q["answer"],
                "topic": topic
            }
            
            questions.append(question)
        
        return questions

    def load_mathematics_section(self):
        try:
            # Attempt to load mathematics questions
            questions = self.load_mathematics_questions()
            if not questions:
                print("No questions found for the mathematics section.")
                messagebox.showinfo("Error", "No mathematics questions available.")
            else:
                # If questions are loaded, display the mock test interface
                self.display_mock_test("Mathematics", questions)
        except Exception as e:
            print(f"Error loading mathematics section: {e}")
            messagebox.showerror("Error", f"Failed to load mathematics section: {e}")

    def load_mathematics_questions(self):
        # This is a sample implementation - you would fetch from your database
        questions = []
        
        # Mathematics topics
        topics = ["Algebra", "Calculus", "Coordinate Geometry", 
                  "Trigonometry", "Vectors and 3D Geometry"]
        
        # Sample mathematics questions
        math_questions = [
            {
                "question": "If z = x + iy, where x and y are real, then the value of |z|² + |z̄|² is:",
                "options": [
                    "A. 2(x² + y²)",
                    "B. 2(x² - y²)",
                    "C. 4xy",
                    "D. 0"
                ],
                "answer": "A",
                "topic": "Algebra"
            },
            {
                "question": "The integral ∫(sin⁴x)dx equals:",
                "options": [
                    "A. (3sin x - sin 3x)/8 + C",
                    "B. (sin x - sin 3x)/4 + C",
                    "C. (3x - sin 2x)/8 + C",
                    "D. (3x - sin 2x + sin 4x/4)/8 + C"
                ],
                "answer": "C",
                "topic": "Calculus"
            },
            {
                "question": "The locus of the point of intersection of the lines x cos α + y sin α = a and x sin α - y cos α = 0, for different values of α, is:",
                "options": [
                    "A. A circle with center at origin",
                    "B. A straight line",
                    "C. An ellipse",
                    "D. A parabola"
                ],
                "answer": "C",
                "topic": "Coordinate Geometry"
            },
            {
                "question": "If tan A + tan B = tan (A + B), then:",
                "options": [
                    "A. tan A · tan B = 0",
                    "B. tan A · tan B = 1",
                    "C. tan A · tan B = -1",
                    "D. tan A = tan B"
                ],
                "answer": "C",
                "topic": "Trigonometry"
            },
            {
                "question": "If a vector is perpendicular to vectors 2i + j - k and i - j + 2k, then it is parallel to:",
                "options": [
                    "A. 3i + 5j + 4k",
                    "B. 5i + 3j - 4k",
                    "C. 5i - 3j + 4k",
                    "D. 3i - 5j - 4k"
                ],
                "answer": "B",
                "topic": "Vectors and 3D Geometry"
            }
        ]
        
        # Create 30 questions by cycling through the sample questions and varying them slightly
        for i in range(1, 31):
            # Choose a base question from the samples
            base_q = math_questions[(i-1) % len(math_questions)]
            topic = topics[(i-1) % len(topics)]
            
            # Create a variation of the question
            question = {
                "id": i,
                "question": base_q["question"],
                "options": base_q["options"],
                "answer": base_q["answer"],
                "topic": topic
            }
            
            questions.append(question)
        
        return questions

    def initialize_database(self):
        """Initialize in-memory storage for test results"""
        try:
            # Create in-memory storage for test results if not already done
            if not hasattr(self, 'test_results'):
                self.test_results = []
            
            if not hasattr(self, 'question_responses'):
                self.question_responses = {}
            
            # Create directory for test_results in case it's needed for other purposes
            os.makedirs("test_results", exist_ok=True)
            
            print("Test storage initialized successfully")
            
        except Exception as e:
            print(f"Error initializing storage: {e}")
            # If storage initialization fails, use backup storage

    def open_video_lectures(self):
        """Open PW-JEEWallah YouTube channel in web browser"""
        youtube_url = "http://www.youtube.com/@PW-JEEWallah"
        webbrowser.open(youtube_url)
    
    def open_formula_sheets(self):
        """Open MathonGo formula sheets in web browser"""
        formula_url = "https://www.mathongo.com/dw/formula-sheets/?subject=Physics"
        webbrowser.open(formula_url) 