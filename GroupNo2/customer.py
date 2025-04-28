import tkinter as tk
from tkinter import ttk, messagebox
from database import create_connection

class AddCustomerPage:
    def __init__(self, root, on_back):
        """
        Initialize the Add Customer page.
        
        Args:
            root: The parent Tkinter window/container
            on_back: Callback function to return to homepage
        """
        self.root = root
        self.on_back = on_back
        self.create_widgets()

    def create_widgets(self):
        """
        Create and arrange all GUI widgets for the customer form.
        Includes form fields, validation, and action buttons.
        """
        # Page title
        tk.Label(self.root, 
                text="Add Customer", 
                font=("Arial", 24), 
                bg="#f2f2f2").pack(pady=20)

        # Create a scrollable frame for the form
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Form container frame
        form_frame = tk.Frame(main_frame, bg="#f2f2f2")
        form_frame.pack(pady=10)

        # Define form fields and their corresponding entry widget names
        fields = [
            ("Full Name", "name_entry"),
            ("Father's Name", "father_name_entry"),
            ("Pincode", "pincode_entry"),
            ("Mobile Number", "mobile_number_entry"),
            ("Email Address", "email_entry"),
            ("Nationality", "nationality_entry"),
            ("ID Proof Number", "id_proof_number_entry"),
        ]

        # Dictionary to store all entry widgets
        self.entries = {}
        
        # Create form fields dynamically
        for i, (label_text, entry_name) in enumerate(fields):
            # Create label for each field
            tk.Label(form_frame, 
                    text=label_text, 
                    font=("Arial", 12), 
                    bg="#f2f2f2").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            
            # Create entry widget
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[entry_name] = entry

            # Set default values for specific fields
            if entry_name == "nationality_entry":
                entry.insert(0, "Indian")

        # Gender selection (radio buttons)
        row = len(fields)  # Next available row
        tk.Label(form_frame, 
                text="Gender", 
                font=("Arial", 12), 
                bg="#f2f2f2").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        self.gender_var = tk.StringVar(value="Male")  # Default selection
        gender_frame = tk.Frame(form_frame, bg="#f2f2f2")
        gender_frame.grid(row=row, column=1, sticky="w", pady=5)
        
        # Male and female radio buttons
        ttk.Radiobutton(gender_frame, 
                       text="Male", 
                       variable=self.gender_var, 
                       value="Male").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(gender_frame, 
                       text="Female", 
                       variable=self.gender_var, 
                       value="Female").pack(side=tk.LEFT, padx=10)

        # ID Proof Type selection (combobox)
        row += 1  # Next row
        tk.Label(form_frame, 
                text="ID Proof Type", 
                font=("Arial", 12), 
                bg="#f2f2f2").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        
        self.id_proof_type = tk.StringVar(value="Aadhar")  # Default selection
        id_proof_options = ["Aadhar", "PAN", "License", "Address"]
        
        # Create combobox with proof type options
        ttk.Combobox(form_frame, 
                    textvariable=self.id_proof_type, 
                    values=id_proof_options, 
                    state="readonly", 
                    width=38).grid(row=row, column=1, sticky="w", padx=10, pady=5)

        # Validation message display (initially empty)
        row += 1
        self.validation_message = tk.StringVar()
        validation_label = tk.Label(form_frame, 
                                  textvariable=self.validation_message, 
                                  fg="red", 
                                  bg="#f2f2f2")
        validation_label.grid(row=row, column=0, columnspan=2, pady=5)

        # Action buttons frame
        button_frame = tk.Frame(main_frame, bg="#f2f2f2")
        button_frame.pack(pady=20)
        
        # Add Customer button
        ttk.Button(button_frame, 
                  text="Add Customer", 
                  command=self.add_customer, 
                  style="TButton").pack(side=tk.LEFT, padx=10)
        
        # Clear Form button
        ttk.Button(button_frame, 
                  text="Clear Form", 
                  command=self.clear_form, 
                  style="TButton").pack(side=tk.LEFT, padx=10)
        
        # Back to Homepage button
        ttk.Button(button_frame, 
                  text="Back to Homepage", 
                  command=self.on_back, 
                  style="TButton").pack(side=tk.LEFT, padx=10)

    def validate_form(self):
        """
        Validate the form data before submission.
        
        Returns:
            bool: True if all validations pass, False otherwise
        """
        # Get field values
        name = self.entries["name_entry"].get().strip()
        mobile_number = self.entries["mobile_number_entry"].get().strip()
        email = self.entries["email_entry"].get().strip()
        id_proof_number = self.entries["id_proof_number_entry"].get().strip()
        
        # Reset validation message
        self.validation_message.set("")
        
        # Validate name field
        if not name:
            self.validation_message.set("Name cannot be empty")
            self.entries["name_entry"].focus_set()
            return False
            
        # Validate mobile number field
        if not mobile_number:
            self.validation_message.set("Mobile number cannot be empty")
            self.entries["mobile_number_entry"].focus_set()
            return False
        
        # Validate mobile number format (10 digits)
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            self.validation_message.set("Mobile number must be 10 digits")
            self.entries["mobile_number_entry"].focus_set()
            return False
            
        # Validate email field
        if not email:
            self.validation_message.set("Email cannot be empty")
            self.entries["email_entry"].focus_set()
            return False
            
        # Simple email validation (contains @ and .)
        if "@" not in email or "." not in email:
            self.validation_message.set("Please enter a valid email address")
            self.entries["email_entry"].focus_set()
            return False
            
        # Validate ID proof number field
        if not id_proof_number:
            self.validation_message.set("ID proof number cannot be empty")
            self.entries["id_proof_number_entry"].focus_set()
            return False
            
        return True
        
    def add_customer(self):
        """Add a new customer to the database after validation."""
        # Validate form first
        if not self.validate_form():
            return
            
        # Get all form values
        name = self.entries["name_entry"].get().strip()
        father_name = self.entries["father_name_entry"].get().strip()
        gender = self.gender_var.get()
        pincode = self.entries["pincode_entry"].get().strip()
        mobile_number = self.entries["mobile_number_entry"].get().strip()
        email = self.entries["email_entry"].get().strip()
        nationality = self.entries["nationality_entry"].get().strip()
        id_proof_type = self.id_proof_type.get()
        id_proof_number = self.entries["id_proof_number_entry"].get().strip()

        # Connect to database
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Check if customer with same mobile number already exists
                cursor.execute("SELECT id FROM customers WHERE mobile_number = %s", (mobile_number,))
                existing_customer = cursor.fetchone()
                
                if existing_customer:
                    self.validation_message.set(f"Customer with mobile {mobile_number} already exists")
                    return
                
                # Insert new customer record
                cursor.execute("""
                    INSERT INTO customers (
                        name, father_name, gender, pincode, 
                        mobile_number, email, nationality, 
                        id_proof_type, id_proof_number
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, father_name, gender, pincode, mobile_number, 
                     email, nationality, id_proof_type, id_proof_number))
                
                # Commit transaction
                connection.commit()
                messagebox.showinfo("Success", f"Customer {name} added successfully!")
                self.clear_form()
                
            except Exception as e:
                # Rollback on error
                connection.rollback()
                error_msg = str(e)
                
                # Provide user-friendly error messages for common cases
                if "Duplicate entry" in error_msg and "mobile_number" in error_msg:
                    self.validation_message.set(f"Customer with mobile {mobile_number} already exists")
                elif "Duplicate entry" in error_msg and "email" in error_msg:
                    self.validation_message.set(f"Customer with email {email} already exists")
                else:
                    messagebox.showerror("Database Error", f"Failed to add customer: {error_msg}")
            finally:
                # Close database resources
                cursor.close()
                connection.close()

    def clear_form(self):
        """Clear all form fields and reset to default values."""
        # Clear all entry widgets
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            
        # Reset to default selections
        self.gender_var.set("Male")
        self.id_proof_type.set("Aadhar")
        self.validation_message.set("")
        
        # Set default nationality
        self.entries["nationality_entry"].insert(0, "Indian")
        
        # Set focus back to name field
        self.entries["name_entry"].focus_set()