import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class ReportsPage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
            
        # Set dark background
        self.configure(fg_color="#1a1a1a")
        
        # Header frame
        header_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        # Back button
        back_btn = ctk.CTkButton(
            header_frame, 
            text="← Back",
            command=self.app.show_dashboard_page,
            width=80,
            height=32,
            fg_color="#333333",
            hover_color="#444444",
            corner_radius=8
        )
        back_btn.pack(side="left", padx=20, pady=20)
        
        # Page title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Test Analysis Reports",
            font=("Arial", 24, "bold")
        )
        title_label.pack(side="left", padx=20, pady=20)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="↻ Refresh",
            command=self.refresh_data,
            width=100,
            height=32,
            fg_color="#3498db",
            hover_color="#2980b9",
            corner_radius=8
        )
        refresh_btn.pack(side="right", padx=20, pady=20)
        
        # Main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title for analysis
        analysis_title = ctk.CTkLabel(
            content_frame,
            text="COMPLETE ANALYSIS REPORT OF YOUR TESTS",
            font=("Arial", 18, "bold"),
            text_color="#ffffff"
        )
        analysis_title.pack(pady=(0, 20))
        
        # Tab-like navigation
        tabs_frame = ctk.CTkFrame(content_frame, fg_color="#1e1e1e")
        tabs_frame.pack(fill="x", pady=(0, 20))
        
        # Overall Performance tab (active)
        overall_btn = ctk.CTkButton(
                tabs_frame,
            text="Overall Performance",
            font=("Arial", 14),
            fg_color="#8a2be2",  # Purple active tab color
            hover_color="#8a2be2",
                corner_radius=0,
            height=40,
            command=lambda: None  # No command needed
        )
        overall_btn.pack(fill="x", expand=True)
        
        # Main content area (white background)
        main_area = ctk.CTkFrame(content_frame, fg_color="#ffffff", corner_radius=10)
        main_area.pack(fill="both", expand=True)
        
        # Debug print to check database connection
        print("Checking database connection:")
        print(f"Has conn attribute: {hasattr(self.app, 'conn')}")
        print(f"Has current_user_id attribute: {hasattr(self.app, 'current_user_id')}")
        if hasattr(self.app, 'current_user_id'):
            print(f"Current user ID: {self.app.current_user_id}")
        
        # Load user progress data - with debug prints
        progress_data = self.load_user_progress()
        print(f"Loaded progress data: {len(progress_data)} records")
        if progress_data:
            print(f"First record: {progress_data[0]}")
        
        # Check if we have any data
        if not progress_data or len(progress_data) == 0:
            no_data_label = ctk.CTkLabel(
                main_area,
                text="No test data available yet. Complete some tests to see your performance analysis.",
                font=("Arial", 16),
                text_color="#333333"
            )
            no_data_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Add a button to take a test
            take_test_btn = ctk.CTkButton(
                main_area,
                text="Take a Test Now",
                font=("Arial", 14),
                fg_color="#8a2be2",
                hover_color="#7025c5",
                height=40,
                command=self.app.show_mock_tests
            )
            take_test_btn.place(relx=0.5, rely=0.6, anchor="center")
            return
        
        # Create scrollable container for all content
        scroll_container = ctk.CTkScrollableFrame(main_area, fg_color="transparent")
        scroll_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Summary section
        summary_frame = ctk.CTkFrame(scroll_container, fg_color="#f8f9fa", corner_radius=10)
        summary_frame.pack(fill="x", pady=(0, 20))
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Performance Summary",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        )
        summary_title.pack(pady=(15, 20))
        
        # Summary stats in a grid
        stats_grid = ctk.CTkFrame(summary_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Calculate summary statistics
        total_tests = len(progress_data)
        avg_score = sum([test.get('score', 0) for test in progress_data]) / total_tests if total_tests > 0 else 0
        best_score = max([test.get('score', 0) for test in progress_data]) if progress_data else 0
        
        # For total marks, handle None values
        total_marks = 0
        for test in progress_data:
            marks = test.get('total_marks')
            if marks is not None:
                total_marks += marks
            
        max_possible = 360 * total_tests  # Assuming 360 is max possible per test
        
        # Configure grid columns
        stats_grid.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Stats boxes
        self.create_stat_box(stats_grid, "Tests Taken", str(total_tests), 0, "#e3f2fd", "#1976d2")
        self.create_stat_box(stats_grid, "Average Score", f"{avg_score:.1f}%", 1, "#fff8e1", "#ff9800")
        self.create_stat_box(stats_grid, "Best Score", f"{best_score:.1f}%", 2, "#e8f5e9", "#4caf50")
        self.create_stat_box(stats_grid, "Total Marks", f"{total_marks}/{max_possible}", 3, "#f3e5f5", "#9c27b0")
        
        # Progress chart section
        chart_frame = ctk.CTkFrame(scroll_container, fg_color="#f8f9fa", corner_radius=10)
        chart_frame.pack(fill="x", pady=(0, 20))
        
        chart_title = ctk.CTkLabel(
            chart_frame,
            text="Score Progression",
            font=("Arial", 18, "bold"),
            text_color="#333333"
        )
        chart_title.pack(pady=(15, 5))
        
        # Create chart showing test scores over time
        self.create_score_chart(chart_frame, progress_data)
        
        # Individual test reports
        reports_frame = ctk.CTkFrame(scroll_container, fg_color="#f8f9fa", corner_radius=10)
        reports_frame.pack(fill="x", pady=(0, 20))
        
        reports_title = ctk.CTkLabel(
            reports_frame,
            text="Individual Test Reports",
                font=("Arial", 18, "bold"),
            text_color="#333333"
        )
        reports_title.pack(pady=(15, 20))
        
        # Create table header
        table_header = ctk.CTkFrame(reports_frame, fg_color="#f1f1f1", corner_radius=0)
        table_header.pack(fill="x", padx=20, pady=(0, 10))
        
        # Configure columns for the table
        col_widths = [50, 150, 100, 100, 100, 100, 150]
        for i, width in enumerate(col_widths):
            table_header.columnconfigure(i, weight=0, minsize=width)
        
        # Table headers
        headers = ["#", "Date", "Score", "Physics", "Chemistry", "Math", "Total Marks"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                table_header,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#555555"
            )
            header_label.grid(row=0, column=i, padx=5, pady=10, sticky="w")
        
        # Test rows container
        rows_container = ctk.CTkFrame(reports_frame, fg_color="transparent")
        rows_container.pack(fill="x", padx=20, pady=(0, 20))
        
        # Add rows for each test
        for i, test in enumerate(reversed(progress_data)):  # Show most recent tests first
            row_bg = "#ffffff" if i % 2 == 0 else "#f9f9f9"
            self.create_test_row(rows_container, i + 1, test, row_bg, col_widths)
        
        # Subject distribution chart
        if len(progress_data) > 0:
            subject_frame = ctk.CTkFrame(scroll_container, fg_color="#f8f9fa", corner_radius=10)
            subject_frame.pack(fill="x", pady=(0, 20))
            
            subject_title = ctk.CTkLabel(
                subject_frame,
                text="Subject Performance",
                font=("Arial", 18, "bold"),
                text_color="#333333"
            )
            subject_title.pack(pady=(15, 5))
            
            # Create chart showing performance by subject
            self.create_subject_chart(subject_frame, progress_data)

    def create_stat_box(self, parent, title, value, col, bg_color, accent_color):
        """Create a statistics box"""
        box = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=8)
        box.grid(row=0, column=col, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)
        
        title_label = ctk.CTkLabel(
            box,
            text=title,
            font=("Arial", 14),
            text_color="#555555"
        )
        title_label.pack(pady=(10, 5))
        
        value_label = ctk.CTkLabel(
            box,
            text=value,
            font=("Arial", 24, "bold"),
            text_color=accent_color
        )
        value_label.pack(pady=(0, 10))
        
        return box
    
    def create_test_row(self, parent, index, test, bg_color, col_widths):
        """Create a row for an individual test"""
        row = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=0, height=40)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)
        
        # Configure columns
        for i, width in enumerate(col_widths):
            row.columnconfigure(i, weight=0, minsize=width)
        
        # Format date from timestamp or date_taken if available
        try:
            date_str = "N/A"
            if 'date_taken' in test and test['date_taken']:
                # Handle datetime object or string format
                if isinstance(test['date_taken'], datetime):
                    date_str = test['date_taken'].strftime('%Y-%m-%d %H:%M')
                else:
                    try:
                        test_date = datetime.strptime(str(test['date_taken']), '%Y-%m-%d %H:%M:%S')
                        date_str = test_date.strftime('%Y-%m-%d %H:%M')
                    except ValueError:
                        date_str = str(test['date_taken'])
            elif 'timestamp' in test and test['timestamp']:
                if isinstance(test['timestamp'], str):
                    try:
                        test_date = datetime.strptime(test['timestamp'], '%Y-%m-%d %H:%M:%S')
                        date_str = test_date.strftime('%Y-%m-%d %H:%M')
                    except ValueError:
                        date_str = test['timestamp']
                else:
                    date_str = str(test['timestamp'])
        except Exception as e:
            print(f"Error formatting date: {e}")
            date_str = "N/A"
        
        # Safe value access with defaults
        def safe_get(dict_obj, key, default=0):
            value = dict_obj.get(key)
            if value is None:
                return default
            return value
        
        # Row data
        data = [
            f"{index}",
            date_str,
            f"{safe_get(test, 'score'):.1f}%",
            f"{safe_get(test, 'physics_score'):.1f}%",
            f"{safe_get(test, 'chemistry_score'):.1f}%",
            f"{safe_get(test, 'mathematics_score'):.1f}%",
            f"{safe_get(test, 'total_marks')}/{safe_get(test, 'max_marks', 360)}"  # Use max_marks if available
        ]
        
        # Create labels for each cell
        for i, text in enumerate(data):
            cell = ctk.CTkLabel(
                row,
                text=text,
                font=("Arial", 12),
                text_color="#333333"
            )
            cell.grid(row=0, column=i, padx=5, pady=0, sticky="w")
        
        # Add a button to view details and add notes
        notes_button = ctk.CTkButton(
            row,
            text="Notes",
            width=60,
            height=24,
            fg_color="#8a2be2",
            hover_color="#7025c5",
            font=("Arial", 10),
            command=lambda t=test: self.show_notes_dialog(t)
        )
        notes_button.grid(row=0, column=len(data), padx=5, sticky="e")
        
        return row
    
    def show_notes_dialog(self, test):
        """Show dialog to view and add notes for a test"""
        # Create a toplevel window for the notes
        dialog = ctk.CTkToplevel(self)
        dialog.title("Test Notes")
        dialog.geometry("600x500")
        dialog.grab_set()  # Make the dialog modal
        
        # Configure the dialog
        dialog.configure(fg_color="#1e1e1e")
        
        # Add header
        header_frame = ctk.CTkFrame(dialog, fg_color="#252525", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"Notes for {test.get('subject', 'Test')} ({test.get('score', 0):.1f}%)",
            font=("Arial", 18, "bold"),
            text_color="white"
        )
        title_label.pack(pady=20)
        
        # Content frame
        content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Existing notes section
        notes_label = ctk.CTkLabel(
            content_frame,
            text="Your Notes:",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        notes_label.pack(anchor="w", pady=(0, 10))
        
        # Create scrollable frame for notes
        notes_container = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="#252525",
            corner_radius=10,
            height=200
        )
        notes_container.pack(fill="x", pady=(0, 20))
        
        # Load existing notes
        notes = []
        if hasattr(self.app, 'db_manager') and self.app.current_user_id and 'id' in test:
            try:
                notes = self.app.db_manager.get_progress_notes(self.app.current_user_id, test['id'])
            except Exception as e:
                print(f"Error loading notes: {e}")
        
        # Display existing notes
        if notes:
            for note in notes:
                note_frame = ctk.CTkFrame(notes_container, fg_color="#333333", corner_radius=8)
                note_frame.pack(fill="x", pady=5, padx=5, ipady=5)
                
                # Format the datetime
                created_at = note.get('created_at')
                if created_at:
                    if isinstance(created_at, datetime):
                        date_str = created_at.strftime('%Y-%m-%d %H:%M')
                    else:
                        try:
                            date_obj = datetime.strptime(str(created_at), '%Y-%m-%d %H:%M:%S')
                            date_str = date_obj.strftime('%Y-%m-%d %H:%M')
                        except ValueError:
                            date_str = str(created_at)
                else:
                    date_str = "Unknown date"
                
                # Note header with date
                date_label = ctk.CTkLabel(
                    note_frame,
                    text=date_str,
                    font=("Arial", 10),
                    text_color="#aaaaaa"
                )
                date_label.pack(anchor="w", padx=10, pady=(5, 0))
                
                # Note text
                note_text = note.get('note_text', 'No text')
                text_label = ctk.CTkLabel(
                    note_frame,
                    text=note_text,
                    font=("Arial", 12),
                    text_color="white",
                    wraplength=500,
                    justify="left"
                )
                text_label.pack(anchor="w", padx=10, pady=(5, 5))
                
                # If there's a highlight color, show it
                if note.get('highlight_color'):
                    highlight = ctk.CTkFrame(
                        note_frame,
                        fg_color=note.get('highlight_color'),
                        height=5,
                        corner_radius=2
                    )
                    highlight.pack(fill="x", padx=10, pady=(0, 5))
        else:
            no_notes_label = ctk.CTkLabel(
                notes_container,
                text="No notes yet. Add your first note below.",
                font=("Arial", 12),
                text_color="#aaaaaa"
            )
            no_notes_label.pack(pady=20)
        
        # Add note section
        add_note_label = ctk.CTkLabel(
            content_frame,
            text="Add a New Note:",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        add_note_label.pack(anchor="w", pady=(0, 10))
        
        # Note text entry
        note_entry = ctk.CTkTextbox(
            content_frame,
            height=100,
            fg_color="#252525",
            text_color="white",
            border_width=1,
            border_color="#444444"
        )
        note_entry.pack(fill="x", pady=(0, 10))
        
        # Color selection frame
        color_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        color_frame.pack(fill="x", pady=(0, 10))
        
        # Color label
        color_label = ctk.CTkLabel(
            color_frame,
            text="Highlight Color:",
            font=("Arial", 12),
            text_color="white"
        )
        color_label.pack(side="left", padx=(0, 10))
        
        # Selected color variable
        selected_color = ctk.StringVar(value="#8a2be2")  # Default purple
        
        # Color options
        colors = [
            ("#8a2be2", "Purple"),
            ("#2196F3", "Blue"),
            ("#4CAF50", "Green"),
            ("#FFC107", "Yellow"),
            ("#FF5722", "Orange"),
            ("#E91E63", "Pink"),
            (None, "None")
        ]
        
        # Create color buttons
        for color_value, color_name in colors:
            if color_value:
                # Color swatch button
                color_btn = ctk.CTkButton(
                    color_frame,
                    text="",
                    width=24,
                    height=24,
                    fg_color=color_value,
                    hover_color=color_value,
                    command=lambda cv=color_value: selected_color.set(cv)
                )
                color_btn.pack(side="left", padx=5)
            else:
                # "None" text button
                none_btn = ctk.CTkButton(
                    color_frame,
                    text="None",
                    width=50,
                    height=24,
                    fg_color="#333333",
                    hover_color="#444444",
                    command=lambda: selected_color.set(None)
                )
                none_btn.pack(side="left", padx=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Function to save the note
        def save_note():
            note_text = note_entry.get("0.0", "end").strip()
            if not note_text:
                messagebox.showwarning("Empty Note", "Please enter some text for your note.")
                return
                
            if hasattr(self.app, 'db_manager') and self.app.current_user_id and 'id' in test:
                try:
                    # Save the note to the database
                    success = self.app.db_manager.save_progress_note(
                        self.app.current_user_id,
                        test['id'],
                        note_text,
                        selected_color.get()
                    )
                    
                    if success:
                        messagebox.showinfo("Success", "Note saved successfully!")
                        # Close the dialog
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Failed to save note. Please try again.")
                except Exception as e:
                    print(f"Error saving note: {e}")
                    messagebox.showerror("Error", f"Failed to save note: {e}")
            else:
                messagebox.showerror("Error", "Database connection not available or test information missing.")
        
        # Save button
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Note",
            width=120,
            height=32,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            command=save_note
        )
        save_btn.pack(side="right", padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=100,
            height=32,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=5)
    
    def create_score_chart(self, parent, progress_data):
        """Create a line chart showing score progression"""
        # Sort data by date_taken or timestamp if available
        try:
            # Try different sorting approaches based on data
            if any('date_taken' in test for test in progress_data):
                def get_date(test):
                    if not test.get('date_taken'):
                        return datetime.min
                    
                    if isinstance(test['date_taken'], datetime):
                        return test['date_taken']
                    
                    try:
                        return datetime.strptime(str(test['date_taken']), '%Y-%m-%d %H:%M:%S')
                    except:
                        return datetime.min
                
                sorted_data = sorted(progress_data, key=get_date)
            elif any('timestamp' in test for test in progress_data):
                sorted_data = sorted(progress_data, key=lambda x: x.get('timestamp', ''))
            else:
                # Fall back to original order if timestamps are missing
                sorted_data = progress_data
        except Exception as e:
            print(f"Error sorting data: {e}")
            sorted_data = progress_data
        
        # Extract scores and labels
        scores = [test.get('score', 0) for test in sorted_data]
        test_nums = list(range(1, len(scores) + 1))
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
        plt.style.use('ggplot')
        
        # Plot line chart
        if len(scores) > 0:
            line = ax.plot(test_nums, scores, marker='o', linestyle='-', linewidth=2, color='#8a2be2')
            
            # Add data points and values
            for i, score in enumerate(scores):
                ax.annotate(f"{score:.1f}%", 
                           (test_nums[i], scores[i]),
                           textcoords="offset points", 
                           xytext=(0, 10),
                           ha='center',
                           fontsize=9,
                           color='#333333')
            
            # Add area under the curve with gradient fill
            ax.fill_between(test_nums, scores, alpha=0.2, color='#8a2be2')
        else:
            # Handle empty data case
            ax.text(0.5, 0.5, "No score data available", 
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes,
                    fontsize=14,
                    color='#999999')
        
        # Customize chart
        ax.set_title("Score Progression Over Time", fontsize=14, pad=20)
        ax.set_xlabel("Test Number", fontsize=12)
        ax.set_ylabel("Score (%)", fontsize=12)
        ax.set_ylim(0, max(100, max(scores) * 1.1 if scores else 100))
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Set x-ticks to match test numbers
        if test_nums:
            ax.set_xticks(test_nums)
        
        # Customize appearance
        fig.patch.set_facecolor('#f8f9fa')
        ax.patch.set_facecolor('#f8f9fa')
        
        # Embed in tkinter
        chart_container = ctk.CTkFrame(parent, fg_color="transparent")
        chart_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_subject_chart(self, parent, progress_data):
        """Create a bar chart showing average performance by subject"""
        # Calculate average scores for each subject - safely handling None values
        physics_scores = []
        chemistry_scores = []
        math_scores = []
        
        for test in progress_data:
            # First try to use the percentages directly
            physics = test.get('physics_percentage')
            if physics is None:
                physics = test.get('physics_score')
                
            chemistry = test.get('chemistry_percentage')
            if chemistry is None:
                chemistry = test.get('chemistry_score')
                
            math = test.get('mathematics_percentage')
            if math is None:
                math = test.get('mathematics_score')
            
            if physics is not None:
                physics_scores.append(physics)
            if chemistry is not None:
                chemistry_scores.append(chemistry)
            if math is not None:
                math_scores.append(math)
        
        avg_physics = sum(physics_scores) / len(physics_scores) if physics_scores else 0
        avg_chemistry = sum(chemistry_scores) / len(chemistry_scores) if chemistry_scores else 0
        avg_math = sum(math_scores) / len(math_scores) if math_scores else 0
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
        plt.style.use('ggplot')
        
        # Data for bar chart
        subjects = ['Physics', 'Chemistry', 'Mathematics']
        avg_scores = [avg_physics, avg_chemistry, avg_math]
        colors = ['#f44336', '#2196f3', '#4caf50']
        
        # Create bar chart
        bars = ax.bar(subjects, avg_scores, color=colors, width=0.6)
        
        # Add data labels on top of bars
        for bar, score in zip(bars, avg_scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{score:.1f}%',
                   ha='center', va='bottom', fontsize=12)
        
        # Customize chart
        ax.set_title("Average Performance by Subject", fontsize=14, pad=20)
        ax.set_ylabel("Average Score (%)", fontsize=12)
        ax.set_ylim(0, max(100, max(avg_scores) * 1.1 if avg_scores else 100))
        
        # Add horizontal grid lines
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Customize appearance
        fig.patch.set_facecolor('#f8f9fa')
        ax.patch.set_facecolor('#f8f9fa')
        
        # Embed in tkinter
        chart_container = ctk.CTkFrame(parent, fg_color="transparent")
        chart_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        canvas = FigureCanvasTkAgg(fig, master=chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def load_user_progress(self):
        """Load user progress data from database with robust error handling"""
        progress_data = []
        
        try:
            if hasattr(self.app, 'db_manager') and self.app.current_user_id:
                print("Attempting to load user progress from database manager")
                
                # Query to get all test results for current user
                query = """
                    SELECT 
                        id, user_id, subject, score, total_marks, max_marks, 
                        correct_answers, incorrect_answers, not_attempted, 
                        time_spent, physics_marks, chemistry_marks, mathematics_marks,
                        physics_percentage, chemistry_percentage, mathematics_percentage,
                        completed, date_taken
                    FROM user_progress 
                    WHERE user_id = %s AND completed = 1
                    ORDER BY date_taken DESC
                """
                
                # Execute query
                results = self.app.db_manager.execute_read_query(query, (self.app.current_user_id,))
                
                if results:
                    print(f"Query returned {len(results)} test results")
                    
                    # Process each test result
                    for test in results:
                        # Calculate subject scores from percentages for display
                        test['physics_score'] = test.get('physics_percentage', 0)
                        test['chemistry_score'] = test.get('chemistry_percentage', 0)
                        test['mathematics_score'] = test.get('mathematics_percentage', 0)
                        
                        # Set timestamp for sorting
                        if 'date_taken' in test:
                            test['timestamp'] = test['date_taken']
                        
                        progress_data.append(test)
                else:
                    print("No test results found for user")
            else:
                print("Database manager not available or user not logged in")
                
        except Exception as e:
            print(f"Error loading user progress: {e}")
        
        # Return whatever data we found (might be empty)
        print(f"Returning {len(progress_data)} test results")
        return progress_data
        
    def refresh_data(self):
        """Refresh the report data from the database"""
        # Clear the current UI
        for widget in self.winfo_children():
            widget.destroy()
            
        # Rebuild the UI with fresh data
        self.setup_ui()