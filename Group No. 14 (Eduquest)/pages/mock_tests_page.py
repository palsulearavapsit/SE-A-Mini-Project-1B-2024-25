import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk

class MockTestsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Create main container with dark background
        container = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        container.pack(fill="both", expand=True)
        
        # Create a grid layout with fixed sidebar width
        container.grid_columnconfigure(0, minsize=350, weight=0)  # Fixed width sidebar
        container.grid_columnconfigure(1, weight=1)  # Content area takes remaining space
        container.grid_rowconfigure(0, weight=1)
        
        # Create sidebar with green background
        sidebar = ctk.CTkFrame(container, corner_radius=0, fg_color="#2ecc71")
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(sidebar, text="Mock Tests", 
                                    font=("Arial", 36, "bold"), 
                                    text_color="white")
        sidebar_title.pack(pady=(70, 10), padx=20)
        
        # Sidebar tagline
        sidebar_tagline = ctk.CTkLabel(sidebar, text="Practice Makes Perfect!", 
                                      font=("Arial", 20), 
                                      text_color="white")
        sidebar_tagline.pack(pady=(0, 50), padx=20)
        
        # Sidebar features with icons
        features = [
            ("📝 Full-length practice exams", 20),
            ("⏱️ Timed sections", 20),
            ("📊 Detailed performance analysis", 20),
            ("📌 Topic-wise assessment", 20),
            ("📈 Progress tracking", 20),
            ("🔄 Regular updates", 20)
        ]
        
        for feature_text, padding in features:
            feature = ctk.CTkLabel(sidebar, text=feature_text, 
                                  font=("Arial", 18), 
                                  text_color="white",
                                  anchor="w")
            feature.pack(pady=padding, padx=40, fill="x")
        
        # Create main content area
        content_area = ctk.CTkFrame(container, corner_radius=0, fg_color="#1e1e1e")
        content_area.grid(row=0, column=1, sticky="nsew")
        
        # Back button
        back_btn = ctk.CTkButton(content_area, text="← Back", 
                               command=self.app.show_dashboard_page,
                               width=80,
                               height=32,
                               fg_color="#333333",
                               hover_color="#444444",
                               corner_radius=8)
        back_btn.pack(anchor="w", padx=30, pady=30)
        
        # Main heading
        main_heading = ctk.CTkLabel(content_area, text="Available Tests", 
                                  font=("Arial", 28, "bold"),
                                  text_color="white")
        main_heading.pack(pady=(20, 40))
        
        # Create a scrollable frame container
        scrollable_container = ctk.CTkScrollableFrame(
            content_area,
            fg_color="transparent",
            width=800,
            height=500,
            scrollbar_button_color="#3a3a3a",
            scrollbar_button_hover_color="#505050"
        )
        scrollable_container.pack(fill="both", expand=True, padx=30, pady=0)
        
        # Define test cards with improved data
        tests = [
            {
                "icon": "🎓",
                "name": "JEE Mock Test",
                "description": "Joint Entrance Examination practice test",
                "duration": "3 hours",
                "questions": "90 questions"
            },
            {
                "icon": "🔬",
                "name": "NEET Mock Test",
                "description": "National Eligibility cum Entrance Test",
                "duration": "3 hours",
                "questions": "180 questions"
            },
            {
                "icon": "🔧",
                "name": "GATE Mock Test",
                "description": "Graduate Aptitude Test in Engineering",
                "duration": "3 hours",
                "questions": "65 questions"
            },
            {
                "icon": "📊",
                "name": "CAT Mock Test",
                "description": "Common Admission Test practice exam",
                "duration": "2 hours",
                "questions": "100 questions"
            },
            {
                "icon": "📝",
                "name": "UPSC Mock Test",
                "description": "Civil Services Preliminary Examination",
                "duration": "2 hours",
                "questions": "100 questions"
            },
            {
                "icon": "💼",
                "name": "SSC CGL Mock Test",
                "description": "Staff Selection Commission Combined Graduate Level",
                "duration": "2 hours",
                "questions": "100 questions"
            },
            {
                "icon": "🏥",
                "name": "AIIMS Mock Test",
                "description": "All India Institute of Medical Sciences Entrance",
                "duration": "3 hours",
                "questions": "200 questions"
            },
            {
                "icon": "🧪",
                "name": "CSIR NET Mock Test",
                "description": "Council of Scientific & Industrial Research Exam",
                "duration": "3 hours",
                "questions": "120 questions"
            }
        ]
        
        # Create card frames 
        for i, test in enumerate(tests):
            # Create card container
            card = ctk.CTkFrame(scrollable_container, corner_radius=10, fg_color="#252525", height=120)
            card.pack(fill="x", padx=10, pady=15, ipady=15)
            
            # Icon with larger font
            icon_label = ctk.CTkLabel(card, text=test["icon"], 
                                    font=("Arial", 28), 
                                    width=40)
            icon_label.pack(side="left", padx=(30, 15))
            
            # Test name with more prominent display
            test_name = ctk.CTkLabel(card, text=test["name"], 
                                   font=("Arial", 22, "bold"),
                                   text_color="white")
            test_name.pack(side="left", padx=10)
            
            # Right-aligned description and button area
            details_area = ctk.CTkFrame(card, fg_color="transparent")
            details_area.pack(side="right", fill="y", padx=30)
            
            # Test description text
            description = ctk.CTkLabel(details_area, text=test["description"], 
                                      font=("Arial", 14),
                                      text_color="#cccccc")
            description.pack(anchor="e", pady=(5, 3))
            
            # Duration and questions info
            duration_info = ctk.CTkLabel(details_area, 
                                        text=f"Duration: {test['duration']} • {test['questions']}", 
                                        font=("Arial", 13), 
                                        text_color="#aaaaaa")
            duration_info.pack(anchor="e", pady=(0, 10))
            
            # Start button with improved styling
            start_btn = ctk.CTkButton(details_area, text="Start Test", 
                                    width=120,
                                    height=36,
                                    fg_color="#2ecc71",
                                    hover_color="#27ae60",
                                    text_color="white",
                                    font=("Arial", 14, "bold"),
                                    corner_radius=8,
                                    command=lambda test_type=test["name"].split()[0]: self.start_test(test_type))
            start_btn.pack(anchor="e")
    
    def start_test(self, test_type):
        """Start a subject test based on the selected test type"""
        # Map test types to subjects
        subject_mapping = {
            "JEE": "Physics,Chemistry,Mathematics",    # Default to Physics for JEE
            "NEET": "Biology,Chemistry,Physics",   # Default to Biology for NEET
            "GATE": "Engineering,Chemistry,Mathematics",
            "CAT": "Aptitude,Logical Reasoning,Verbal,Data Interpretation",
            "UPSC": "General Studies,Current Affairs,History,Geography",
            "SSC": "General Knowledge,Reasoning,Mathematics,English",
            "AIIMS": "Biology,Chemistry,Physics,General Knowledge",
            "CSIR": "Life Sciences,Chemical Sciences,Physical Sciences,Mathematics"
        }
        
        if test_type in subject_mapping:
            subject = subject_mapping[test_type]
            # Clear current page before creating new one
            self.app.clear_current_frame()
            # Initialize QuestionPage for the subject
            self.app.question_page = QuestionPage(self.master, self.app, subject)
            self.app.question_page.pack(fill="both", expand=True)


