import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import pymysql

class PatientProfile:
    def __init__(self, root, user_name=None,username=None):
        self.root = root
        self.root.title("Patient Profile")
        self.root.state('zoomed')  # Maximize window
        
        # Store the username for database queries
        self.user_name = user_name
        self.username = username 
        
        # Configure styles
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Section.TLabelframe.Label', font=('Helvetica', 12, 'bold'))
        style.configure('Content.TLabel', font=('Helvetica', 10))
        
        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header(main_frame)
        
        # Create two columns
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create sections
        self.create_personal_info(self.left_frame)
        self.create_contact_info(self.left_frame)
        self.create_medical_records(right_frame)
        self.create_prescription(right_frame)
        self.create_doctors_comments(right_frame)
        
        # Bind selection event to medical records
        self.records_tree.bind('<<TreeviewSelect>>', self.on_record_select)
        
        # Add update profile button at right bottom of left frame
        self.create_update_button()
        
        # Add medical tests button
        self.create_back_to_dashboard_button()
        
        # Load data from database
        if self.username:
            self.load_user_data()
        else:
            messagebox.showwarning("No Username", "No username provided. Unable to load user data.")
        
    def create_header(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, 
                 text="Patient Profile",
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        # Save Changes button removed as updates will be handled on a different page
    
    def create_personal_info(self, parent):
        self.personal_frame = ttk.LabelFrame(parent,
                            text="Personal Information",
                            style='Section.TLabelframe',
                            padding="10")
        self.personal_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid layout for personal info
        labels = ['Name:', 'Age:', 'Birth Date:', 'Address:']
        for i, label in enumerate(labels):
            ttk.Label(self.personal_frame,
                    text=label,
                    style='Content.TLabel').grid(row=i, column=0,
                                                sticky=tk.W,
                                                pady=5,
                                                padx=5)
        
        # Read-only Label widgets instead of Entry widgets
        self.name_var = tk.StringVar()
        name_label = ttk.Label(self.personal_frame, textvariable=self.name_var, 
                            style='Content.TLabel', background='#f0f0f0', 
                            relief='sunken', padding=5)
        name_label.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        self.age_var = tk.StringVar()
        age_label = ttk.Label(self.personal_frame, textvariable=self.age_var,
                            style='Content.TLabel', background='#f0f0f0',
                            relief='sunken', padding=5)
        age_label.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # For birth date - replace DateEntry with a Label
        self.birth_date_var = tk.StringVar()
        birth_date_label = ttk.Label(self.personal_frame, textvariable=self.birth_date_var,
                                    style='Content.TLabel', background='#f0f0f0',
                                    relief='sunken', padding=5)
        birth_date_label.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Replace Text widget with a read-only Label for address
        self.address_var = tk.StringVar()
        address_label = ttk.Label(self.personal_frame, textvariable=self.address_var,
                                style='Content.TLabel', background='#f0f0f0',
                                relief='sunken', padding=5, wraplength=400)
        address_label.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Configure grid column weights
        self.personal_frame.columnconfigure(1, weight=1)
        return self.personal_frame

    def create_contact_info(self, parent):
        self.contact_frame = ttk.LabelFrame(parent,
                            text="Contact Information",
                            style='Section.TLabelframe',
                            padding="10")
        self.contact_frame.pack(fill=tk.X)
        
        # Grid layout for contact info
        labels = ['Phone Number:', 'Email:']
        for i, label in enumerate(labels):
            ttk.Label(self.contact_frame,
                    text=label,
                    style='Content.TLabel').grid(row=i, column=0,
                                                sticky=tk.W,
                                                pady=5,
                                                padx=5)
        
        # Label widgets instead of Entry widgets - these will be read-only
        self.phone_var = tk.StringVar()
        phone_label = ttk.Label(self.contact_frame, textvariable=self.phone_var, 
                            style='Content.TLabel', background='#f0f0f0', 
                            relief='sunken', padding=5)
        phone_label.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        self.email_var = tk.StringVar() 
        email_label = ttk.Label(self.contact_frame, textvariable=self.email_var,
                            style='Content.TLabel', background='#f0f0f0',
                            relief='sunken', padding=5)
        email_label.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Configure grid column weights
        self.contact_frame.columnconfigure(1, weight=1)
        return self.contact_frame
    
    def create_back_to_dashboard_button(self):
        # Create a frame at the bottom of left frame for the medical tests button
        tests_button_frame = ttk.Frame(self.left_frame)
        tests_button_frame.pack(fill=tk.X, pady=5)
        
        # Add medical tests button aligned to the right
        tests_label = ttk.Label(tests_button_frame, text="Back to Dashboard", 
                            background="#e1f0da", foreground="blue", 
                            font=("Helvetica", 12), anchor="center", 
                            borderwidth=2, relief="solid")
        # Place at the right of the frame
        tests_label.pack(side=tk.RIGHT, padx=10, pady=10)
        tests_label.bind('<Button-1>', lambda event: self.open_userdashboard())
    
    
    
    def create_update_button(self):
        # Create a frame at the bottom of left frame for the update button
        button_frame = ttk.Frame(self.left_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add update profile button aligned to the right
        update_label = ttk.Label(button_frame, text="Update Profile", 
                              background="#e1f0da", foreground="red", 
                              font=("Helvetica", 12), anchor="center", 
                              borderwidth=2, relief="solid")
        # Place at the right of the frame
        update_label.pack(side=tk.RIGHT, padx=10, pady=10)
        update_label.bind('<Button-1>', lambda event: self.open_updatepage())

    def create_medical_records(self, parent):
        frame = ttk.LabelFrame(parent,
                            text="Previous Medical Records",
                            style='Section.TLabelframe',
                            padding="10")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview for medical records
        columns = ('Doctor', 'Specialization', 'Appointment Date')
        self.records_tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configure columns
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=100)
        
        self.records_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame,
                                orient=tk.VERTICAL,
                                command=self.records_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_prescription(self, parent):
        frame = ttk.LabelFrame(parent,
                             text="Prescription",
                             style='Section.TLabelframe',
                             padding="10")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Text widget for prescription
        self.prescription_text = scrolledtext.ScrolledText(frame, height=5)
        self.prescription_text.pack(fill=tk.BOTH, expand=True)
    
    def create_doctors_comments(self, parent):
        frame = ttk.LabelFrame(parent,
                             text="Doctor's Comments",
                             style='Section.TLabelframe',
                             padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget for comments
        self.comments_text = scrolledtext.ScrolledText(frame, height=5)
        self.comments_text.pack(fill=tk.BOTH, expand=True)

    def load_user_data(self):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Drishti2005@',
                database='medimate'
            )
            
            try:
                with connection.cursor() as cursor:
                    # Execute query to fetch user data with separate address fields
                    query = """SELECT name, username, phone, email, password, dob, age, 
                            building_details, city, state, pincode FROM login WHERE username = %s"""
                    cursor.execute(query, (self.username,))
                    user_data = cursor.fetchone()
                    
                    if user_data:
                        # Populate personal information fields
                        self.name_var.set(user_data[0])  # name
                        self.age_var.set(user_data[6])   # age
                        
                        # Handle date format for the label
                        if user_data[5]:  # dob
                            try:
                                # Format the date for display
                                date_obj = user_data[5]
                                if isinstance(date_obj, datetime):
                                    formatted_date = date_obj.strftime('%Y-%m-%d')
                                else:
                                    formatted_date = str(date_obj)
                                self.birth_date_var.set(formatted_date)
                            except Exception as e:
                                messagebox.showwarning("Date Format Error", f"Could not format birth date: {e}")
                                self.birth_date_var.set("Not available")
                        else:
                            self.birth_date_var.set("Not available")
                        
                        # Combine address components
                        building = user_data[7] if user_data[7] else ""
                        city = user_data[8] if user_data[8] else ""
                        state = user_data[9] if user_data[9] else ""
                        pincode = user_data[10] if user_data[10] else ""
                        
                        # Format address
                        full_address = ""
                        if building:
                            full_address += f"{building}\n"
                        if city or state or pincode:
                            full_address += f"{city}, {state} {pincode}".strip()
                        
                        # Set address
                        self.address_var.set(full_address)
                        
                        # Populate contact information fields
                        self.phone_var.set(user_data[2])  # phone
                        self.email_var.set(user_data[3])  # email
                        
                        # Load medical records
                        self.load_medical_records()
                        
                        # Load most recent medical record's comments and prescription
                        self.load_most_recent_record()
                    else:
                        messagebox.showinfo("User Not Found", f"No user data found for username: {self.username}")
            
            except pymysql.Error as e:
                messagebox.showerror("Database Error", f"Error fetching data: {e}")
            
            finally:
                connection.close()
                
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
            
    def load_most_recent_record(self):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Drishti2005@',
                database='medimate'
            )
            
            try:
                with connection.cursor() as cursor:
                    # Query to fetch the most recent appointment
                    query = """
                    SELECT 
                        d_name, 
                        appoint_date 
                    FROM 
                        patient_records 
                    WHERE 
                        p_username = %s 
                    ORDER BY 
                        appoint_date DESC 
                    LIMIT 1
                    """
                    cursor.execute(query, (self.username,))
                    recent_record = cursor.fetchone()
                    
                    # Reset text widgets
                    self.comments_text.config(state='normal')
                    self.prescription_text.config(state='normal')
                    self.comments_text.delete('1.0', tk.END)
                    self.prescription_text.delete('1.0', tk.END)
                    
                    if recent_record:
                        # Fetch comments and prescription for the most recent record
                        details_query = """
                        SELECT comments, prescription 
                        FROM doc_replies 
                        WHERE username = %s
                        AND appoint_date = %s
                        """
                        cursor.execute(details_query, (self.username, recent_record[1]))
                        result = cursor.fetchone()
                        
                        if result:
                            # Insert comments
                            self.comments_text.insert('1.0', result[0] if result[0] else "No comments available.")
                            
                            # Insert prescription
                            self.prescription_text.insert('1.0', result[1] if result[1] else "No prescription available.")
                        else:
                            # If no records found
                            self.comments_text.insert('1.0', "No comments available.")
                            self.prescription_text.insert('1.0', "No prescription available.")
                    else:
                        # If no recent appointments
                        self.comments_text.insert('1.0', "No recent medical records.")
                        self.prescription_text.insert('1.0', "No recent prescriptions.")
                    
                    # Set to readonly
                    self.comments_text.config(state='disabled')
                    self.prescription_text.config(state='disabled')
            
            except pymysql.Error as e:
                messagebox.showwarning("Data Error", f"Failed to load doctor data: {e}")
            
            finally:
                connection.close()
                
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")
        
    def load_doc_replies(self, doctor_name, appoint_date):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Drishti2005@',
                database='medimate'
            )
            
            try:
                # Reset text widgets
                self.comments_text.config(state='normal')
                self.prescription_text.config(state='normal')
                self.comments_text.delete('1.0', tk.END)
                self.prescription_text.delete('1.0', tk.END)
                
                with connection.cursor() as cursor:
                    # Query to fetch comments and prescription using patient username and appointment date
                    query = """
                    SELECT comments, prescription 
                    FROM doc_replies 
                    WHERE username = %s 
                    AND appoint_date = %s
                    """
                    cursor.execute(query, (self.username, appoint_date))
                    result = cursor.fetchone()
                    
                    if result:
                        # Insert comments
                        self.comments_text.insert('1.0', result[0] if result[0] else "No comments available.")
                        
                        # Insert prescription
                        self.prescription_text.insert('1.0', result[1] if result[1] else "No prescription available.")
                    else:
                        # If no records found
                        self.comments_text.insert('1.0', "No comments available.")
                        self.prescription_text.insert('1.0', "No prescription available.")
                    
                    # Set to readonly
                    self.comments_text.config(state='disabled')
                    self.prescription_text.config(state='disabled')
            
            except pymysql.Error as e:
                messagebox.showwarning("Data Error", f"Failed to load doctor data: {e}")
            
            finally:
                connection.close()
                
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")

    
    def load_medical_records(self):
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Drishti2005@',
                database='medimate'
            )
            
            try:
                with connection.cursor() as cursor:
                    # Fetch medical records from patient_records table
                    query = """
                    SELECT 
                        d_name, 
                        specialization, 
                        appoint_date
                    FROM 
                        patient_records
                    WHERE 
                        p_username = %s
                    ORDER BY 
                        appoint_date DESC
                    """
                    cursor.execute(query, (self.username,))
                    records = cursor.fetchall()
                    
                    # Clear existing items
                    for item in self.records_tree.get_children():
                        self.records_tree.delete(item)
                    
                    # Insert records into treeview
                    for record in records:
                        self.records_tree.insert('', 'end', values=(
                            record[0],  # Doctor Name
                            record[1],  # Specialization
                            record[2]   # Appointment Date
                        ), tags=(str(record[2]),))  # Store appointment date as a tag
            
            except pymysql.Error as e:
                messagebox.showwarning("Records Error", f"Failed to load medical records: {e}")
            
            finally:
                connection.close()
                
        except pymysql.Error as e:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {e}")

    def on_record_select(self, event):
        # Get the selected item
        selected_item = self.records_tree.selection()
        
        if not selected_item:
            return
        
        # Get the values of the selected record
        record_values = self.records_tree.item(selected_item[0])['values']
        
        # Check if we have enough data
        if len(record_values) < 3:
            messagebox.showwarning("Selection Error", "Unable to retrieve record details.")
            return
        
        # Extract doctor name and appointment date
        doctor_name = record_values[0]
        appoint_date = record_values[2]
        
        # Fetch prescription and comments for this specific record
        self.load_doc_replies(doctor_name, appoint_date)


    def open_updatepage(self):
        self.root.destroy()
        from updateprofile import ProfileUpdateApp
        root = tk.Tk()
        app = ProfileUpdateApp(root,self.user_name,self.username)
        root.mainloop()

    def open_userdashboard(self):
        self.root.destroy()
        from userdashboard import NavigationApp
        root = tk.Tk()
        app = NavigationApp(root, self.user_name, self.username)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    username = sys.argv[1]
    app = PatientProfile(root, username)
    root.mainloop()