import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime

class MockTestResultPage(ctk.CTkFrame):
    def __init__(self, master, app, test_result):
        super().__init__(master)
        self.master = master
        self.app = app
        self.test_result = test_result  # Dictionary containing test result data
        
        # Extract test data
        self.subject = test_result.get('subject', 'Unknown')
        self.total_marks = test_result.get('total_marks', 0)
        self.max_marks = test_result.get('max_marks', 0)
        self.score_percentage = test_result.get('score_percentage', 0)
        self.correct_answers = test_result.get('correct_answers', 0)
        self.incorrect_answers = test_result.get('incorrect_answers', 0)
        self.not_attempted = test_result.get('not_attempted', 0)
        self.time_spent = test_result.get('time_spent', 0)
        
        # Subject-wise scores
        self.physics_marks = test_result.get('physics_marks', 0)
        self.chemistry_marks = test_result.get('chemistry_marks', 0)
        self.mathematics_marks = test_result.get('mathematics_marks', 0)
        
        self.physics_percentage = test_result.get('physics_percentage', 0)
        self.chemistry_percentage = test_result.get('chemistry_percentage', 0)
        self.mathematics_percentage = test_result.get('mathematics_percentage', 0)
        
        # Save test result to database
        self.save_test_result()
        
        # Setup the UI
        self.setup_ui()
        
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Set dark background
        self.configure(fg_color="#1a1a1a")
        
        # Create main container with two columns
        container = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        container.pack(fill="both", expand=True)
        
        # Create a grid layout with a fixed sidebar width
        container.grid_columnconfigure(0, minsize=350, weight=0)  # Fixed width sidebar
        container.grid_columnconfigure(1, weight=1)  # Content area takes remaining space
        container.grid_rowconfigure(0, weight=1)
        
        # Create sidebar with accent color
        sidebar = ctk.CTkFrame(container, corner_radius=0, fg_color="#2ecc71")
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Sidebar title
        sidebar_title = ctk.CTkLabel(sidebar, text="Test Results", 
                                    font=("Arial", 36, "bold"), 
                                    text_color="white")
        sidebar_title.pack(pady=(70, 10), padx=20)
        
        # Sidebar tagline
        sidebar_tagline = ctk.CTkLabel(sidebar, text="Your Performance Report", 
                                      font=("Arial", 20), 
                                      text_color="white")
        sidebar_tagline.pack(pady=(0, 50), padx=20)
        
        # Sidebar features with icons
        features = [
            ("📊 Detailed Score Analysis", 20),
            ("📈 Subject-wise Breakdown", 20),
            ("🎯 Strengths & Weaknesses", 20),
            ("⏱️ Time Management Stats", 20),
            ("📝 Answer Review", 20),
            ("🔍 Recommended Focus Areas", 20)
        ]
        
        for feature_text, padding in features:
            feature = ctk.CTkLabel(sidebar, text=feature_text, 
                                  font=("Arial", 18), 
                                  text_color="white",
                                  anchor="w")
            feature.pack(pady=padding, padx=40, fill="x")
        
        # Create main content area with scrolling
        content_frame = ctk.CTkFrame(container, corner_radius=0, fg_color="#1e1e1e")
        content_frame.grid(row=0, column=1, sticky="nsew")
        
        # Scrollable container for results
        scrollable_container = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="transparent",
            scrollbar_button_color="#3a3a3a",
            scrollbar_button_hover_color="#505050"
        )
        scrollable_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Back button
        back_btn = ctk.CTkButton(scrollable_container, text="← Back to Dashboard", 
                               command=self.app.show_dashboard_page,
                               width=180,
                               height=36,
                               fg_color="#333333",
                               hover_color="#444444",
                               corner_radius=8)
        back_btn.pack(anchor="w", pady=(0, 30))
        
        # Main heading with test type
        test_type = self.subject.split(',')[0] if ',' in self.subject else self.subject
        main_heading = ctk.CTkLabel(scrollable_container, text=f"{test_type} Test Results", 
                                  font=("Arial", 28, "bold"),
                                  text_color="white")
        main_heading.pack(pady=(0, 30))
        
        # Overall score section (accent color based on score)
        if self.score_percentage >= 80:
            accent_color = "#4CAF50"  # Green for excellent
            score_text = "Excellent!"
        elif self.score_percentage >= 60:
            accent_color = "#2196F3"  # Blue for good
            score_text = "Good Job!"
        elif self.score_percentage >= 40:
            accent_color = "#FF9800"  # Orange for average
            score_text = "Keep Practicing!"
        else:
            accent_color = "#F44336"  # Red for needs improvement
            score_text = "Needs Improvement"
        
        score_frame = ctk.CTkFrame(scrollable_container, fg_color="#252525", corner_radius=15)
        score_frame.pack(fill="x", pady=(0, 30), ipady=20)
        
        score_title = ctk.CTkLabel(score_frame, text="Overall Score", 
                                 font=("Arial", 18),
                                 text_color="#BBBBBB")
        score_title.pack(pady=(20, 10))
        
        score_percentage = ctk.CTkLabel(score_frame, text=f"{self.score_percentage:.1f}%", 
                                      font=("Arial", 48, "bold"),
                                      text_color=accent_color)
        score_percentage.pack(pady=(0, 10))
        
        score_evaluation = ctk.CTkLabel(score_frame, text=score_text, 
                                      font=("Arial", 22, "bold"),
                                      text_color=accent_color)
        score_evaluation.pack(pady=(0, 10))
        
        score_details = ctk.CTkLabel(score_frame, text=f"Total Marks: {self.total_marks} / {self.max_marks}", 
                                   font=("Arial", 16),
                                   text_color="#BBBBBB")
        score_details.pack(pady=(0, 20))
        
        # Create a button to show results in reports page
        view_reports_btn = ctk.CTkButton(score_frame, text="View in Reports Dashboard", 
                                       command=self.app.show_reports,
                                       width=220,
                                       height=36,
                                       fg_color=accent_color,
                                       hover_color="#505050",
                                       corner_radius=8)
        view_reports_btn.pack(pady=(0, 20))
        
        # Response breakdown section
        responses_frame = ctk.CTkFrame(scrollable_container, fg_color="#252525", corner_radius=15)
        responses_frame.pack(fill="x", pady=(0, 30), ipady=20)
        
        responses_title = ctk.CTkLabel(responses_frame, text="Response Breakdown", 
                                     font=("Arial", 18),
                                     text_color="#BBBBBB")
        responses_title.pack(pady=(20, 30))
        
        # Create a frame for the charts
        chart_frame = ctk.CTkFrame(responses_frame, fg_color="transparent")
        chart_frame.pack(fill="both", padx=30, pady=(0, 30))
        
        # Create the response breakdown chart
        self.create_response_chart(chart_frame)
        
        # Statistics section
        stats_frame = ctk.CTkFrame(scrollable_container, fg_color="#252525", corner_radius=15)
        stats_frame.pack(fill="x", pady=(0, 30), ipady=20)
        
        stats_title = ctk.CTkLabel(stats_frame, text="Test Statistics", 
                                 font=("Arial", 18),
                                 text_color="#BBBBBB")
        stats_title.pack(pady=(20, 30))
        
        # Stats in a grid - 2 columns
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=40, pady=(0, 30))
        
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        
        # Convert seconds to HH:MM:SS
        hours = self.time_spent // 3600
        minutes = (self.time_spent % 3600) // 60
        seconds = self.time_spent % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Stats data
        stats_data = [
            ("Questions Attempted", f"{self.correct_answers + self.incorrect_answers} of {self.correct_answers + self.incorrect_answers + self.not_attempted}"),
            ("Time Taken", time_str),
            ("Correct Answers", f"{self.correct_answers}"),
            ("Avg. Time per Question", f"{self.time_spent // (self.correct_answers + self.incorrect_answers) if (self.correct_answers + self.incorrect_answers) > 0 else 0} seconds"),
            ("Incorrect Answers", f"{self.incorrect_answers}"),
            ("Accuracy", f"{(self.correct_answers / (self.correct_answers + self.incorrect_answers) * 100) if (self.correct_answers + self.incorrect_answers) > 0 else 0:.1f}%")
        ]
        
        # Add stat rows
        for i, (label, value) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            stat_container = ctk.CTkFrame(stats_grid, fg_color="transparent")
            stat_container.grid(row=row, column=col, padx=10, pady=10, sticky="w")
            
            stat_label = ctk.CTkLabel(stat_container, text=label, 
                                    font=("Arial", 14),
                                    text_color="#AAAAAA")
            stat_label.pack(anchor="w")
            
            stat_value = ctk.CTkLabel(stat_container, text=value, 
                                    font=("Arial", 16, "bold"),
                                    text_color="#FFFFFF")
            stat_value.pack(anchor="w", pady=(5, 0))
        
        # Subject-wise performance section
        if ',' in self.subject:  # Only show for multi-subject tests
            subject_frame = ctk.CTkFrame(scrollable_container, fg_color="#252525", corner_radius=15)
            subject_frame.pack(fill="x", pady=(0, 30), ipady=20)
            
            subject_title = ctk.CTkLabel(subject_frame, text="Subject-wise Performance", 
                                      font=("Arial", 18),
                                      text_color="#BBBBBB")
            subject_title.pack(pady=(20, 30))
            
            # Create subject chart
            subject_chart_frame = ctk.CTkFrame(subject_frame, fg_color="transparent")
            subject_chart_frame.pack(fill="x", padx=40, pady=(0, 30))
            
            self.create_subject_chart(subject_chart_frame)
        
        # Next steps section
        nextsteps_frame = ctk.CTkFrame(scrollable_container, fg_color="#252525", corner_radius=15)
        nextsteps_frame.pack(fill="x", pady=(0, 30), ipady=20)
        
        nextsteps_title = ctk.CTkLabel(nextsteps_frame, text="Next Steps", 
                                     font=("Arial", 18),
                                     text_color="#BBBBBB")
        nextsteps_title.pack(pady=(20, 20))
        
        # Buttons for next actions
        buttons_frame = ctk.CTkFrame(nextsteps_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        # Two columns for buttons
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # Take another test
        retry_btn = ctk.CTkButton(buttons_frame, text="Take Another Test", 
                                command=self.app.show_mock_tests,
                                width=200,
                                height=45,
                                fg_color="#2ecc71",
                                hover_color="#27ae60",
                                corner_radius=8,
                                font=("Arial", 14, "bold"))
        retry_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # View detailed analysis
        analysis_btn = ctk.CTkButton(buttons_frame, text="View Detailed Analysis", 
                                   command=self.app.show_reports,
                                   width=200,
                                   height=45,
                                   fg_color="#3498db",
                                   hover_color="#2980b9",
                                   corner_radius=8,
                                   font=("Arial", 14, "bold"))
        analysis_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Study resources
        resources_btn = ctk.CTkButton(buttons_frame, text="Study Resources", 
                                    command=lambda: self.app.show_dashboard_page(),  # Replace with study resources page
                                    width=200,
                                    height=45,
                                    fg_color="#9b59b6",
                                    hover_color="#8e44ad",
                                    corner_radius=8,
                                    font=("Arial", 14, "bold"))
        resources_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # Return to dashboard
        dashboard_btn = ctk.CTkButton(buttons_frame, text="Return to Dashboard", 
                                    command=self.app.show_dashboard_page,
                                    width=200,
                                    height=45,
                                    fg_color="#e74c3c",
                                    hover_color="#c0392b",
                                    corner_radius=8,
                                    font=("Arial", 14, "bold"))
        dashboard_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # After displaying the results, refresh the dashboard stats
        self.refresh_dashboard_stats()
    
    def create_response_chart(self, parent):
        """Create a pie chart showing response breakdown"""
        # Create a figure for the pie chart
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Data for the pie chart
        labels = ['Correct', 'Incorrect', 'Not Attempted']
        sizes = [self.correct_answers, self.incorrect_answers, self.not_attempted]
        colors = ['#4CAF50', '#F44336', '#9E9E9E']
        explode = (0.1, 0, 0)  # explode the 1st slice (Correct)
        
        # Create the pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            explode=explode, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True
        )
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        plt.tight_layout()
        
        # Set font color to white for better visibility
        for text in texts:
            text.set_color('white')
        
        for autotext in autotexts:
            autotext.set_color('white')
        
        # Set background color to match the app theme
        fig.patch.set_facecolor('#252525')
        ax.set_facecolor('#252525')
        
        # Create a canvas to display the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_subject_chart(self, parent):
        """Create a bar chart showing subject-wise performance"""
        # Create a figure for the chart
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Data for the chart
        subjects = ['Physics', 'Chemistry', 'Mathematics']
        percentages = [self.physics_percentage, self.chemistry_percentage, self.mathematics_percentage]
        colors = ['#2196F3', '#FF9800', '#9C27B0']  # Different color for each subject
        
        # Create horizontal bars
        bars = ax.barh(subjects, percentages, color=colors)
        
        # Add percentage labels on the bars
        for bar in bars:
            width = bar.get_width()
            label_x_pos = width + 1
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.1f}%',
                   va='center', color='white')
        
        # Set chart title and labels
        ax.set_title('Subject-wise Score Percentage', color='white')
        ax.set_xlabel('Score Percentage (%)', color='white')
        
        # Set x-axis limit
        ax.set_xlim(0, 100)
        
        # Set tick colors to white
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Set background colors
        fig.patch.set_facecolor('#252525')
        ax.set_facecolor('#252525')
        
        # Create a canvas to display the chart
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def save_test_result(self):
        """Save test result to the database"""
        try:
            # Check if we have database manager access
            if hasattr(self.app, 'db_manager'):
                # Get current timestamp
                now = datetime.now()
                
                # Create a tuple with test details in the correct order
                query = """
                    INSERT INTO user_progress (
                        user_id, subject, score, total_marks, max_marks, 
                        correct_answers, incorrect_answers, not_attempted, 
                        time_spent, physics_marks, chemistry_marks, mathematics_marks,
                        physics_percentage, chemistry_percentage, mathematics_percentage,
                        completed, date_taken
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                
                # Create parameter tuple in the same order as the query
                params = (
                    self.app.current_user_id,
                    self.subject,
                    self.score_percentage,
                    self.total_marks,
                    self.max_marks,
                    self.correct_answers,
                    self.incorrect_answers,
                    self.not_attempted,
                    self.time_spent,
                    self.physics_marks,
                    self.chemistry_marks,
                    self.mathematics_marks,
                    self.physics_percentage,
                    self.chemistry_percentage,
                    self.mathematics_percentage,
                    1,  # completed
                    now
                )
                
                # Execute query
                success = self.app.db_manager.execute_query(query, params)
                
                if success:
                    print(f"Test result saved successfully: {self.score_percentage:.1f}%")
                else:
                    print("Failed to save test result, trying basic fields")
                    
                    # Fallback to basic fields if there was an error
                    try:
                        basic_query = """
                            INSERT INTO user_progress (
                                user_id, subject, score, completed, date_taken
                            ) VALUES (
                                %s, %s, %s, %s, %s
                            )
                        """
                        basic_params = (
                            self.app.current_user_id,
                            self.subject,
                            self.score_percentage,
                            1,  # completed
                            now
                        )
                        success = self.app.db_manager.execute_query(basic_query, basic_params)
                        
                        if success:
                            print(f"Test result saved with basic fields: {self.score_percentage:.1f}%")
                        else:
                            print("Failed to save test result with basic fields")
                    except Exception as basic_error:
                        print(f"Error saving test result with basic fields: {basic_error}")
            else:
                print("Database manager not available, test result not saved")
                
        except Exception as err:
            print(f"Error saving test result: {err}")
    
    def refresh_dashboard_stats(self):
        """Refresh the dashboard stats after completing a test"""
        # Check if dashboard exists and app property exists and also check that the widgets are still valid
        try:
            if (hasattr(self, 'app') and 
                hasattr(self.app, 'dashboard_page') and 
                self.app.dashboard_page and 
                hasattr(self.app.dashboard_page, 'winfo_exists') and
                self.app.dashboard_page.winfo_exists()):
                    
                # First ensure test result is saved before refreshing stats
                if not hasattr(self, '_result_saved') or not self._result_saved:
                    self.save_test_result()
                    self._result_saved = True
                    
                # Add a small delay to allow database to update
                self.after(500, self._delayed_refresh_stats)
                    
                print("Dashboard stats refresh scheduled")
            else:
                print("Dashboard not available for refresh")
        except Exception as e:
            print(f"Error scheduling dashboard stats refresh: {e}")
            
    def _delayed_refresh_stats(self):
        """Refresh stats after a short delay to ensure database is updated"""
        try:
            if (hasattr(self, 'app') and 
                hasattr(self.app, 'dashboard_page') and
                self.app.dashboard_page and
                hasattr(self.app.dashboard_page, 'winfo_exists') and
                self.app.dashboard_page.winfo_exists()):
                
                # Call the load_user_stats method to refresh the stats
                self.app.dashboard_page.load_user_stats()
                print("Dashboard stats refreshed successfully")
        except Exception as e:
            print(f"Error refreshing dashboard stats: {e}")
            # This is not critical, so just log the error and continue 