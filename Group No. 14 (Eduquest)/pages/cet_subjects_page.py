import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import time
from datetime import datetime
import webbrowser

class CETSubjectsPage(ctk.CTkFrame):
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
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="CET Preparation",
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
            text="Common Entrance Test",
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
        
        # Subject data for CET
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
            text="Recent CET Questions",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        recent_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Sample recent CET questions
        recent_questions = [
            {
                "question": "A particle moves in a straight line with a constant acceleration of 2 m/s². If its initial velocity is 4 m/s, what is its velocity after 3 seconds?",
                "subject": "Physics",
                "year": "2022"
            },
            {
                "question": "What is the pH of a 0.01 M solution of HCl?",
                "subject": "Chemistry",
                "year": "2022"
            },
            {
                "question": "If the roots of the equation x² - 5x + 6 = 0 are α and β, then what is the value of α² + β²?",
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
        
        # Resources grid
        resources_grid = ctk.CTkFrame(resources_section, fg_color="transparent")
        resources_grid.pack(fill="x", padx=20, pady=10)
        
        resources = [
            {"name": "Video Lectures", "icon": "🎬"},
            {"name": "Formula Sheets", "icon": "📄"}
        ]
        
        # Configure grid columns
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
        # Sample CET physics questions
        questions = []
        for i in range(1, 31):  # Create 30 sample questions
            questions.append({
                "id": i,
                "question": "A particle moves in a straight line with a constant acceleration of 2 m/s². If its initial velocity is 4 m/s, what is its velocity after 3 seconds?",
                "options": [
                    "A. 6 m/s",
                    "B. 8 m/s",
                    "C. 10 m/s",
                    "D. 12 m/s"
                ],
                "answer": "C",
                "topic": "Mechanics"
            })
        return questions

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
        # Sample CET chemistry questions
        questions = []
        
        # Chemistry topics
        topics = ["Physical Chemistry", "Organic Chemistry", "Inorganic Chemistry", 
                  "Analytical Chemistry", "Coordination Chemistry"]
        
        # Sample chemistry questions
        chem_questions = [
            {
                "question": "What is the pH of a 0.01 M solution of HCl?",
                "options": [
                    "A. 1",
                    "B. 2",
                    "C. 3",
                    "D. 4"
                ],
                "answer": "B",
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
        
        # Create 30 questions by cycling through the sample questions
        for i in range(1, 31):
            base_q = chem_questions[(i-1) % len(chem_questions)]
            topic = topics[(i-1) % len(topics)]
            
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
        # Sample CET mathematics questions
        questions = []
        
        # Mathematics topics
        topics = ["Algebra", "Calculus", "Coordinate Geometry", 
                  "Trigonometry", "Vectors and 3D Geometry"]
        
        # Sample mathematics questions
        math_questions = [
            {
                "question": "If the roots of the equation x² - 5x + 6 = 0 are α and β, then what is the value of α² + β²?",
                "options": [
                    "A. 13",
                    "B. 17",
                    "C. 19",
                    "D. 25"
                ],
                "answer": "A",
                "topic": "Algebra"
            },
            {
                "question": "The derivative of sin²x with respect to x is:",
                "options": [
                    "A. 2sinx",
                    "B. 2sinxcosx",
                    "C. sin2x",
                    "D. cos2x"
                ],
                "answer": "C",
                "topic": "Calculus"
            },
            {
                "question": "The equation of the line passing through (2,3) and perpendicular to the line 3x + 4y = 5 is:",
                "options": [
                    "A. 4x - 3y + 1 = 0",
                    "B. 3x - 4y + 6 = 0",
                    "C. 4x + 3y - 17 = 0",
                    "D. 3x + 4y - 18 = 0"
                ],
                "answer": "A",
                "topic": "Coordinate Geometry"
            }
        ]
        
        # Create 30 questions by cycling through the sample questions
        for i in range(1, 31):
            base_q = math_questions[(i-1) % len(math_questions)]
            topic = topics[(i-1) % len(topics)]
            
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

    def open_video_lectures(self):
        """Open CET preparation YouTube channel in web browser"""
        youtube_url = "https://www.youtube.com/results?search_query=cet+preparation"
        webbrowser.open(youtube_url)
    
    def open_formula_sheets(self):
        """Open CET formula sheets in web browser"""
        formula_url = "https://www.google.com/search?q=cet+formula+sheets"
        webbrowser.open(formula_url)

    def display_mock_test(self, subject, questions):
        """Display the mock test interface for a given subject"""
        # Clear the current frame
        self.app.clear_current_frame()
        
        # Create and display the question page
        question_page = QuestionPage(self.app.root, self.app, subject, questions)
        question_page.pack(fill="both", expand=True)

# New class for the Question Page
class QuestionPage(ctk.CTkFrame):
    def __init__(self, master, app, subject, questions):
        super().__init__(master, corner_radius=0)
        self.master = master
        self.app = app
        self.subject = subject
        self.questions = questions
        self.current_question_idx = 0
        self.total_questions = len(questions)
        
        # Store user answers
        self.user_answers = {}
        # Track visited questions
        self.visited_questions = set()
        # Track answered questions
        self.answered_questions = set()
        # Track marked questions
        self.marked_questions = set()
        
        # Set test time (60 minutes)
        self.time_remaining = 60 * 60  # seconds
        
        # Create UI elements
        self.create_ui()
        
        # Start timer
        self.update_timer()
    
    def create_ui(self):
        # Set background color
        self.configure(fg_color="#1a1a1a")
        
        # Create header
        header_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Test title in header
        test_title = ctk.CTkLabel(
            header_frame,
            text=f"CET {self.subject} Mock Test",
            font=("Arial", 20, "bold"),
        )
        test_title.pack(side="left", padx=20, pady=20)
        
        # User info frame
        user_info_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", height=100)
        user_info_frame.pack(fill="x")
        
        # User icon
        user_icon = ctk.CTkLabel(
            user_info_frame,
            text="👤",
            font=("Arial", 24)
        )
        user_icon.pack(side="left", padx=20, pady=10)
        
        # User details
        user_info = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        user_info.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        
        candidate_name = ctk.CTkLabel(
            user_info,
            text="Candidate Name: User",
            font=("Arial", 12),
            anchor="w"
        )
        candidate_name.pack(anchor="w")
        
        exam_name = ctk.CTkLabel(
            user_info,
            text=f"Exam Name: {self.subject}",
            font=("Arial", 12),
            anchor="w"
        )
        exam_name.pack(anchor="w")
        
        subject_name = ctk.CTkLabel(
            user_info,
            text=f"Subject Name: {self.subject}",
            font=("Arial", 12),
            anchor="w"
        )
        subject_name.pack(anchor="w")
        
        # Timer frame on the right
        timer_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        timer_frame.pack(side="right", padx=20, pady=10)
        
        timer_label = ctk.CTkLabel(
            timer_frame,
            text="Remaining Time",
            font=("Arial", 12)
        )
        timer_label.pack()
        
        self.timer_value = ctk.CTkLabel(
            timer_frame,
            text="01:00:00",
            font=("Arial", 20, "bold"),
            text_color="#4cc9f0"
        )
        self.timer_value.pack()
        
        # Main content area - split into question area and navigation panel
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Question area (left side)
        question_frame = ctk.CTkFrame(content_frame, fg_color="#2c2c2c", corner_radius=10)
        question_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Question number and text
        self.question_number_label = ctk.CTkLabel(
            question_frame,
            text=f"Question 1/{self.total_questions}",
            font=("Arial", 14),
            anchor="w"
        )
        self.question_number_label.pack(anchor="w", padx=20, pady=10)
        
        # Question text
        self.question_text = ctk.CTkLabel(
            question_frame,
            text="",
            font=("Arial", 14),
            justify="left",
            wraplength=800,
            anchor="w"
        )
        self.question_text.pack(anchor="w", padx=20, pady=10, fill="x")
        
        # Options frame
        self.options_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=20, pady=20)
        
        # Option radio buttons (will be created dynamically)
        self.option_vars = {}
        self.option_buttons = {}
        
        # Navigation panel (right side)
        nav_panel = ctk.CTkFrame(content_frame, fg_color="#2c2c2c", corner_radius=10, width=200)
        nav_panel.pack(side="right", fill="y", padx=(10, 0))
        nav_panel.pack_propagate(False)
        
        # Question status indicators
        status_frame = ctk.CTkFrame(nav_panel, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=10)
        
        # Status legends
        status_types = [
            {"count": 1, "text": "Not Visited", "color": "#6c757d"},
            {"count": 0, "text": "Not Answered", "color": "#dc3545"},
            {"count": 0, "text": "Answered", "color": "#28a745"},
            {"count": 0, "text": "Marked for Review", "color": "#ffc107"},
            {"count": 0, "text": "Answered & Marked for Review", "color": "#6f42c1"}
        ]
        
        for status in status_types:
            status_row = ctk.CTkFrame(status_frame, fg_color="transparent")
            status_row.pack(fill="x", pady=2)
            
            count_label = ctk.CTkLabel(
                status_row,
                text=str(status["count"]),
                fg_color=status["color"],
                corner_radius=5,
                width=30,
                height=30
            )
            count_label.pack(side="left", padx=(0, 5))
            
            text_label = ctk.CTkLabel(
                status_row,
                text=status["text"],
                font=("Arial", 12),
                anchor="w"
            )
            text_label.pack(side="left", fill="x", expand=True)
        
        # Question number buttons grid
        question_grid = ctk.CTkFrame(nav_panel, fg_color="transparent")
        question_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a grid of question number buttons
        self.question_buttons = {}
        rows = (self.total_questions + 4) // 5  # 5 columns
        
        for i in range(self.total_questions):
            q_num = i + 1
            row = i // 5
            col = i % 5
            
            q_button = ctk.CTkButton(
                question_grid,
                text=str(q_num),
                width=30,
                height=30,
                fg_color="#6c757d",
                hover_color="#5a6268",
                command=lambda idx=i: self.jump_to_question(idx)
            )
            q_button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.question_buttons[q_num] = q_button
        
        # Bottom navigation buttons
        nav_buttons = ctk.CTkFrame(self, fg_color="transparent", height=50)
        nav_buttons.pack(fill="x", pady=10)
        
        # Previous button
        prev_button = ctk.CTkButton(
            nav_buttons,
            text="← Previous",
            command=self.prev_question,
            width=100,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        prev_button.pack(side="left", padx=20, pady=10)
        
        # Submit test button
        submit_button = ctk.CTkButton(
            nav_buttons,
            text="Submit Test",
            command=self.submit_test,
            width=150,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        submit_button.pack(side="left", padx=20, pady=10)
        
        # Next button
        next_button = ctk.CTkButton(
            nav_buttons,
            text="Next →",
            command=self.next_question,
            width=100,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        next_button.pack(side="right", padx=20, pady=10)
        
        # Load first question
        self.load_question(0)
    
    def load_question(self, idx):
        """Load a specific question"""
        if idx < 0 or idx >= self.total_questions:
            return
            
        self.current_question_idx = idx
        question_data = self.questions[idx]
        
        # Mark as visited
        self.visited_questions.add(idx)
        
        # Update question number
        self.question_number_label.configure(text=f"Question {idx+1}/{self.total_questions}")
        
        # Update question text
        self.question_text.configure(text=question_data["question"])
        
        # Clear previous options
        for widget in self.options_frame.winfo_children():
            widget.destroy()
            
        # Create radio variable
        self.option_var = tk.StringVar(value="")
        
        # Set to saved answer if exists
        if idx in self.user_answers:
            self.option_var.set(self.user_answers[idx])
        
        # Create option buttons
        for i, option_text in enumerate(question_data["options"]):
            option_id = option_text.split(".")[0].strip()  # Extract A, B, C, D
            
            option_button = ctk.CTkRadioButton(
                self.options_frame,
                text=option_text,
                variable=self.option_var,
                value=option_id,
                font=("Arial", 14),
                command=self.save_answer
            )
            option_button.pack(anchor="w", pady=5)
        
        # Update question button status
        self.update_question_status(idx)
    
    def save_answer(self):
        """Save the current answer"""
        selected_option = self.option_var.get()
        if selected_option:
            self.user_answers[self.current_question_idx] = selected_option
            self.answered_questions.add(self.current_question_idx)
            self.update_question_status(self.current_question_idx)
    
    def update_question_status(self, idx):
        """Update the status of a question button"""
        button = self.question_buttons[idx + 1]
        
        # Default status (not visited)
        color = "#6c757d"
        
        if idx in self.answered_questions and idx in self.marked_questions:
            # Answered and marked
            color = "#6f42c1"
        elif idx in self.marked_questions:
            # Marked for review
            color = "#ffc107"
        elif idx in self.answered_questions:
            # Answered
            color = "#28a745"
        elif idx in self.visited_questions:
            # Visited but not answered
            color = "#dc3545"
            
        button.configure(fg_color=color)
        
        # Also update the current button if applicable
        if idx == 0:
            button.configure(fg_color="#007bff")
    
    def next_question(self):
        """Go to the next question"""
        if self.current_question_idx < self.total_questions - 1:
            self.load_question(self.current_question_idx + 1)
    
    def prev_question(self):
        """Go to the previous question"""
        if self.current_question_idx > 0:
            self.load_question(self.current_question_idx - 1)
    
    def jump_to_question(self, idx):
        """Jump to a specific question"""
        self.load_question(idx)
    
    def mark_for_review(self):
        """Mark current question for review"""
        idx = self.current_question_idx
        if idx in self.marked_questions:
            self.marked_questions.remove(idx)
        else:
            self.marked_questions.add(idx)
        self.update_question_status(idx)
    
    def update_timer(self):
        """Update the timer display"""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            
            # Format time as HH:MM:SS
            hours = self.time_remaining // 3600
            minutes = (self.time_remaining % 3600) // 60
            seconds = self.time_remaining % 60
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_value.configure(text=time_str)
            
            # Schedule next update
            self.after(1000, self.update_timer)
        else:
            # Time's up - auto submit
            self.submit_test()
    
    def submit_test(self):
        """Submit the test and show results"""
        # Ask for confirmation
        if not self.answered_questions:
            messagebox.showwarning("Warning", "You haven't answered any questions yet. Are you sure you want to submit?")
            return
            
        confirm = messagebox.askyesno("Submit Test", "Are you sure you want to submit your test?")
        if confirm:
            # Calculate score
            correct_answers = 0
            for q_idx, answer in self.user_answers.items():
                correct = self.questions[q_idx]["answer"]
                if answer == correct:
                    correct_answers += 1
            
            # Create result object
            result = {
                "score": correct_answers,
                "percentage": (correct_answers / self.total_questions) * 100,
                "passed": (correct_answers / self.total_questions) >= 0.4,  # 40% passing threshold
                "time_taken": 3600 - self.time_remaining,  # seconds
                "correct_answers": correct_answers,
                "total_questions": self.total_questions
            }
            
            # Save test results to memory
            test_id = self.save_test_results(correct_answers, len(self.answered_questions))
            
            # Show results window
            self.show_results_window(correct_answers, len(self.answered_questions), result["percentage"], test_id)
    
    def save_test_results(self, correct_answers, total_attempted):
        """Save test results to memory"""
        try:
            # Calculate time taken (in seconds)
            time_spent = 3600 - self.time_remaining  # Assuming 1-hour test
            
            # Generate a unique test ID
            test_id = int(datetime.now().timestamp())
            
            # Create test data
            test_data = {
                "id": test_id,
                "user_id": getattr(self.app, 'current_user_id', 1),  # Default to 1 if not set
                "subject": self.subject,
                "total_questions": self.total_questions,
                "attempted": total_attempted,
                "correct": correct_answers,
                "score_percentage": (correct_answers / self.total_questions) * 100,
                "test_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_taken": time_spent
            }
            
            # Store in memory
            if not hasattr(self.app, 'test_results'):
                self.app.test_results = []
            self.app.test_results.append(test_data)
            
            print(f"Test results stored with ID: {test_id}")
            return test_id
            
        except Exception as e:
            print(f"Error saving test results: {e}")
            messagebox.showerror("Error", "Could not save test results.")
            return None
    
    def show_results_window(self, correct_answers, total_attempted, score_percentage, test_id):
        """Display test results in a popup window"""
        # Create results window
        results_window = ctk.CTkToplevel(self)
        results_window.title("Test Results")
        results_window.geometry("400x600")  # Increased height to match the image
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
        results_frame.pack(padx=40, pady=10, fill="x", expand=False)  # Changed to fill="x" not both
        
        # Add test ID for reference
        if test_id:
            test_id_label = ctk.CTkLabel(
                results_frame,
                text=f"Test ID: {test_id}",
                font=("Arial", 12),
                text_color="#aaaaaa"
            )
            test_id_label.pack(anchor="e", padx=20, pady=(10, 0))
        
        # Results details - simpler layout to match screenshot
        ctk.CTkLabel(
            results_frame,
            text=f"Total Questions: {self.total_questions}",
            font=("Arial", 14),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=(30, 10))
        
        ctk.CTkLabel(
            results_frame,
            text=f"Answered: {total_attempted}",
            font=("Arial", 14),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        ctk.CTkLabel(
            results_frame,
            text=f"Correct Answers: {correct_answers}",
            font=("Arial", 14),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        # Score with red color for low score
        score_color = "#e74c3c"  # Red color for score
        
        ctk.CTkLabel(
            results_frame,
            text=f"Score: {score_percentage:.1f}%",
            font=("Arial", 20, "bold"),
            text_color=score_color,
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        # Time taken in simpler format
        time_spent = 3600 - self.time_remaining
        mins, secs = divmod(time_spent, 60)
        hours, mins = divmod(mins, 60)
        
        ctk.CTkLabel(
            results_frame,
            text=f"Time Taken: {hours:02d}:{mins:02d}:{secs:02d}",
            font=("Arial", 14),
            anchor="w"
        ).pack(anchor="w", padx=30, pady=10)
        
        # Result status - PASSED or FAILED
        status_text = "PASSED" if score_percentage >= 40 else "FAILED"
        status_color = "#2ecc71" if score_percentage >= 40 else "#e74c3c"
        
        ctk.CTkLabel(
            results_frame,
            text=status_text,
            font=("Arial", 20, "bold"),
            text_color=status_color,
            anchor="center"
        ).pack(pady=15)
        
        # Back to Dashboard button - placed at the bottom with significant spacing
        bottom_spacing = ctk.CTkFrame(results_window, fg_color="transparent", height=80)
        bottom_spacing.pack(fill="x", expand=True)
        
        # Add button directly to results window for better positioning
        back_btn = ctk.CTkButton(
            results_window,
            text="← Back to Dashboard",
            command=lambda: [results_window.destroy(), self.app.show_dashboard_page()],
            font=("Arial", 14),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=240,
            height=45,
            corner_radius=5
        )
        back_btn.pack(pady=(0, 30))
    
    def handle_back(self):
        """Handle back button press"""
        confirm = messagebox.askyesno("Exit Test", "Are you sure you want to exit? Your progress will be lost.")
        if confirm:
            self.app.show_cet_subjects() 