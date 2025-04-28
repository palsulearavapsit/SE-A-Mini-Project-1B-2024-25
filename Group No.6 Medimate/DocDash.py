import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import tkinter.messagebox as messagebox
import mysql.connector
from mysql.connector import Error

class DoctorDashboard:
    def __init__(self, root, doc_username, doctor_name=None):
        self.root = root
        self.root.title("Doctor's Dashboard - Medimate")
        self.root.state('zoomed')  # Maximize window
        
        # User information
        self.doctor_username = doc_username
        self.doctor_name = doctor_name if doctor_name else doc_username
        
        # Database connection params - update these based on your actual configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Drishti2005@',
            'database': 'medimate'
        }
        
        # Database connection
        self.db_connection = None
        self.connect_to_database()
        
        # Currently selected patient
        self.current_patient_username = None
        
        # Configure style and set white background
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        style.configure('TLabelframe', background='white')
        style.configure('TLabelframe.Label', background='white')
        style.configure('Green.TFrame', background='#e8f5e9')  # Light green background
        style.configure('Orange.TFrame', background='#fff3e0')  # Light orange background
        
        # Configure button styles
        style.configure('Accept.TButton',
                       background='#4CAF50',  # Green
                       font=('Helvetica', 9, 'bold'))
        
        style.configure('Decline.TButton',
                       background='#F44336',  # Red
                       font=('Helvetica', 9, 'bold'))
        
        # Logout button 
        style.configure('Logout.TButton',
                       background='white',
                       foreground='#FF0000',  # Red text
                       font=('Helvetica', 10, 'bold'))
        
        style.map('Accept.TButton',
                 background=[('active', '#45a049')])  # Darker green when clicked
        
        style.map('Decline.TButton',
                 background=[('active', '#da190b')])  # Darker red when clicked
        
        style.map('Logout.TButton',
                 background=[('active', '#f8f8f8')])  # Slightly grey when clicked
        
        # Set root window background
        self.root.configure(bg='white')
        
        # Create main containers
        self.create_header()
        self.create_main_content()
    
    def connect_to_database(self):
        """Establish connection to MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(
                host=self.db_config['host'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            if self.db_connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
    
    def create_header(self):
        header = ttk.Frame(self.root, padding="10", style='TFrame')
        header.pack(fill=tk.X)
        
        # Left section for logout button
        left_section = ttk.Frame(header, style='TFrame')
        left_section.pack(side=tk.LEFT, padx=(0, 20))
        
        # Logout button
        logout_btn = ttk.Button(left_section, 
                              text="Logout",
                              style='Logout.TButton',
                              command=self.handle_logout)
        logout_btn.pack(side=tk.LEFT)
        
        # Logo and title
        title_label = ttk.Label(header, text="MEDIMATE", font=('Helvetica', 24, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Welcome message with doctor name
        doctor_label = ttk.Label(header, 
                               text=f"Welcome, Dr. {self.doctor_name}",
                               font=('Helvetica', 12, 'italic'))
        doctor_label.pack(side=tk.LEFT, padx=20)
        
        # Date and time
        date_label = ttk.Label(header, 
                             text=datetime.now().strftime("%B %d, %Y"),
                             font=('Helvetica', 12))
        date_label.pack(side=tk.RIGHT)

    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if self.db_connection and self.db_connection.is_connected():
                self.db_connection.close()
                print("Database connection closed")
            
            self.root.destroy()  # Close the current window
            from login import LoginPage
            app = LoginPage()

    def create_main_content(self):
        main_container = ttk.Frame(self.root, padding="10", style='TFrame')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create three columns
        self.create_left_column(main_container)
        self.create_middle_column(main_container)
        self.create_right_column(main_container)
        
        # Load default patient after all columns are created
        self.load_default_patient()
        
    def create_left_column(self, parent):
        left_frame = ttk.Frame(parent, padding="5", style='TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Ongoing Patients Section
        ongoing_label = ttk.Label(left_frame, text="Ongoing Patients",
                                font=('Helvetica', 12, 'bold'))
        ongoing_label.pack(fill=tk.X, pady=5)
        
        # Ongoing Patients List
        ongoing_frame = ttk.Frame(left_frame, style='Green.TFrame')
        ongoing_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fetch ongoing patients from database
        ongoing_patients = self.fetch_ongoing_patients()
        
        if ongoing_patients:
            for i, patient in enumerate(ongoing_patients):
                patient_frame = ttk.Frame(ongoing_frame, padding="5", style='TFrame')
                patient_frame.pack(fill=tk.X, pady=2)
                
                patient_info_frame = ttk.Frame(patient_frame, style='TFrame')
                patient_info_frame.pack(fill=tk.X)
                
                patient_button = ttk.Button(
                    patient_info_frame, 
                    text=f"{patient['p_name']}",
                    command=lambda p_username=patient['p_username']: self.load_patient_details(p_username)
                )
                patient_button.pack(side=tk.LEFT)
                
                ttk.Label(patient_info_frame,
                         text="In Progress",
                         foreground='green').pack(side=tk.RIGHT)
                
                # Add Complete Button below patient info
                stop_btn = ttk.Button(
                    patient_frame,
                    text="Complete",
                    style='Accept.TButton',  # Using the green button style
                    command=lambda p_user=patient['p_username']: self.complete_appointment(p_user)
                )
                stop_btn.pack(pady=(5, 0))
        else:
            ttk.Label(ongoing_frame, text="No ongoing patients").pack(pady=10)
        
        # Upcoming Patients Section
        upcoming_label = ttk.Label(left_frame, text="Upcoming Patients",
                                 font=('Helvetica', 12, 'bold'))
        upcoming_label.pack(fill=tk.X, pady=5)
        
        # Upcoming Patients List
        upcoming_frame = ttk.Frame(left_frame, style='Orange.TFrame')
        upcoming_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fetch upcoming patients from database
        upcoming_patients = self.fetch_upcoming_patients()
        
        if upcoming_patients:
            for i, patient in enumerate(upcoming_patients):
                patient_frame = ttk.Frame(upcoming_frame, padding="5", style='TFrame')
                patient_frame.pack(fill=tk.X, pady=2)
                
                patient_info_frame = ttk.Frame(patient_frame, style='TFrame')
                patient_info_frame.pack(fill=tk.X)
                
                patient_button = ttk.Button(
                    patient_info_frame, 
                    text=f"{patient['p_name']}",
                    command=lambda p_username=patient['p_username']: self.load_patient_details(p_username)
                )
                patient_button.pack(side=tk.LEFT)
                
                date_string = patient['appoint_date'].strftime("%b %d") if patient['appoint_date'] else "N/A"
                time_string = patient['appoint_time'] if patient['appoint_time'] else "N/A"
                
                ttk.Label(patient_info_frame,
                         text=f"{date_string}, {time_string}",
                         foreground='orange').pack(side=tk.RIGHT)
                
                # Add Start Button below patient info
                start_btn = ttk.Button(
                    patient_frame,
                    text="Start",
                    style='Accept.TButton',
                    command=lambda p_user=patient['p_username']: self.start_appointment(p_user)
                )
                start_btn.pack(pady=(5, 0))
        else:
            ttk.Label(upcoming_frame, text="No upcoming patients").pack(pady=10)
    
    def create_middle_column(self, parent):
        self.middle_frame = ttk.Frame(parent, padding="5", style='TFrame')
        self.middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Patient Details Section
        self.details_frame = ttk.LabelFrame(self.middle_frame, text="Patient Details",
                                    padding="10")
        self.details_frame.pack(fill=tk.X, pady=5)
        
        # Create grid for patient details
        self.patient_details_widgets = {}
        details_labels = ["Name:", "DOB:", "Age:", "Address:", "Appointment Date:", "Appointment Time:"]
        
        for i, label in enumerate(details_labels):
            ttk.Label(self.details_frame, text=label).grid(row=i, column=0, sticky='w', pady=2, padx=5)
            value_label = ttk.Label(self.details_frame, text="")
            value_label.grid(row=i, column=1, sticky='w', pady=2, padx=5)
            self.patient_details_widgets[label] = value_label
        
        # Medical Content Container
        medical_container = ttk.Frame(self.middle_frame, style='TFrame')
        medical_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Prescription Section
        prescription_frame = ttk.LabelFrame(medical_container, text="Prescription",
                                   padding="10")
        prescription_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.notes_text = scrolledtext.ScrolledText(prescription_frame, height=10)
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        
        save_notes_btn = ttk.Button(prescription_frame, text="Save Prescription",
                                  command=self.save_notes)
        save_notes_btn.pack(pady=5)
        
        # Doctor's Comments Section (Moved from right column)
        comments_frame = ttk.Labelframe(medical_container, text="Doctor Comments",
                                      padding="10")
        comments_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.prescription_text = scrolledtext.ScrolledText(comments_frame, height=10)
        self.prescription_text.pack(fill=tk.BOTH, expand=True)
        
        save_prescription_btn = ttk.Button(comments_frame,
                                         text="Save Comments",
                                         command=self.save_prescription)
        save_prescription_btn.pack(pady=5)
        
    def create_right_column(self, parent):
        right_frame = ttk.Frame(parent, padding="5", style='TFrame')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Appointment Requests Section
        requests_frame = ttk.LabelFrame(right_frame, text="Appointment Requests",
                                    padding="10")
        requests_frame.pack(fill=tk.BOTH, expand=False, pady=5)
        
        # Fetch appointment requests from database
        appointment_requests = self.fetch_appointment_requests()
        
        if appointment_requests:
            for i, request in enumerate(appointment_requests):
                request_frame = ttk.Frame(requests_frame, padding="5", style='TFrame')
                request_frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(request_frame,
                        text=f"{request['p_name']}",
                        font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
                
                date_string = request['appoint_date'].strftime("%b %d, %Y") if request['appoint_date'] else "N/A"
                time_string = request['appoint_time'] if request['appoint_time'] else "N/A"
                
                ttk.Label(request_frame,
                        text=f"Requested for: {date_string} at {time_string}").pack(anchor=tk.W)
                
                btn_frame = ttk.Frame(request_frame, style='TFrame')
                btn_frame.pack(fill=tk.X, pady=2)
                
                # Using a composite key (doctor username + patient username) as there's no ID in the table
                composite_key = (request['d_username'], request['p_username'])
                
                ttk.Button(btn_frame, text="Accept",
                        style='Accept.TButton',
                        command=lambda key=composite_key: self.handle_request(key, "accept")).pack(side=tk.LEFT, padx=2)
                ttk.Button(btn_frame, text="Decline",
                        style='Decline.TButton',
                        command=lambda key=composite_key: self.handle_request(key, "decline")).pack(side=tk.LEFT, padx=2)
        else:
            ttk.Label(requests_frame, text="No pending appointment requests").pack(pady=10)
        
        # Completed Appointments Section
        completed_frame = ttk.LabelFrame(right_frame, text="Completed Appointments",
                                    padding="10")
        completed_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for completed appointments
        completed_tree = ttk.Treeview(completed_frame, columns=("name", "date", "time"), 
                                show="headings", height=8)  # Reduced height to make room for patient records
        completed_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(completed_tree, orient="vertical", command=completed_tree.yview)
        completed_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure columns
        completed_tree.heading("name", text="Patient Name")
        completed_tree.heading("date", text="Date")
        completed_tree.heading("time", text="Time")
        
        completed_tree.column("name", width=150)
        completed_tree.column("date", width=100)
        completed_tree.column("time", width=100)
        
        # Add binding for click event
        completed_tree.bind("<ButtonRelease-1>", self.completed_appointment_clicked)
        
        # Store the tree widget as instance variable to access it later
        self.completed_tree = completed_tree
        
        # Fetch and display completed appointments
        completed_appointments = self.fetch_completed_appointments()
        
        if completed_appointments:
            for appointment in completed_appointments:
                date_string = appointment['appoint_date'].strftime("%b %d, %Y") if appointment['appoint_date'] else "N/A"
                time_string = appointment['appoint_time'] if appointment['appoint_time'] else "N/A"
                
                # Store patient username as item ID for reference when clicked
                item_id = completed_tree.insert("", "end", values=(
                    appointment['p_name'],
                    date_string,
                    time_string
                ))
                # Store the patient username as a tag for the item
                completed_tree.item(item_id, tags=(appointment['p_username'],))
        else:
            ttk.Label(completed_frame, text="No completed appointments").pack(pady=10)
        
        # Patient Records Section (New addition)
        records_frame = ttk.LabelFrame(right_frame, text="Patient Medical History",
                                    padding="10")
        records_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for patient records
        records_tree = ttk.Treeview(records_frame, 
                                columns=("doctor", "specialization", "date"), 
                                show="headings", 
                                height=8)
        records_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar for records tree
        records_scrollbar = ttk.Scrollbar(records_tree, orient="vertical", command=records_tree.yview)
        records_tree.configure(yscrollcommand=records_scrollbar.set)
        records_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure columns
        records_tree.heading("doctor", text="Doctor Name")
        records_tree.heading("specialization", text="Specialization")
        records_tree.heading("date", text="Date")
        
        records_tree.column("doctor", width=150)
        records_tree.column("specialization", width=150)
        records_tree.column("date", width=100)
        
        # Add binding for click event
        records_tree.bind("<ButtonRelease-1>", self.patient_record_clicked)
        
        # Store the tree widget as instance variable to access it later
        self.records_tree = records_tree
        
        # Default message when no patient selected
        self.records_label = ttk.Label(records_frame, text="Select a patient to view medical history")
        self.records_label.pack(pady=5)


    def fetch_ongoing_patients(self):
        """Fetch ongoing patients from database"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM appointment WHERE d_username = %s AND status = 'ongoing' ORDER BY appoint_date ASC"
            cursor.execute(query, (self.doctor_username,))
            patients = cursor.fetchall()
            cursor.close()
            return patients
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching ongoing patients: {e}")
            return []
    
    def fetch_upcoming_patients(self):
        """Fetch upcoming patients from database"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM appointment WHERE d_username = %s AND status = 'upcoming' ORDER BY appoint_date ASC"
            cursor.execute(query, (self.doctor_username,))
            patients = cursor.fetchall()
            cursor.close()
            return patients
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching upcoming patients: {e}")
            return []
    
    def fetch_appointment_requests(self):
        """Fetch appointment requests from database"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM appointment WHERE d_username = %s AND status = 'requested' ORDER BY appoint_date ASC"
            cursor.execute(query, (self.doctor_username,))
            requests = cursor.fetchall()
            cursor.close()
            return requests
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching appointment requests: {e}")
            return []
    
    def fetch_completed_appointments(self):
        """Fetch completed appointments from database"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = "SELECT * FROM appointment WHERE d_username = %s AND status = 'completed' ORDER BY appoint_date DESC"
            cursor.execute(query, (self.doctor_username,))
            completed = cursor.fetchall()
            cursor.close()
            return completed
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching completed appointments: {e}")
            return []
    

    def start_appointment(self, patient_username):
        """Move patient from upcoming to ongoing status"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # First, get the appointment date for this patient
            date_query = """
            SELECT appoint_date 
            FROM appointment 
            WHERE p_username = %s AND d_username = %s AND status = 'upcoming'
            ORDER BY appoint_date ASC
            LIMIT 1
            """
            cursor.execute(date_query, (patient_username, self.doctor_username))
            appointment = cursor.fetchone()
            
            if not appointment or not appointment['appoint_date']:
                messagebox.showwarning("Warning", "No appointment date found!")
                cursor.close()
                return
            
            appoint_date = appointment['appoint_date']
            
            # Update appointment status from upcoming to ongoing with appointment date constraint
            query = """
            UPDATE appointment 
            SET status = 'ongoing' 
            WHERE p_username = %s AND d_username = %s AND status = 'upcoming' AND appoint_date = %s
            """
            cursor.execute(query, (patient_username, self.doctor_username, appoint_date))
            
            self.db_connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                messagebox.showinfo("Success", "Appointment started successfully!")
                # Load the patient details
                self.load_patient_details(patient_username)
                # Refresh the dashboard to update lists
                self.refresh_dashboard()
            else:
                messagebox.showwarning("Warning", "Could not start appointment. Please try again.")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error starting appointment: {e}")
    
    def complete_appointment(self, patient_username):
        """Mark appointment as completed and record patient record"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Fetch the appointment date
            fetch_appoint_query = """
            SELECT appoint_date
            FROM appointment 
            WHERE p_username = %s AND d_username = %s AND status = 'ongoing'
            ORDER BY appoint_date ASC
            LIMIT 1
            """
            cursor.execute(fetch_appoint_query, (patient_username, self.doctor_username))
            appointment_details = cursor.fetchone()
            
            # Fetch doctor's specialization from doc_info table
            fetch_spec_query = """
            SELECT specialization
            FROM doc_info 
            WHERE username = %s
            """
            cursor.execute(fetch_spec_query, (self.doctor_username,))
            doc_info = cursor.fetchone()
            
            if not appointment_details:
                messagebox.showwarning("Warning", "Could not find ongoing appointment details.")
                cursor.close()
                return
            
            if not doc_info:
                messagebox.showwarning("Warning", "Could not find doctor's specialization.")
                cursor.close()
                return
            
            appoint_date = appointment_details['appoint_date']
            
            # Update appointment status from ongoing to completed with appointment date constraint
            update_query = """
            UPDATE appointment 
            SET status = 'completed' 
            WHERE p_username = %s AND d_username = %s AND status = 'ongoing' AND appoint_date = %s
            """
            cursor.execute(update_query, (patient_username, self.doctor_username, appoint_date))
            
            # Insert into patient_records table
            insert_query = """
            INSERT INTO patient_records 
            (d_name, d_username, p_username, specialization, appoint_date) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                self.doctor_name,  # Doctor's name passed during initialization 
                self.doctor_username, 
                patient_username, 
                doc_info['specialization'], 
                appoint_date
            ))
            
            self.db_connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                messagebox.showinfo("Success", "Appointment completed and patient record created successfully!")
                # Refresh the dashboard to update lists
                self.refresh_dashboard()
            else:
                messagebox.showwarning("Warning", "Could not complete appointment. Please try again.")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error completing appointment: {e}")
    
    def load_default_patient(self):
        """Load the first patient in the list or show default message"""
        ongoing_patients = self.fetch_ongoing_patients()
        if ongoing_patients:
            self.load_patient_details(ongoing_patients[0]['p_username'])
        else:
            # Display empty/default values
            for label, widget in self.patient_details_widgets.items():
                widget.config(text="--")
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.insert(tk.END, "")
            self.prescription_text.delete("1.0", tk.END)
            self.prescription_text.insert(tk.END, "")
    
    def load_patient_details(self, patient_username):
        """Load patient details from database based on patient username"""
        self.current_patient_username = patient_username
        
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Fetch patient basic info from appointment table joined with login table
            query = """
            SELECT 
                a.p_name, 
                a.p_username,
                a.appoint_date,
                a.appoint_time,
                l.dob,
                l.age,
                l.building_details,
                l.city,
                l.state,
                l.pincode
            FROM appointment a
            LEFT JOIN login l ON a.p_username = l.username
            WHERE a.p_username = %s AND a.d_username = %s
            ORDER BY 
                CASE 
                    WHEN a.status = 'ongoing' THEN 1
                    WHEN a.status = 'upcoming' THEN 2
                    ELSE 3
                END,
                a.appoint_date ASC
            LIMIT 1
            """
            cursor.execute(query, (patient_username, self.doctor_username))
            patient = cursor.fetchone()
            # Consume any remaining rows to prevent "unread result found" error
            cursor.fetchall()
            
            if patient:
                # Update UI with patient details
                self.patient_details_widgets["Name:"].config(text=patient['p_name'])
                
                # Display DOB
                dob_string = patient['dob'].strftime("%b %d, %Y") if patient['dob'] else "Not provided"
                self.patient_details_widgets["DOB:"].config(text=dob_string)
                
                # Display Age
                age_string = str(patient['age']) if patient['age'] else "Not provided"
                self.patient_details_widgets["Age:"].config(text=age_string)
                
                # Create and display full address
                address_parts = []
                if patient['building_details']:
                    address_parts.append(patient['building_details'])
                if patient['city']:
                    address_parts.append(patient['city'])
                if patient['state']:
                    address_parts.append(patient['state'])
                if patient['pincode']:
                    address_parts.append(str(patient['pincode']))
                
                full_address = ", ".join(address_parts) if address_parts else "Address not provided"
                self.patient_details_widgets["Address:"].config(text=full_address)
                
                date_string = patient['appoint_date'].strftime("%b %d, %Y") if patient['appoint_date'] else "Not scheduled"
                self.patient_details_widgets["Appointment Date:"].config(text=date_string)
                
                time_string = patient['appoint_time'] if patient['appoint_time'] else "Not specified"
                self.patient_details_widgets["Appointment Time:"].config(text=time_string)
                
                # Rest of the function for fetching prescription, comments and patient records remains the same...
                
                # Fetch latest prescription if any
                query = """
                SELECT prescription 
                FROM doc_replies 
                WHERE username = %s AND appoint_date = %s
                """
                cursor.execute(query, (patient_username, patient['appoint_date']))
                prescription = cursor.fetchone()
                # Consume any remaining rows
                cursor.fetchall()
                
                self.notes_text.delete("1.0", tk.END)
                if prescription and 'prescription' in prescription and prescription['prescription']:
                    self.notes_text.insert(tk.END, prescription['prescription'])
                
                # Fetch latest comments if any
                query = """
                SELECT comments 
                FROM doc_replies 
                WHERE username = %s AND appoint_date = %s
                """
                cursor.execute(query, (patient_username, patient['appoint_date']))
                comments = cursor.fetchone()
                # Consume any remaining rows
                cursor.fetchall()
                
                self.prescription_text.delete("1.0", tk.END)
                if comments and 'comments' in comments and comments['comments']:
                    self.prescription_text.insert(tk.END, comments['comments'])
                
                # Load patient medical history records
                self.update_patient_records(patient_username)
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading patient details: {e}")
    
    def save_notes(self):
        """Save prescription to database for current patient with appointment date"""
        if not self.current_patient_username:
            messagebox.showwarning("Warning", "No patient selected!")
            return
        
        prescription_text = self.notes_text.get("1.0", tk.END).strip()
        
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Fetch the current appointment date for this patient
            date_query = """
            SELECT appoint_date 
            FROM appointment 
            WHERE p_username = %s AND d_username = %s 
            AND (status = 'ongoing' OR status = 'upcoming' OR status = 'completed')
            ORDER BY appoint_date DESC 
            LIMIT 1
            """
            cursor.execute(date_query, (self.current_patient_username, self.doctor_username))
            appointment = cursor.fetchone()
            
            if not appointment or not appointment['appoint_date']:
                messagebox.showwarning("Warning", "No appointment date found!")
                cursor.close()
                return
            
            appoint_date = appointment['appoint_date']
            
            # Check if entry exists
            check_query = "SELECT * FROM doc_replies WHERE username = %s AND appoint_date = %s"
            cursor.execute(check_query, (self.current_patient_username, appoint_date))
            result = cursor.fetchone()
            
            if result:
                # Update existing entry
                query = "UPDATE doc_replies SET prescription = %s WHERE username = %s AND appoint_date = %s"
                cursor.execute(query, (prescription_text, self.current_patient_username, appoint_date))
            else:
                # Insert new entry
                query = "INSERT INTO doc_replies (username, prescription, appoint_date) VALUES (%s, %s, %s)"
                cursor.execute(query, (self.current_patient_username, prescription_text, appoint_date))
            
            self.db_connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Prescription saved successfully!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error saving prescription: {e}")

    def save_prescription(self):
        """Save doctor comments to database for current patient with appointment date"""
        if not self.current_patient_username:
            messagebox.showwarning("Warning", "No patient selected!")
            return
        
        comments = self.prescription_text.get("1.0", tk.END).strip()
        
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Fetch the current appointment date for this patient
            date_query = """
            SELECT appoint_date 
            FROM appointment 
            WHERE p_username = %s AND d_username = %s 
            AND (status = 'ongoing' OR status = 'upcoming' OR status = 'completed')
            ORDER BY appoint_date DESC 
            LIMIT 1
            """
            cursor.execute(date_query, (self.current_patient_username, self.doctor_username))
            appointment = cursor.fetchone()
            
            if not appointment or not appointment['appoint_date']:
                messagebox.showwarning("Warning", "No appointment date found!")
                cursor.close()
                return
            
            appoint_date = appointment['appoint_date']
            
            # Check if entry exists
            check_query = "SELECT * FROM doc_replies WHERE username = %s AND appoint_date = %s"
            cursor.execute(check_query, (self.current_patient_username, appoint_date))
            result = cursor.fetchone()
            
            if result:
                # Update existing entry
                query = "UPDATE doc_replies SET comments = %s WHERE username = %s AND appoint_date = %s"
                cursor.execute(query, (comments, self.current_patient_username, appoint_date))
            else:
                # Insert new entry
                query = "INSERT INTO doc_replies (username, comments, appoint_date) VALUES (%s, %s, %s)"
                cursor.execute(query, (self.current_patient_username, comments, appoint_date))
            
            self.db_connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "Comments saved successfully!")
        except Error as e:
            messagebox.showerror("Database Error", f"Error saving comments: {e}")
    
    def handle_request(self, composite_key, action):
        """Handle appointment request acceptance or rejection"""
        d_username, p_username = composite_key
        
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # First, get the appointment date for this request
            date_query = """
            SELECT appoint_date 
            FROM appointment 
            WHERE p_username = %s AND d_username = %s AND status = 'requested'
            ORDER BY appoint_date ASC
            LIMIT 1
            """
            cursor.execute(date_query, (p_username, d_username))
            appointment = cursor.fetchone()
            
            if not appointment or not appointment['appoint_date']:
                messagebox.showwarning("Warning", "No appointment date found for this request!")
                cursor.close()
                return
            
            appoint_date = appointment['appoint_date']
            
            if action == "accept":
                # Update request status to upcoming with appointment date constraint
                query = """
                UPDATE appointment 
                SET status = 'upcoming' 
                WHERE d_username = %s AND p_username = %s AND status = 'requested' AND appoint_date = %s
                """
                cursor.execute(query, (d_username, p_username, appoint_date))
                
                action_text = "accepted"
            else:
                # Update request status to rejected with appointment date constraint
                query = """
                UPDATE appointment 
                SET status = 'rejected' 
                WHERE d_username = %s AND p_username = %s AND status = 'requested' AND appoint_date = %s
                """
                cursor.execute(query, (d_username, p_username, appoint_date))
                
                action_text = "declined"
            
            self.db_connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            if affected_rows > 0:
                messagebox.showinfo("Success", f"Appointment request {action_text}!")
                # Refresh the appointment requests list
                self.refresh_dashboard()
            else:
                messagebox.showwarning("Warning", f"Could not {action_text} the appointment request. Please try again.")
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error handling appointment request: {e}")
    
    def refresh_dashboard(self):
        """Refresh all data displayed in the dashboard"""
        # Get parent container
        parent = self.middle_frame.master
        
        # Destroy all existing widgets
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Recreate columns with fresh data
        self.create_left_column(parent)
        self.create_middle_column(parent)
        self.create_right_column(parent)
        
        # Load default patient
        self.load_default_patient()

    def completed_appointment_clicked(self, event):
        """Handle click on completed appointment row"""
        # Get the selected item
        selected_item = self.completed_tree.focus()
        
        if selected_item:  # If an item is selected
            # Get the patient username from the item's tags
            patient_username = self.completed_tree.item(selected_item, "tags")[0]
            
            # Get the appointment date from the selected item's values
            item_values = self.completed_tree.item(selected_item, "values")
            selected_date = item_values[1]  # Date is the second column
            selected_time = item_values[2]  # Time is the third column
            
            if patient_username:
                if not self.db_connection or not self.db_connection.is_connected():
                    self.connect_to_database()
                    if not self.db_connection.is_connected():
                        return
                
                try:
                    cursor = self.db_connection.cursor(dictionary=True)
                    
                    # Convert string date back to datetime object for database query
                    try:
                        parsed_date = datetime.strptime(selected_date, "%b %d, %Y")
                        formatted_date = parsed_date.strftime("%Y-%m-%d")  # Format for database query
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format")
                        cursor.close()
                        return
                    
                    # Fetch prescription and comments for the specific appointment date
                    query = """
                    SELECT prescription, comments
                    FROM doc_replies
                    WHERE username = %s AND appoint_date = %s
                    """
                    cursor.execute(query, (patient_username, formatted_date))
                    record = cursor.fetchone()
                    
                    # Fetch patient info including login table data
                    patient_query = """
                    SELECT a.p_name, a.p_username, a.appoint_time,
                        l.dob, l.age, l.building_details, l.city, l.state, l.pincode
                    FROM appointment a
                    LEFT JOIN login l ON a.p_username = l.username
                    WHERE a.p_username = %s AND a.d_username = %s AND a.appoint_date = %s
                    """
                    cursor.execute(patient_query, (patient_username, self.doctor_username, formatted_date))
                    patient = cursor.fetchone()
                    cursor.close()
                    
                    # Update patient details section
                    if patient:
                        self.patient_details_widgets["Name:"].config(text=patient['p_name'])
                        
                        # Display DOB
                        dob_string = patient['dob'].strftime("%b %d, %Y") if patient['dob'] else "Not provided"
                        self.patient_details_widgets["DOB:"].config(text=dob_string)
                        
                        # Display Age
                        age_string = str(patient['age']) if patient['age'] else "Not provided"
                        self.patient_details_widgets["Age:"].config(text=age_string)
                        
                        # Create and display full address
                        address_parts = []
                        if patient['building_details']:
                            address_parts.append(patient['building_details'])
                        if patient['city']:
                            address_parts.append(patient['city'])
                        if patient['state']:
                            address_parts.append(patient['state'])
                        if patient['pincode']:
                            address_parts.append(str(patient['pincode']))
                        
                        full_address = ", ".join(address_parts) if address_parts else "Address not provided"
                        self.patient_details_widgets["Address:"].config(text=full_address)
                        
                        self.patient_details_widgets["Appointment Date:"].config(text=selected_date)
                        
                        # Use the time from the tree view or fall back to database value
                        time_string = selected_time if selected_time and selected_time != "N/A" else "-"
                        self.patient_details_widgets["Appointment Time:"].config(text=time_string)
                    
                    # Update prescription and comments
                    self.notes_text.delete("1.0", tk.END)
                    if record and record['prescription']:
                        self.notes_text.insert(tk.END, record['prescription'])
                    
                    self.prescription_text.delete("1.0", tk.END)
                    if record and record['comments']:
                        self.prescription_text.insert(tk.END, record['comments'])
                    
                    # Store current patient username
                    self.current_patient_username = patient_username
                    
                    # Update patient records
                    self.update_patient_records(patient_username)
                    
                    messagebox.showinfo("Information", f"Viewing completed appointment from {selected_date}")
                    
                except Error as e:
                    messagebox.showerror("Database Error", f"Error fetching appointment details: {e}")

    def fetch_patient_records(self, patient_username):
        """Fetch medical records history for a specific patient"""
        if not self.db_connection or not self.db_connection.is_connected():
            self.connect_to_database()
            if not self.db_connection.is_connected():
                return []
        
        try:
            cursor = self.db_connection.cursor(dictionary=True)
            query = """
            SELECT pr.d_name, pr.specialization, pr.appoint_date, dr.prescription, dr.comments
            FROM patient_records pr
            LEFT JOIN doc_replies dr ON pr.p_username = dr.username AND pr.appoint_date = dr.appoint_date
            WHERE pr.p_username = %s
            ORDER BY pr.appoint_date DESC
            """
            cursor.execute(query, (patient_username,))
            records = cursor.fetchall()
            cursor.close()
            return records
        except Error as e:
            messagebox.showerror("Database Error", f"Error fetching patient records: {e}")
            return []

    def patient_record_clicked(self, event):
        """Handle click on patient record row"""
        # Get the selected item
        selected_item = self.records_tree.focus()
        
        if selected_item:  # If an item is selected
            # Get the values from the selected item
            item_values = self.records_tree.item(selected_item, "values")
            selected_date = item_values[2]  # Date is the third column
            
            if self.current_patient_username and selected_date:
                # Convert string date back to datetime object
                try:
                    parsed_date = datetime.strptime(selected_date, "%b %d, %Y")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format")
                    return
                
                # Format date as it's stored in the database (ISO format)
                formatted_date = parsed_date.strftime("%Y-%m-%d")
                
                # Update the appointment date in the patient details section
                self.patient_details_widgets["Appointment Date:"].config(text=selected_date)
                # Set appointment time to "-" for historical records
                self.patient_details_widgets["Appointment Time:"].config(text="-")
                
                # No need to update other patient details as they remain the same for the current patient
                
                # Fetch prescription and comments for this specific date
                if not self.db_connection or not self.db_connection.is_connected():
                    self.connect_to_database()
                    if not self.db_connection.is_connected():
                        return
                
                try:
                    cursor = self.db_connection.cursor(dictionary=True)
                    
                    # Fetch prescription and comments for this specific date
                    query = """
                    SELECT prescription, comments
                    FROM doc_replies
                    WHERE username = %s AND appoint_date = %s
                    """
                    cursor.execute(query, (self.current_patient_username, formatted_date))
                    record = cursor.fetchone()
                    cursor.close()
                    
                    # Display prescription
                    self.notes_text.delete("1.0", tk.END)
                    if record and record['prescription']:
                        self.notes_text.insert(tk.END, record['prescription'])
                    
                    # Display comments
                    self.prescription_text.delete("1.0", tk.END)
                    if record and record['comments']:
                        self.prescription_text.insert(tk.END, record['comments'])
                    
                    messagebox.showinfo("Information", f"Viewing record from {selected_date}")
                    
                except Error as e:
                    messagebox.showerror("Database Error", f"Error fetching record details: {e}")

    
    def update_patient_records(self, patient_username):
        """Update the patient records treeview with data for the selected patient"""
        # Clear existing records
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        # Remove the default message if it exists
        if hasattr(self, 'records_label') and self.records_label.winfo_exists():
            self.records_label.pack_forget()
        
        # Fetch patient records
        records = self.fetch_patient_records(patient_username)
        
        if records:
            for record in records:
                date_string = record['appoint_date'].strftime("%b %d, %Y") if record['appoint_date'] else "N/A"
                
                # Insert record into treeview
                self.records_tree.insert("", "end", values=(
                    record['d_name'],
                    record['specialization'],
                    date_string
                ))
        else:
            # If no records, show a message
            if hasattr(self, 'records_label'):
                self.records_label.pack(pady=5)
                self.records_label.config(text="No medical history found for this patient")


if __name__ == "__main__":
    # Get command-line arguments
    doctor_username = "default_username"
    doctor_name = "Doctor"
    
    # Check if arguments were provided
    if len(sys.argv) > 1:
        doctor_username = sys.argv[1]
    if len(sys.argv) > 2:
        doctor_name = sys.argv[2]
    
    # Print for debugging
    print(f"Starting dashboard with username: {doctor_username}, name: {doctor_name}")
    
    # Start the application
    root = tk.Tk()
    app = DoctorDashboard(root, doctor_username, doctor_name)
    root.mainloop()