class QuestionPage(ctk.CTkFrame):
    def __init__(self, master, app, subject):
        super().__init__(master)
        self.master = master
        self.app = app
        self.subject = subject
        self.current_question_idx = 0
        self.user_answers = {}
        self.marked_for_review = set()
        self.visited_questions = set()
        
        # Increase to 3 hours (JEE-style exam)
        self.time_remaining = 3 * 60 * 60  # 3 hours in seconds
        self.timer_running = False
        
        # Fetch questions from database
        self.questions = self.fetch_questions_from_db(subject)
        self.total_questions = len(self.questions)
        
        if self.total_questions == 0:
            # Fallback to generated questions if no questions in database
            print("No questions found in database. Using generated questions.")
            self.questions = self.generate_questions(subject, 90)
            self.total_questions = len(self.questions)
            
        self.setup_ui()
        self.start_timer()
        self.display_question()
        
    def fetch_questions_from_db(self, subject):
        """Fetch questions from the database based on subject"""
        try:
            # Get questions from database using the database manager
            db_questions = self.app.db_manager.get_questions_by_subject(subject, 90)
            
            if not db_questions or len(db_questions) == 0:
                return []
                
            # Convert database questions to the format needed by this class
            formatted_questions = []
            for q in db_questions:
                formatted_question = {
                    "question": q["question_text"],
                    "options": {
                        "A": q["option_a"],
                        "B": q["option_b"],
                        "C": q["option_c"],
                        "D": q["option_d"]
                    },
                    "correct_answer": q["correct_answer"],
                    "subject": q["subject"]
                }
                formatted_questions.append(formatted_question)
                
            print(f"Fetched {len(formatted_questions)} questions from database for subject: {subject}")
            return formatted_questions
            
        except Exception as e:
            print(f"Error fetching questions from database: {e}")
            return []
        
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Set the background color
        self.configure(fg_color="#1a1a1a")
        
        # Top controls area
        top_controls = ctk.CTkFrame(self, fg_color="#2C2C2C")
        top_controls.pack(fill="x", padx=20, pady=20)
        
        # Question subject and timer
        subject_label = ctk.CTkLabel(
            top_controls, 
            text=f"Subject: {self.subject}", 
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        subject_label.pack(side="left", padx=20)
        
        # Time remaining display
        self.timer_label = ctk.CTkLabel(
            top_controls, 
            text="Time Remaining: 03:00:00", 
            font=("Arial", 16),
            text_color="#FF9800"
        )
        self.timer_label.pack(side="right", padx=20)
        
        # Question navigation panel
        nav_panel = ctk.CTkFrame(self, fg_color="#252525")
        nav_panel.pack(fill="x", padx=20, pady=(0, 20))
        
        # Question status indicators
        question_status_frame = ctk.CTkFrame(nav_panel, fg_color="transparent")
        question_status_frame.pack(pady=10, padx=10)
        
        # Grid of question numbers
        self.question_buttons = []
        btn_frame = ctk.CTkFrame(question_status_frame, fg_color="transparent")
        btn_frame.pack(padx=10, pady=10)
        
        # Create grid layout for question numbers
        rows = 5
        cols = self.total_questions // rows + (1 if self.total_questions % rows else 0)
        
        for i in range(self.total_questions):
            row = i % rows
            col = i // rows
            
            btn = ctk.CTkButton(
                btn_frame,
                text=str(i + 1),
                width=50,
                height=35,
                fg_color="#3C3C3C",
                hover_color="#505050",
                command=lambda idx=i: self.go_to_question(idx)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.question_buttons.append(btn)
        
        # Legend
        legend_frame = ctk.CTkFrame(nav_panel, fg_color="transparent")
        legend_frame.pack(pady=(0, 10), padx=10)
        
        legend_items = [
            ("Not Visited", "#3C3C3C"),
            ("Current", "#2E7D32"),
            ("Answered", "#1976D2"),
            ("Marked for Review", "#F57C00"),
            ("Answered & Marked", "#7B1FA2")
        ]
        
        for text, color in legend_items:
            item_frame = ctk.CTkFrame(legend_frame, fg_color="transparent")
            item_frame.pack(side="left", padx=15)
            
            color_box = ctk.CTkFrame(item_frame, width=20, height=20, fg_color=color)
            color_box.pack(side="left", padx=(0, 5))
            
            ctk.CTkLabel(
                item_frame, 
                text=text, 
                font=("Arial", 12),
                text_color="#CCCCCC"
            ).pack(side="left")
        
        # Main question content area
        self.question_frame = ctk.CTkFrame(self, fg_color="#2C2C2C")
        self.question_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Bottom controls
        bottom_controls = ctk.CTkFrame(self, fg_color="#252525")
        bottom_controls.pack(fill="x", padx=20, pady=(0, 20))
        
        # Navigation buttons
        button_frame = ctk.CTkFrame(bottom_controls, fg_color="transparent")
        button_frame.pack(pady=10, fill="x", padx=20)
        
        # Mark for Review button
        review_btn = ctk.CTkButton(
            button_frame,
            text="Mark for Review",
            width=150,
            height=35,
            fg_color="#3E3E3E",
            hover_color="#505050",
            command=self.mark_for_review
        )
        review_btn.pack(side="left", padx=10)
        
        # Submit Test button (on the right)
        submit_btn = ctk.CTkButton(
            button_frame,
            text="Submit Test",
            command=self.submit_test,
            width=150,
            height=40,
            fg_color="#D32F2F",
            hover_color="#B71C1C"
        )
        submit_btn.pack(side="right")
        
        # Next/Previous buttons
        nav_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        nav_buttons.pack(side="right", padx=10)
        
        self.prev_btn = ctk.CTkButton(
            nav_buttons,
            text="Previous",
            command=self.previous_question,
            width=120,
            height=40,
            fg_color="#505050",
            hover_color="#606060"
        )
        self.prev_btn.pack(side="left", padx=(0, 10))
        
        self.next_btn = ctk.CTkButton(
            nav_buttons,
            text="Next",
            command=self.next_question,
            width=120,
            height=40,
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        )
        self.next_btn.pack(side="left")
        
        # Clear response button (on the left side)
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Response",
            command=self.clear_response,
            width=150,
            height=40,
            fg_color="#673AB7",
            hover_color="#512DA8"
        )
        clear_btn.pack(side="left")
        
    def display_question(self):
        """Display the current question and options"""
        # Clear the question frame contents
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        # Get the question data
        q_num = self.current_question_idx + 1
        question_data = self.questions[self.current_question_idx]
        
        # Update question button styling
        for i, btn in enumerate(self.question_buttons):
            if i == self.current_question_idx:
                btn.configure(fg_color="#2E7D32")  # Current question (green)
            elif i in self.user_answers and i in self.marked_for_review:
                btn.configure(fg_color="#7B1FA2")  # Answered and marked (purple)
            elif i in self.user_answers:
                btn.configure(fg_color="#1976D2")  # Answered (blue)
            elif i in self.marked_for_review:
                btn.configure(fg_color="#F57C00")  # Marked for review (orange)
            else:
                btn.configure(fg_color="#3C3C3C")  # Not visited (gray)
        
        # Add the question to the visited set
        self.visited_questions.add(self.current_question_idx)
        
        # Question number and text
        question_header = ctk.CTkFrame(self.question_frame, fg_color="transparent")
        question_header.pack(fill="x", padx=20, pady=10)
        
        question_num_label = ctk.CTkLabel(
            question_header,
            text=f"Question {q_num} of {self.total_questions}",
            font=("Arial", 14),
            text_color="#CCCCCC"
        )
        question_num_label.pack(side="left")
        
        # Question text with larger font for readability
        question_text = ctk.CTkLabel(
            self.question_frame,
            text=question_data["question"],
            font=("Arial", 16),
            text_color="white",
            wraplength=800,
            justify="left"
        )
        question_text.pack(fill="x", padx=30, pady=(10, 30), anchor="w")
        
        # Options frame
        options_frame = ctk.CTkFrame(self.question_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=30, pady=10)
        
        # Create radio buttons for options
        self.selected_option = tk.StringVar()
        
        # Set the selected value if previously answered
        if self.current_question_idx in self.user_answers:
            self.selected_option.set(self.user_answers[self.current_question_idx])
        
        options = question_data["options"]
        for option_key, option_text in options.items():
            option_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
            option_frame.pack(fill="x", pady=10, anchor="w")
            
            radio_btn = ctk.CTkRadioButton(
                option_frame,
                text=f"{option_key}. {option_text}",
                variable=self.selected_option,
                value=option_key,
                font=("Arial", 14),
                text_color="white",
                fg_color="#1976D2",
                border_color="#AAAAAA"
            )
            radio_btn.pack(side="left")
        
    def next_question(self):
        """Move to the next question"""
        self.save_answer()
        if self.current_question_idx < self.total_questions - 1:
            self.current_question_idx += 1
            self.display_question()
    
    def previous_question(self):
        """Move to the previous question"""
        self.save_answer()
        if self.current_question_idx > 0:
            self.current_question_idx -= 1
            self.display_question()
    
    def go_to_question(self, index):
        """Jump to a specific question"""
        self.save_answer()
        self.current_question_idx = index
        self.display_question()
    
    def mark_for_review(self):
        """Mark the current question for review"""
        if self.current_question_idx in self.marked_for_review:
            self.marked_for_review.remove(self.current_question_idx)
        else:
            self.marked_for_review.add(self.current_question_idx)
        self.display_question()
    
    def clear_response(self):
        """Clear the response for the current question"""
        if self.current_question_idx in self.user_answers:
            del self.user_answers[self.current_question_idx]
        self.selected_option.set("")
        self.display_question()
    
    def save_answer(self):
        """Save the current answer"""
        selected = self.selected_option.get()
        if selected:
            self.user_answers[self.current_question_idx] = selected
    
    def submit_test(self):
        """Submit the test and show results"""
        self.save_answer()
        
        # Stop the timer
        self.timer_running = False
        
        # Initialize counters
        correct_answers = 0
        incorrect_answers = 0
        not_attempted = 0
        
        # Initialize subject-wise scores (raw counts)
        physics_correct = 0
        chemistry_correct = 0
        mathematics_correct = 0
        
        physics_incorrect = 0
        chemistry_incorrect = 0
        mathematics_incorrect = 0
        
        # Calculate scores based on question ranges and JEE marking scheme
        total_marks = 0
        physics_marks = 0
        chemistry_marks = 0
        mathematics_marks = 0
        
        # Determine question ranges for each subject
        subject_questions = {}
        physics_count = 0
        chemistry_count = 0
        mathematics_count = 0
        
        # Count questions by subject
        for idx, question in enumerate(self.questions):
            if question["subject"] == "Physics":
                physics_count += 1
                if "subject_questions" not in subject_questions:
                    subject_questions["Physics"] = []
                subject_questions["Physics"].append(idx)
            elif question["subject"] == "Chemistry":
                chemistry_count += 1
                if "Chemistry" not in subject_questions:
                    subject_questions["Chemistry"] = []
                subject_questions["Chemistry"].append(idx)
            elif question["subject"] == "Mathematics":
                mathematics_count += 1
                if "Mathematics" not in subject_questions:
                    subject_questions["Mathematics"] = []
                subject_questions["Mathematics"].append(idx)
        
        for q_idx in range(self.total_questions):
            if q_idx in self.user_answers:
                if self.user_answers[q_idx] == self.questions[q_idx]["correct_answer"]:
                    correct_answers += 1
                    total_marks += 4  # +4 for correct answer
                    
                    # Determine subject based on question's subject property
                    subject = self.questions[q_idx]["subject"]
                    if subject == "Physics":
                        physics_correct += 1
                        physics_marks += 4
                    elif subject == "Chemistry":
                        chemistry_correct += 1
                        chemistry_marks += 4
                    elif subject == "Mathematics":
                        mathematics_correct += 1
                        mathematics_marks += 4
                else:
                    incorrect_answers += 1
                    total_marks -= 1  # -1 for incorrect answer
                    
                    # Determine subject based on question's subject property
                    subject = self.questions[q_idx]["subject"]
                    if subject == "Physics":
                        physics_incorrect += 1
                        physics_marks -= 1
                    elif subject == "Chemistry":
                        chemistry_incorrect += 1
                        chemistry_marks -= 1
                    elif subject == "Mathematics":
                        mathematics_incorrect += 1
                        mathematics_marks -= 1
            else:
                not_attempted += 1
        
        # Calculate maximum possible score (4 marks * total questions)
        max_possible_marks = self.total_questions * 4
        
        # Calculate percentage score
        score_percentage = (total_marks / max_possible_marks) * 100 if max_possible_marks > 0 else 0
        
        # Calculate subject-wise percentages
        physics_percentage = 0
        chemistry_percentage = 0 
        mathematics_percentage = 0
        
        if physics_count > 0:
            max_physics_marks = physics_count * 4
            physics_percentage = (physics_marks / max_physics_marks) * 100 if max_physics_marks > 0 else 0
            
        if chemistry_count > 0:
            max_chemistry_marks = chemistry_count * 4
            chemistry_percentage = (chemistry_marks / max_chemistry_marks) * 100 if max_chemistry_marks > 0 else 0
            
        if mathematics_count > 0:
            max_mathematics_marks = mathematics_count * 4
            mathematics_percentage = (mathematics_marks / max_mathematics_marks) * 100 if max_mathematics_marks > 0 else 0
        
        # Calculate time spent (seconds)
        test_duration = 3 * 60 * 60  # 3 hours in seconds
        time_spent = test_duration - self.time_remaining
        
        # Create a comprehensive test result dictionary
        test_result = {
            'subject': self.subject,
            'total_marks': total_marks,
            'max_marks': max_possible_marks,
            'score_percentage': score_percentage,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'not_attempted': not_attempted,
            'time_spent': time_spent,
            'physics_marks': physics_marks,
            'chemistry_marks': chemistry_marks,
            'mathematics_marks': mathematics_marks,
            'physics_percentage': physics_percentage,
            'chemistry_percentage': chemistry_percentage,
            'mathematics_percentage': mathematics_percentage,
            'physics_correct': physics_correct,
            'physics_incorrect': physics_incorrect,
            'chemistry_correct': chemistry_correct,
            'chemistry_incorrect': chemistry_incorrect,
            'mathematics_correct': mathematics_correct,
            'mathematics_incorrect': mathematics_incorrect
        }
        
        # Save test results to database if the user is logged in
        if hasattr(self.app, 'current_user_id') and self.app.current_user_id:
            try:
                query = """
                    INSERT INTO user_progress (
                        user_id, score, total_marks, max_marks, correct_answers, 
                        incorrect_answers, not_attempted, time_spent, 
                        physics_marks, chemistry_marks, mathematics_marks,
                        physics_percentage, chemistry_percentage, mathematics_percentage,
                        physics_score, chemistry_score, mathematics_score,
                        completed, date_taken
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                    )
                """
                
                params = (
                    self.app.current_user_id, score_percentage, total_marks, max_possible_marks, correct_answers,
                    incorrect_answers, not_attempted, time_spent,
                    physics_marks, chemistry_marks, mathematics_marks,
                    physics_percentage, chemistry_percentage, mathematics_percentage,
                    physics_percentage, chemistry_percentage, mathematics_percentage,
                    1  # completed
                )
                
                success = self.app.db_manager.execute_query(query, params)
                if success:
                    print("Test results saved to database successfully!")
                else:
                    print("Failed to save test results to database.")
            except Exception as e:
                print(f"Error saving test results: {e}")
        
        # Show the results page with the test results
        self.app.show_mock_test_result(test_result)
    
    def start_timer(self):
        """Start the exam timer"""
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display"""
        if self.timer_running and self.time_remaining > 0:
            self.time_remaining -= 1
            
            # Format time as HH:MM:SS
            hours = self.time_remaining // 3600
            minutes = (self.time_remaining % 3600) // 60
            seconds = self.time_remaining % 60
            
            time_str = f"Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.configure(text=time_str)
            
            # Change color when time is running low
            if self.time_remaining < 300:  # Less than 5 minutes
                self.timer_label.configure(text_color="#f44336")  # Red color
            
            # Schedule next update
            self.after(1000, self.update_timer)
        elif self.time_remaining <= 0:
            self.timer_label.configure(text="Time Remaining: 00:00:00", text_color="#f44336")
            messagebox.showinfo("Time's Up", "Your time is up. The test will be submitted automatically.")
            self.submit_test()
    
    def generate_questions(self, subject, count):
        """
        Fallback method in case database questions aren't available.
        This is kept as a minimal fallback, since questions are now stored in the database.
        """
        print(f"Warning: No questions found in database for {subject}. Using empty question set.")
        print("Please ensure the database is properly set up and populated with questions.")
        
        # Return an empty list - mock tests should now use database questions instead
        return []
