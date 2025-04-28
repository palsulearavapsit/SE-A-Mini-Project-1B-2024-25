import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from database import create_connection

class FeedbackPage:
    def __init__(self, root, on_back):
        """
        Initialize the Feedback page.
        
        Args:
            root: The parent Tkinter window/container
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()
        
    def create_widgets(self):
        """
        Create and arrange all GUI widgets for the feedback form.
        Includes customer details, feedback text area, and rating system.
        """
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Page title
        tk.Label(main_frame, text="Customer Feedback", 
                font=("Arial", 24, "bold"), 
                bg="#f2f2f2").pack(pady=20)

        # Form container frame
        form_frame = tk.Frame(main_frame, bg="#f2f2f2")
        form_frame.pack(pady=10)
        
        # Customer details section
        details_frame = tk.LabelFrame(form_frame, 
                                    text="Customer Details", 
                                    bg="#f2f2f2", 
                                    padx=10, pady=10)
        details_frame.pack(fill=tk.X, pady=10)
        
        # Name field
        tk.Label(details_frame, 
                text="Customer Name:", 
                bg="#f2f2f2").grid(row=0, column=0, 
                                 padx=10, pady=5, 
                                 sticky="w")
        self.name_entry = ttk.Entry(details_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Verify button to fetch customer details from database
        ttk.Button(details_frame, 
                 text="Verify", 
                 command=self.verify_customer).grid(row=0, column=2, 
                                                  padx=10, pady=5)

        # Mobile number field
        tk.Label(details_frame, 
                text="Mobile Number:", 
                bg="#f2f2f2").grid(row=1, column=0, 
                                  padx=10, pady=5, 
                                  sticky="w")
        self.mobile_number_entry = ttk.Entry(details_frame, width=30)
        self.mobile_number_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Feedback section
        feedback_frame = tk.LabelFrame(form_frame, 
                                     text="Your Feedback", 
                                     bg="#f2f2f2", 
                                     padx=10, pady=10)
        feedback_frame.pack(fill=tk.X, pady=10)
        
        # Review text area with scrollbar
        tk.Label(feedback_frame, 
                text="Review:", 
                bg="#f2f2f2").grid(row=0, column=0, 
                                  padx=10, pady=5, 
                                  sticky="nw")
        self.review_text = scrolledtext.ScrolledText(feedback_frame, 
                                                    height=5, 
                                                    width=40, 
                                                    wrap=tk.WORD)
        self.review_text.grid(row=0, column=1, padx=10, pady=5)
        
        # Rating section with star display
        rating_frame = tk.Frame(feedback_frame, bg="#f2f2f2")
        rating_frame.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        tk.Label(feedback_frame, 
                text="Rating:", 
                bg="#f2f2f2").grid(row=1, column=0, 
                                  padx=10, pady=5, 
                                  sticky="w")
        # Default to 5-star rating
        self.rating_var = tk.IntVar(value=5)  
        
        # Create 5-star rating radio buttons
        self.stars = []
        for i in range(1, 6):
            star_btn = ttk.Radiobutton(rating_frame, 
                                      text="★", 
                                      value=i, 
                                      variable=self.rating_var)
            star_btn.pack(side=tk.LEFT, padx=2)
            self.stars.append(star_btn)
         
        # Error message display
        self.error_var = tk.StringVar()
        self.error_label = tk.Label(form_frame, 
                                   textvariable=self.error_var, 
                                   fg="red", 
                                   bg="#f2f2f2")
        self.error_label.pack(pady=5)
        
        # Button container
        btn_frame = tk.Frame(main_frame, bg="#f2f2f2")
        btn_frame.pack(pady=15)
        
        # Submit feedback button
        submit_btn = ttk.Button(btn_frame, 
                              text="Submit Feedback", 
                              command=self.submit_feedback)
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        # Back to homepage button
        back_btn = ttk.Button(btn_frame, 
                            text="Back to Homepage", 
                            command=self.on_back)
        back_btn.pack(side=tk.LEFT, padx=10)
        
        # Helpful note for users
        note_label = tk.Label(main_frame, 
                            text="Note: Your feedback helps us improve our services.", 
                            fg="gray", 
                            bg="#f2f2f2", 
                            font=("Arial", 10, "italic"))
        note_label.pack(pady=5)

    def verify_customer(self):
        """
        Verify customer exists in database using mobile number.
        If found, auto-fills the name field.
        """
        mobile_number = self.mobile_number_entry.get().strip()
        
        # Validate mobile number is provided
        if not mobile_number:
            self.error_var.set("Please enter a mobile number")
            return
            
        # Clear previous error messages
        self.error_var.set("")
        
        # Validate mobile number format
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            self.error_var.set("Mobile number should be 10 digits")
            return
            
        # Query database for customer
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT name FROM customers WHERE mobile_number = %s", 
                              (mobile_number,))
                customer = cursor.fetchone()
                
                if customer:
                    # Auto-fill name if customer exists
                    self.name_entry.delete(0, tk.END)
                    self.name_entry.insert(0, customer[0])
                    messagebox.showinfo("Customer Found", 
                                      f"Welcome back, {customer[0]}!")
                else:
                    # Clear name if customer not found
                    self.name_entry.delete(0, tk.END)
                    self.error_var.set("Customer not found. You can still submit feedback.")
            except Exception as e:
                self.error_var.set(f"Error verifying customer: {e}")
            finally:
                cursor.close()
                connection.close()

    def validate_input(self):
        """
        Validate all form inputs before submission.
        
        Returns:
            bool: True if all inputs are valid, False otherwise
        """
        name = self.name_entry.get().strip()
        mobile_number = self.mobile_number_entry.get().strip()
        review = self.review_text.get("1.0", tk.END).strip()
        
        # Clear previous errors
        self.error_var.set("")
        
        # Validate name
        if not name:
            self.error_var.set("Please enter your name")
            self.name_entry.focus_set()
            return False
            
        # Validate mobile number
        if not mobile_number:
            self.error_var.set("Please enter your mobile number")
            self.mobile_number_entry.focus_set()
            return False
            
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            self.error_var.set("Mobile number should be 10 digits")
            self.mobile_number_entry.focus_set()
            return False
            
        # Validate review text
        if not review:
            self.error_var.set("Please enter your review")
            self.review_text.focus_set()
            return False
            
        # Check review length
        if len(review) > 1000:  # Database field limit
            self.error_var.set("Review is too long (maximum 1000 characters)")
            return False
            
        return True

    def submit_feedback(self):
        """Submit validated feedback to the database."""
        # Validate inputs first
        if not self.validate_input():
            return
            
        # Get form values
        name = self.name_entry.get().strip()
        mobile_number = self.mobile_number_entry.get().strip()
        review = self.review_text.get("1.0", tk.END).strip()
        rating = self.rating_var.get()

        # Connect to database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Insert feedback record
                cursor.execute("""
                    INSERT INTO feedback (customer_name, mobile_number, review, rating)
                    VALUES (%s, %s, %s, %s)
                """, (name, mobile_number, review, rating))
                
                # Commit transaction
                connection.commit()
                messagebox.showinfo("Success", "Thank you for your feedback!")
                self.clear_form()
            except Exception as e:
                # Rollback on error
                connection.rollback()
                # Handle specific database constraints
                error_msg = str(e)
                if "CHECK constraint" in error_msg and "rating" in error_msg:
                    self.error_var.set("Rating must be between 1 and 5")
                else:
                    self.error_var.set(f"Failed to submit feedback: {e}")
            finally:
                cursor.close()
                connection.close()
    
    def clear_form(self):
        """Reset all form fields to their default state."""
        self.name_entry.delete(0, tk.END)
        self.mobile_number_entry.delete(0, tk.END)
        self.review_text.delete("1.0", tk.END)
        self.rating_var.set(5)  # Reset to 5-star rating
        self.error_var.set("")  # Clear error messages