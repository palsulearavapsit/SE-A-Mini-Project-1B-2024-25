import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import os
import random

class PreviousYearQuestionsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, corner_radius=0)
        self.master = master
        self.app = app
        
        # Store selected exam and year
        self.selected_exam = tk.StringVar(value="JEE")
        self.selected_year = tk.StringVar(value="2023")
        
        # Create UI components
        self.create_ui()
        
        # Populate initial content
        self.load_questions()
    
    def create_ui(self):
        # Top bar with title
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        self.title_label = ctk.CTkLabel(
            self.top_frame, 
            text="Previous Year Questions", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Frame for filters (exam type and year)
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Exam selection
        self.exam_label = ctk.CTkLabel(self.filter_frame, text="Select Exam:")
        self.exam_label.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        exams = ["JEE", "NEET", "GATE", "CET"]
        self.exam_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            values=exams,
            variable=self.selected_exam,
            command=self.load_questions
        )
        self.exam_dropdown.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Year selection
        self.year_label = ctk.CTkLabel(self.filter_frame, text="Select Year:")
        self.year_label.pack(side=tk.LEFT, padx=(20, 5), pady=10)
        
        current_year = 2023  # You might want to use the actual current year
        years = [str(year) for year in range(current_year, current_year-10, -1)]
        self.year_dropdown = ctk.CTkOptionMenu(
            self.filter_frame,
            values=years,
            variable=self.selected_year,
            command=self.load_questions
        )
        self.year_dropdown.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Search box
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.filter_frame,
            placeholder_text="Search questions...",
            width=250,
            textvariable=self.search_var
        )
        self.search_entry.pack(side=tk.RIGHT, padx=10, pady=10)
        self.search_var.trace("w", lambda name, index, mode: self.filter_questions())
        
        # Create main content area with scrollable frame
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Back to dashboard button
        self.back_button = ctk.CTkButton(
            self,
            text="Back to Dashboard",
            command=self.app.show_dashboard_page
        )
        self.back_button.pack(padx=20, pady=20, side=tk.BOTTOM)
    
    def load_questions(self, *args):
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        exam = self.selected_exam.get()
        year = self.selected_year.get()
        
        # This is where you would fetch questions from your database
        # For now, we'll use dummy data
        questions = self.get_dummy_questions(exam, year)
        
        if not questions:
            no_questions_label = ctk.CTkLabel(
                self.content_frame,
                text=f"No questions found for {exam} {year}",
                font=ctk.CTkFont(size=16)
            )
            no_questions_label.pack(pady=50)
            return
        
        # Display questions
        for i, question in enumerate(questions):
            self.create_question_card(i+1, question)
    
    def create_question_card(self, number, question_data):
        question_frame = ctk.CTkFrame(self.content_frame)
        question_frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        # Question number and subject tag
        header_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        num_label = ctk.CTkLabel(
            header_frame,
            text=f"Q{number}.",
            font=ctk.CTkFont(weight="bold")
        )
        num_label.pack(side=tk.LEFT)
        
        subject_label = ctk.CTkLabel(
            header_frame,
            text=question_data['subject'],
            font=ctk.CTkFont(size=12),
            fg_color="#4b6bff",
            corner_radius=5,
            text_color="white"
        )
        subject_label.pack(side=tk.RIGHT, padx=5)
        
        # Question text
        question_text = ctk.CTkLabel(
            question_frame,
            text=question_data['question_text'],
            wraplength=800,
            justify="left"
        )
        question_text.pack(fill=tk.X, padx=10, pady=5, anchor="w")
        
        # Options (if multiple choice)
        if 'options' in question_data and question_data['options']:
            options_frame = ctk.CTkFrame(question_frame, fg_color="transparent")
            options_frame.pack(fill=tk.X, padx=20, pady=5)
            
            for opt_key, opt_text in question_data['options'].items():
                option_label = ctk.CTkLabel(
                    options_frame, 
                    text=f"{opt_key}) {opt_text}",
                    anchor="w"
                )
                option_label.pack(fill=tk.X, pady=2, anchor="w")
        
        # Answer button
        answer_button = ctk.CTkButton(
            question_frame,
            text="View Answer",
            width=100,
            height=28,
            command=lambda q=question_data: self.show_answer(q)
        )
        answer_button.pack(anchor="e", padx=10, pady=10)
        
        # Store the question data for reference
        question_frame.question_data = question_data
    
    def show_answer(self, question_data):
        answer_window = ctk.CTkToplevel(self)
        answer_window.title(f"Answer - {question_data['subject']}")
        answer_window.geometry("600x400")
        answer_window.grab_set()  # Make it modal
        
        # Title
        title_label = ctk.CTkLabel(
            answer_window,
            text="Answer & Solution",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(padx=20, pady=20)
        
        # Question recap
        question_label = ctk.CTkLabel(
            answer_window,
            text=question_data['question_text'],
            wraplength=550,
            justify="left",
            font=ctk.CTkFont(size=12)
        )
        question_label.pack(fill=tk.X, padx=20, pady=5, anchor="w")
        
        # Correct answer
        correct_answer = ctk.CTkLabel(
            answer_window,
            text=f"Correct Answer: {question_data['answer']}",
            font=ctk.CTkFont(weight="bold"),
            text_color="#2ecc71"
        )
        correct_answer.pack(fill=tk.X, padx=20, pady=10, anchor="w")
        
        # Explanation
        if 'explanation' in question_data:
            explanation_frame = ctk.CTkScrollableFrame(answer_window, height=200)
            explanation_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            explanation_label = ctk.CTkLabel(
                explanation_frame,
                text=question_data['explanation'],
                wraplength=550,
                justify="left"
            )
            explanation_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        close_button = ctk.CTkButton(
            answer_window,
            text="Close",
            command=answer_window.destroy
        )
        close_button.pack(pady=20)
    
    def filter_questions(self):
        search_term = self.search_var.get().lower()
        
        for widget in self.content_frame.winfo_children():
            if hasattr(widget, 'question_data'):
                question_text = widget.question_data['question_text'].lower()
                subject = widget.question_data['subject'].lower()
                
                if search_term in question_text or search_term in subject:
                    widget.pack(fill=tk.X, padx=5, pady=5, ipady=5)
                else:
                    widget.pack_forget()
    
    def get_dummy_questions(self, exam, year):
        # This function provides sample data; replace with database fetching
        # In a real implementation, you would fetch from your database instead
        
        # Sample subjects based on exam type
        subjects = {
            "JEE": ["Physics", "Chemistry", "Mathematics"],
            "NEET": ["Physics", "Chemistry", "Biology"],
            "GATE": ["Computer Science", "Electronics", "Mechanical Engineering"],
            "CET": ["Physics", "Chemistry", "Mathematics", "Biology"]
        }
        
        # Generate some random questions based on exam type
        questions = []
        num_questions = random.randint(5, 15)  # Random number of questions
        
        for i in range(num_questions):
            subject = random.choice(subjects.get(exam, ["General"]))
            
            # Create different question types based on exam
            if exam == "JEE":
                if subject == "Physics":
                    question = {
                        'question_text': f"A particle moves in a circle of radius 20 cm with constant speed and time period 2π seconds. What is the magnitude of the velocity of the particle?",
                        'subject': subject,
                        'options': {
                            'A': '10 cm/s',
                            'B': '20 cm/s',
                            'C': '40 cm/s',
                            'D': '80 cm/s'
                        },
                        'answer': 'B',
                        'explanation': 'The velocity v = 2πr/T, where r is the radius and T is the time period. Substituting r = 20 cm and T = 2π seconds, we get v = 2π × 20 / 2π = 20 cm/s.'
                    }
                elif subject == "Chemistry":
                    question = {
                        'question_text': f"Which of the following has the highest electron affinity?",
                        'subject': subject,
                        'options': {
                            'A': 'F',
                            'B': 'Cl',
                            'C': 'Br',
                            'D': 'I'
                        },
                        'answer': 'B',
                        'explanation': 'Chlorine (Cl) has the highest electron affinity among the halogens. While fluorine has smaller atomic size, its high electron density causes significant electron-electron repulsion, reducing its electron affinity compared to chlorine.'
                    }
                else:  # Mathematics
                    question = {
                        'question_text': f"If f(x) = x³ - 3x² + 4x - 2, then f'(2) equals:",
                        'subject': subject,
                        'options': {
                            'A': '2',
                            'B': '4',
                            'C': '6',
                            'D': '8'
                        },
                        'answer': 'C',
                        'explanation': "f'(x) = 3x² - 6x + 4, so f'(2) = 3(2)² - 6(2) + 4 = 12 - 12 + 4 = 4"
                    }
            elif exam == "NEET":
                if subject == "Biology":
                    question = {
                        'question_text': f"Which of the following is NOT a part of the human digestive system?",
                        'subject': subject,
                        'options': {
                            'A': 'Pharynx',
                            'B': 'Trachea',
                            'C': 'Esophagus',
                            'D': 'Stomach'
                        },
                        'answer': 'B',
                        'explanation': 'Trachea (windpipe) is a part of the respiratory system, not the digestive system. It carries air from the larynx to the bronchi.'
                    }
                else:
                    question = {
                        'question_text': f"Sample {exam} question {i+1} for {subject} from year {year}",
                        'subject': subject,
                        'options': {
                            'A': 'Option A',
                            'B': 'Option B',
                            'C': 'Option C',
                            'D': 'Option D'
                        },
                        'answer': random.choice(['A', 'B', 'C', 'D']),
                        'explanation': f'This is a sample explanation for the {subject} question.'
                    }
            else:  # GATE or CET
                question = {
                    'question_text': f"Sample {exam} question {i+1} for {subject} from year {year}",
                    'subject': subject,
                    'options': {
                        'A': 'Option A',
                        'B': 'Option B',
                        'C': 'Option C',
                        'D': 'Option D'
                    },
                    'answer': random.choice(['A', 'B', 'C', 'D']),
                    'explanation': f'This is a sample explanation for the {subject} question.'
                }
            
            questions.append(question)
        
        return questions 