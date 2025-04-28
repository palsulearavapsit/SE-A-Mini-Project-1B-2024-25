import sys
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pymysql
import tkcalendar  # Make sure to install this with: pip install tkcalendar
from datetime import datetime
import subprocess  # For launching the userdashboard.py
import re  # For regular expression validation

class ProfileUpdateApp:
    def __init__(self, master, user_name=None,username=None):
        self.master = master
        self.username = username
        self.user_name = user_name
        master.title("Profile Update")
        master.geometry("1000x850")  # Increased width to accommodate medical records
        
        # Create main frame to hold both sections
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for profile details
        self.profile_frame = tk.Frame(self.main_frame, padx=10)
        self.profile_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Right frame for medical records
        self.medical_frame = tk.Frame(self.main_frame, padx=10, borderwidth=1, relief=tk.GROOVE)
        self.medical_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create and set up profile form fields in left frame
        self.create_profile_fields()

        # Load user data if username is provided
        if self.username:
            self.load_user_data()
        
        # Create medical records section in right frame
        self.create_medical_records_section()
        
        # Create buttons frame at the bottom
        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(pady=10, fill=tk.X)
        
        # Create back button that redirects to userdashboard.py
        back_button = tk.Button(
            self.buttons_frame, 
            text="Back to Dashboard", 
            command=self.back_to_user_dashboard,
            bg="#FF9800",
            fg="white",
            width=15
        )
        back_button.pack(side=tk.LEFT, padx=(100, 20))
        
        # Create submit button
        submit_button = tk.Button(
            self.buttons_frame, 
            text="Update Profile", 
            command=self.update_profile,
            bg="#4CAF50",
            fg="white",
            width=15
        )
        submit_button.pack(side=tk.LEFT, padx=20)
        
        # Create add medical record button
        add_record_button = tk.Button(
            self.buttons_frame, 
            text="Add Medical Record", 
            command=self.add_medical_record,
            bg="#2196F3",
            fg="white",
            width=15
        )
        add_record_button.pack(side=tk.LEFT, padx=20)

    def create_profile_fields(self):
        # Profile section title
        tk.Label(self.profile_frame, text="Profile Information", font=("Helvetica", 12, "bold")).pack(pady=(10,15))
        
        # Username
        tk.Label(self.profile_frame, text="Username").pack(pady=(10,0))
        self.username_var = tk.StringVar()
        self.username_var.set(self.username)
        self.username_entry = tk.Entry(self.profile_frame, width=30, textvariable=self.username_var, state='readonly')
        self.username_entry.pack(pady=5)
        
        # Name
        tk.Label(self.profile_frame, text="Name").pack(pady=(10,0))
        self.name_entry = tk.Entry(self.profile_frame, width=30)
        self.name_entry.pack(pady=5)

        # Phone Number
        tk.Label(self.profile_frame, text="Phone Number (10 digits)").pack(pady=(10,0))
        self.phone_entry = tk.Entry(self.profile_frame, width=30)
        self.phone_entry.pack(pady=5)

        # Email
        tk.Label(self.profile_frame, text="Email").pack(pady=(10,0))
        self.email_entry = tk.Entry(self.profile_frame, width=30)
        self.email_entry.pack(pady=5)
 
        # Date of Birth (with Calendar Button)
        tk.Label(self.profile_frame, text="Date of Birth").pack(pady=(10,0))
        
        # Frame to hold date of birth entry and calendar button
        dob_frame = tk.Frame(self.profile_frame)
        dob_frame.pack(pady=5)

        # Date of Birth Entry (Read-only)
        self.dob_entry = tk.Entry(dob_frame, width=20, state='readonly')
        self.dob_entry.pack(side=tk.LEFT, padx=(0,10))

        # Calendar Button
        calendar_button = tk.Button(
            dob_frame, 
            text="Select Date", 
            command=self.open_calendar
        )
        calendar_button.pack(side=tk.LEFT)

        # Age (Read-only)
        tk.Label(self.profile_frame, text="Age").pack(pady=(10,0))
        self.age_entry = tk.Entry(self.profile_frame, width=30, state='readonly')
        self.age_entry.pack(pady=5)

        # Address fields
        tk.Label(self.profile_frame, text="Address", font=("Helvetica", 10, "bold")).pack(pady=(10,0))

        # Building Details
        tk.Label(self.profile_frame, text="Building Details").pack(pady=(5,0))
        self.building_entry = tk.Entry(self.profile_frame, width=30)
        self.building_entry.pack(pady=2)

        # City
        tk.Label(self.profile_frame, text="City").pack(pady=(5,0))
        self.city_entry = tk.Entry(self.profile_frame, width=30)
        self.city_entry.pack(pady=2)

        # State
        tk.Label(self.profile_frame, text="State").pack(pady=(5,0))
        self.state_entry = tk.Entry(self.profile_frame, width=30)
        self.state_entry.pack(pady=2)

        # Pincode
        tk.Label(self.profile_frame, text="Pincode").pack(pady=(5,0))
        self.pincode_entry = tk.Entry(self.profile_frame, width=30)
        self.pincode_entry.pack(pady=2)

    def create_medical_records_section(self):
        # Medical records section title
        tk.Label(self.medical_frame, text="Previous Medical Records", font=("Helvetica", 12, "bold")).pack(pady=(10,15))
        
        # Doctor's Name
        tk.Label(self.medical_frame, text="Doctor's Name").pack(pady=(10,0))
        self.doctor_name_entry = tk.Entry(self.medical_frame, width=30)
        self.doctor_name_entry.pack(pady=5)
        
        # Doctor's Specialization
        tk.Label(self.medical_frame, text="Doctor's Specialization").pack(pady=(10,0))
        self.specialization_entry = tk.Entry(self.medical_frame, width=30)
        self.specialization_entry.pack(pady=5)
        
        # Appointment Date (with Calendar Button)
        tk.Label(self.medical_frame, text="Appointment Date").pack(pady=(10,0))
        
        # Frame to hold appointment date entry and calendar button
        appointment_frame = tk.Frame(self.medical_frame)
        appointment_frame.pack(pady=5)

        # Appointment Date Entry (Read-only)
        self.appointment_entry = tk.Entry(appointment_frame, width=20, state='readonly')
        self.appointment_entry.pack(side=tk.LEFT, padx=(0,10))

        # Calendar Button for appointment
        appointment_calendar_button = tk.Button(
            appointment_frame, 
            text="Select Date", 
            command=self.open_appointment_calendar
        )
        appointment_calendar_button.pack(side=tk.LEFT)
        
        # Prescription
        tk.Label(self.medical_frame, text="Prescription").pack(pady=(10,0))
        self.prescription_text = tk.Text(self.medical_frame, width=30, height=4)
        self.prescription_text.pack(pady=5)
        
        # Comments
        tk.Label(self.medical_frame, text="Comments").pack(pady=(10,0))
        self.comments_text = tk.Text(self.medical_frame, width=30, height=4)
        self.comments_text.pack(pady=5)
        
        # Display previous records
        self.load_previous_records()

    def load_previous_records(self):
        # Create a frame for displaying previous records
        records_frame = tk.Frame(self.medical_frame)
        records_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Label for previous records section
        tk.Label(records_frame, text="History", font=("Helvetica", 10, "bold")).pack(pady=(5,5))
        
        try:
            # Connect to database and fetch records
            connection = pymysql.connect(host='localhost',
                                        user='root',
                                        password='Drishti2005@',                                     
                                        database='medimate')
            cursor = connection.cursor()
            
            # Get patient records with proper JOIN on both username and appointment date
            cursor.execute("""
                SELECT pr.d_name, pr.specialization, pr.appoint_date, dr.prescription, dr.comments 
                FROM patient_records pr
                LEFT JOIN doc_replies dr ON pr.p_username = dr.username AND pr.appoint_date = dr.appoint_date
                WHERE pr.p_username = %s
                ORDER BY pr.appoint_date DESC
                LIMIT 3
            """, (self.username,))
            
            records = cursor.fetchall()
            connection.close()
            
            if records:
                # Create Treeview to display records
                columns = ("Doctor", "Specialization", "Date", "Prescription", "Comments")
                self.tree = ttk.Treeview(records_frame, columns=columns, show="headings", height=3)
                
                # Configure column headings
                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=70)
                
                # Add records to the tree
                for record in records:
                    formatted_date = record[2].strftime("%Y-%m-%d") if record[2] else "N/A"
                    self.tree.insert("", "end", values=(record[0], record[1], formatted_date, 
                                                record[3] if record[3] else "N/A", 
                                                record[4] if record[4] else "N/A"))
                
                self.tree.pack(fill=tk.BOTH, expand=True)
                
                # Add Delete Record button
                delete_button = tk.Button(
                    records_frame, 
                    text="Delete Selected Record", 
                    command=self.delete_medical_record,
                    bg="#F44336",
                    fg="white",
                    width=20
                )
                delete_button.pack(pady=10)
            else:
                tk.Label(records_frame, text="No previous records found").pack(pady=10)
                
        except Exception as e:
            tk.Label(records_frame, text=f"Error loading records: {str(e)}").pack(pady=10)

    def delete_medical_record(self):
        # Check if a record is selected
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
            
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this medical record?")
        if not confirm:
            return
            
        # Get the values of the selected item
        record_values = self.tree.item(selected_item, 'values')
        doctor_name = record_values[0]
        specialization = record_values[1]
        appointment_date = record_values[2]
        
        try:
            connection = pymysql.connect(host='localhost',
                                        user='root',
                                        password='Drishti2005@',                                     
                                        database='medimate')
            cursor = connection.cursor()
            
            # Delete from patient_records
            sql1 = """DELETE FROM patient_records 
                    WHERE p_username = %s 
                    AND d_name = %s 
                    AND specialization = %s 
                    AND appoint_date = %s"""
            cursor.execute(sql1, (
                self.username,
                doctor_name,
                specialization,
                appointment_date
            ))
            
            # Delete from doc_replies
            sql2 = """DELETE FROM doc_replies 
                    WHERE username = %s 
                    AND appoint_date = %s"""
            cursor.execute(sql2, (
                self.username,
                appointment_date
            ))
            
            connection.commit()
            connection.close()
            
            messagebox.showinfo("Success", "Medical record deleted successfully")
            
            # Completely recreate the medical records section
            # First destroy the current records display
            for widget in self.medical_frame.winfo_children():
                widget.destroy()
            
            # Recreate the medical records section
            self.create_medical_records_section()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete medical record: {str(e)}")

    def open_calendar(self):
        # Create a top-level window for the calendar
        top = tk.Toplevel(self.master)
        top.title("Select Date of Birth")
        
        # Create calendar widget
        cal = tkcalendar.Calendar(
            top, 
            selectmode='day',
            date_pattern='y-mm-dd',
        )
        cal.pack(padx=10, pady=10)

        def on_date_select():
            # Get selected date
            selected_date = cal.get_date()
            
            # Update date of birth entry
            self.dob_entry.config(state='normal')
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, selected_date)
            self.dob_entry.config(state='readonly')

            # Calculate and update age
            self.calculate_age()

            # Close the calendar window
            top.destroy()

        # Select Date Button
        select_button = tk.Button(
            top, 
            text="Select", 
            command=on_date_select
        )
        select_button.pack(pady=10)
    
    def open_appointment_calendar(self):
        # Create a top-level window for the calendar
        top = tk.Toplevel(self.master)
        top.title("Select Appointment Date")
        
        # Create calendar widget
        cal = tkcalendar.Calendar(
            top, 
            selectmode='day',
            date_pattern='y-mm-dd',
        )
        cal.pack(padx=10, pady=10)

        def on_date_select():
            # Get selected date
            selected_date = cal.get_date()
            
            # Update appointment date entry
            self.appointment_entry.config(state='normal')
            self.appointment_entry.delete(0, tk.END)
            self.appointment_entry.insert(0, selected_date)
            self.appointment_entry.config(state='readonly')

            # Close the calendar window
            top.destroy()

        # Select Date Button
        select_button = tk.Button(
            top, 
            text="Select", 
            command=on_date_select
        )
        select_button.pack(pady=10)
    
    def calculate_age(self):
        try:
            # Parse the date of birth
            dob = datetime.strptime(self.dob_entry.get(), "%Y-%m-%d")
            today = datetime.now()
            
            # Calculate age
            age = today.year - dob.year
            
            # Adjust age if birthday hasn't occurred this year
            if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
                age -= 1
            
            # Update age entry - store as integer without .0
            self.age_entry.config(state='normal')
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, str(int(age)))  # Convert to int to remove decimal
            self.age_entry.config(state='readonly')
        except ValueError:
            messagebox.showerror("Invalid Date", "Please select a valid date")
            self.dob_entry.config(state='normal')
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.config(state='readonly')
            self.age_entry.config(state='normal')
            self.age_entry.delete(0, tk.END)
            self.age_entry.config(state='readonly')

    def validate_email(self, email):
        # Regular expression pattern for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        # Check if phone number is exactly 10 digits
        return phone.isdigit() and len(phone) == 10

    def update_profile(self):
        # Collect form data
        profile_data = {
            "Name": self.name_entry.get(),
            "Phone Number": self.phone_entry.get(),
            "Email": self.email_entry.get(),
            "Date of Birth": self.dob_entry.get(),
            "Age": self.age_entry.get(),
            "Building Details": self.building_entry.get(),
            "City": self.city_entry.get(),
            "State": self.state_entry.get(),
            "Pincode": self.pincode_entry.get()
        }

        # Validate inputs
        required_fields = ["Name", "Phone Number", "Email", "Date of Birth", "Age"]
        if not all(profile_data[field] for field in required_fields):
            messagebox.showerror("Error", "Please fill in all required profile fields")
            return
            
        # Validate phone number (10 digits only)
        if not self.validate_phone(profile_data["Phone Number"]):
            messagebox.showerror("Invalid Phone", "Phone number must be exactly 10 digits")
            return
            
        # Validate email format
        if not self.validate_email(profile_data["Email"]):
            messagebox.showerror("Invalid Email", "Please enter a valid email address")
            return

        # Save to database
        try:
            connection = pymysql.connect(host='localhost',
                                        user='root',
                                        password='Drishti2005@',                                     
                                        database='medimate')
            cur = connection.cursor()
            sql = """UPDATE login 
                    SET name = %s, phone = %s, email = %s, dob = %s, age = %s, 
                    building_details = %s, city = %s, state = %s, pincode = %s 
                    WHERE username = %s"""
            cur.execute(sql, (
                profile_data["Name"],
                profile_data["Phone Number"], 
                profile_data["Email"], 
                profile_data["Date of Birth"], 
                int(profile_data["Age"]),  # Store as integer to fix .0 issue
                profile_data["Building Details"],
                profile_data["City"],
                profile_data["State"],
                profile_data["Pincode"],
                self.username
            ))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Profile Updated Successfully")
            self.master.destroy()
            from patientui import PatientProfile
            root = tk.Tk()
            app = PatientProfile(root, self.user_name, self.username)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

    def add_medical_record(self):
        # Collect medical record data
        medical_data = {
            "Doctor's Name": self.doctor_name_entry.get(),
            "Specialization": self.specialization_entry.get(),
            "Appointment Date": self.appointment_entry.get(),
            "Prescription": self.prescription_text.get("1.0", tk.END).strip(),
            "Comments": self.comments_text.get("1.0", tk.END).strip()
        }

        # Validate required fields
        if not medical_data["Doctor's Name"] or not medical_data["Specialization"] or not medical_data["Appointment Date"]:
            messagebox.showerror("Error", "Please fill in doctor's name, specialization, and appointment date")
            return

        # Save to database
        try:
            connection = pymysql.connect(host='localhost',
                                        user='root',
                                        password='Drishti2005@',                                     
                                        database='medimate')
            cursor = connection.cursor()
            
            # Insert into patient_records
            sql1 = """INSERT INTO patient_records 
                    (d_name, d_username, p_username, specialization, appoint_date) 
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql1, (
                medical_data["Doctor's Name"],
                '',  # d_username placeholder (empty for now)
                self.username,
                medical_data["Specialization"],
                medical_data["Appointment Date"]
            ))
            
            # Insert into doc_replies with the same appointment date
            sql2 = """INSERT INTO doc_replies 
                    (username, comments, prescription, appoint_date) 
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql2, (
                self.username,
                medical_data["Comments"],
                medical_data["Prescription"],
                medical_data["Appointment Date"]  # Use the same appointment date to link records
            ))
            
            connection.commit()
            connection.close()
            
            messagebox.showinfo("Success", "Medical record added successfully")
            
            # Clear form fields
            self.doctor_name_entry.delete(0, tk.END)
            self.specialization_entry.delete(0, tk.END)
            self.appointment_entry.config(state='normal')
            self.appointment_entry.delete(0, tk.END)
            self.appointment_entry.config(state='readonly')
            self.prescription_text.delete("1.0", tk.END)
            self.comments_text.delete("1.0", tk.END)
            
            # Completely recreate the medical records section
            # First destroy the current records display
            for widget in self.medical_frame.winfo_children():
                widget.destroy()
            
            # Recreate the medical records section
            self.create_medical_records_section()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add medical record: {str(e)}")

    def back_to_user_dashboard(self):
        # Close the current window
        self.master.destroy()
        from userdashboard import NavigationApp
        root = tk.Tk()
        if self.username:
            app = NavigationApp(root, self.user_name,self.username)
        else:
            app = NavigationApp(root)

    def refresh_medical_records(self):
        # Destroy all widgets in the records display area
        for widget in self.medical_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        # Reload previous records
        self.load_previous_records()

    def load_user_data(self):
        # Load user data from database after creating form fields
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Drishti2005@',
                database='medimate'
            )
            
            cursor = connection.cursor()
            query = """SELECT name, phone, email, dob, age, 
                    building_details, city, state, pincode 
                    FROM login WHERE username = %s"""
            cursor.execute(query, (self.username,))
            user_data = cursor.fetchone()
            connection.close()
            
            if user_data:
                # Populate form fields with user data
                self.name_entry.insert(0, user_data[0] if user_data[0] else "")
                self.phone_entry.insert(0, user_data[1] if user_data[1] else "")
                self.email_entry.insert(0, user_data[2] if user_data[2] else "")
                
                # Set date of birth
                if user_data[3]:
                    self.dob_entry.config(state='normal')
                    self.dob_entry.insert(0, user_data[3].strftime("%Y-%m-%d"))
                    self.dob_entry.config(state='readonly')
                    
                    # Set age - make sure it's an integer to avoid .0
                    self.age_entry.config(state='normal')
                    if user_data[4]:
                        self.age_entry.insert(0, str(int(user_data[4])))  # Convert to int to remove decimal
                    self.age_entry.config(state='readonly')
                
                # Set address fields
                self.building_entry.insert(0, user_data[5] if user_data[5] else "")
                self.city_entry.insert(0, user_data[6] if user_data[6] else "")
                self.state_entry.insert(0, user_data[7] if user_data[7] else "")
                self.pincode_entry.insert(0, user_data[8] if user_data[8] else "")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user data: {str(e)}")

def main():
    root = tk.Tk()
    app = ProfileUpdateApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()