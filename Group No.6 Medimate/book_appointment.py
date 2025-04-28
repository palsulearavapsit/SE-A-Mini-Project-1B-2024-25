import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import pymysql
from tkcalendar import Calendar
from datetime import datetime

class BookAppointment:
    def __init__(self, root, p_username, p_name):
        self.root = root
        self.root.title("Doctor Selection")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        
        self.p_username = p_username
        self.p_name = p_name  # Add patient name parameter
        
        # Initialize doctor data - only Indian doctors
        self.doctors = [
            {"id": 1, "name": "Dr. Aisha Patel", "username": "aishapatel", "specialization": "Cardiology", "experience": 15, "availability": "Mon, Wed, Fri"},
            {"id": 5, "name": "Dr. Raj Kumar", "username": "rajkumar", "specialization": "Cardiology", "experience": 18, "availability": "Mon to Sat"},
            {"id": 6, "name": "Dr. Priya Sharma", "username": "priyasharma", "specialization": "Endocrinology", "experience": 11, "availability": "Tue, Thu, Sat"},
            {"id": 10, "name": "Dr. Vikram Desai", "username": "vikramdesai", "specialization": "Neurology", "experience": 17, "availability": "Mon, Wed, Fri"},
            {"id": 11, "name": "Dr. Neha Gupta", "username": "nehagupta", "specialization": "Pediatrics", "experience": 8, "availability": "Mon to Fri"},
            {"id": 12, "name": "Dr. Suresh Mehta", "username": "sureshmehta", "specialization": "Orthopedics", "experience": 20, "availability": "Wed, Thu, Sat"},
            {"id": 13, "name": "Dr. Ananya Reddy", "username": "ananyareddy", "specialization": "Dermatology", "experience": 10, "availability": "Mon, Tue, Fri"},
            {"id": 14, "name": "Dr. Sanjay Patel", "username": "sanjaypatel", "specialization": "Psychiatry", "experience": 16, "availability": "Mon, Wed, Fri"},
            {"id": 15, "name": "Dr. Kavita Verma", "username": "kavitaverma", "specialization": "Ophthalmology", "experience": 9, "availability": "Mon to Thu"},
            {"id": 16, "name": "Dr. Arjun Singh", "username": "arjunsingh", "specialization": "Pediatrics", "experience": 22, "availability": "Mon, Wed, Fri"}
        ]
        
        # Data storage for appointments
        self.appointments = []
        if os.path.exists("doctor_appointments.json"):
            try:
                with open("doctor_appointments.json", "r") as file:
                    self.appointments = json.load(file)
            except:
                pass
        
        # Get unique specializations
        self.specializations = sorted(list(set(doc["specialization"] for doc in self.doctors)))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create header
        header_frame = tk.Frame(self.root, bg="#28a745", height=80)
        header_frame.pack(fill=tk.X)
        
        # Add green border around the entire window
        border_frame = tk.Frame(self.root, bg="#28a745", padx=2, pady=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_frame = tk.Frame(border_frame, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header content - only title, no logo
        title_label = tk.Label(header_frame, text="Doctor Selection", 
                             font=("Arial", 24, "bold"), bg="#28a745", fg="white")
        title_label.pack(pady=20)
        
        # Filter frame
        filter_frame = tk.Frame(main_frame, bg="white", pady=10)
        filter_frame.pack(fill=tk.X, padx=20)
        
        # Specialization filter
        tk.Label(filter_frame, text="Specialization:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.specialization_var = tk.StringVar(value="All")
        specialization_combo = ttk.Combobox(filter_frame, textvariable=self.specialization_var, font=("Arial", 12), width=20, state="readonly")
        specialization_combo["values"] = ["All"] + self.specializations
        specialization_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        specialization_combo.bind("<<ComboboxSelected>>", self.filter_doctors)
        
        # Experience filter
        tk.Label(filter_frame, text="Min. Experience (years):", font=("Arial", 14), bg="white").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.experience_var = tk.StringVar(value="0")
        experience_combo = ttk.Combobox(filter_frame, textvariable=self.experience_var, font=("Arial", 12), width=10, state="readonly")
        experience_combo["values"] = ["0", "5", "10", "15", "20"]
        experience_combo.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        experience_combo.bind("<<ComboboxSelected>>", self.filter_doctors)
        
        # Apply filter button
        filter_button = tk.Button(filter_frame, text="Apply Filters", command=self.filter_doctors, 
                               bg="#28a745", fg="white", font=("Arial", 12), padx=10)
        filter_button.grid(row=0, column=4, padx=20, pady=10, sticky="w")
        
        # Doctor list frame
        list_frame = tk.Frame(main_frame, bg="white", bd=1, relief=tk.SOLID)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Table headers - removed ID column
        columns = ("Name", "Specialization", "Experience", "Availability")
        self.doctor_table = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Define column widths - adjusted after removing ID column
        self.doctor_table.column("Name", width=250, anchor="w")
        self.doctor_table.column("Specialization", width=200, anchor="w")
        self.doctor_table.column("Experience", width=150, anchor="center")
        self.doctor_table.column("Availability", width=250, anchor="w")
        
        # Define column headings
        for col in columns:
            self.doctor_table.heading(col, text=col)
            
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.doctor_table.yview)
        self.doctor_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.doctor_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Select doctor and appointment details frame
        selection_frame = tk.Frame(main_frame, bg="white", pady=15)
        selection_frame.pack(fill=tk.X, padx=20)
        
        # Selected doctor info
        tk.Label(selection_frame, text="Selected Doctor:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.selected_doctor_var = tk.StringVar(value="None selected")
        tk.Label(selection_frame, textvariable=self.selected_doctor_var, font=("Arial", 14, "bold"), bg="white", fg="#28a745").grid(row=0, column=1, padx=10, pady=5, sticky="w", columnspan=2)
        
        # Date selection with calendar
        tk.Label(selection_frame, text="Date:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(selection_frame, textvariable=self.date_var, font=("Arial", 14), width=15, state="readonly")
        self.date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        calendar_button = tk.Button(selection_frame, text="Select Date", command=self.show_calendar, 
                                  bg="#28a745", fg="white", font=("Arial", 12))
        calendar_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        # Time selection
        tk.Label(selection_frame, text="Time:", font=("Arial", 14), bg="white").grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.time_var = tk.StringVar()
        self.time_combo = ttk.Combobox(selection_frame, textvariable=self.time_var, font=("Arial", 12), width=15, state="readonly")
        self.time_combo["values"] = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
        self.time_combo.grid(row=1, column=4, padx=10, pady=5, sticky="w")
        
        # Book appointment and Cancel buttons in the same frame
        button_frame = tk.Frame(main_frame, bg="white", pady=20)
        button_frame.pack()
        
        # Add Book Appointment button
        book_button = tk.Button(button_frame, text="Book Appointment", command=self.book_appointment, 
                               bg="white", fg="#28a745", font=("Arial", 14, "bold"),
                               width=20, relief=tk.SOLID, bd=1)
        book_button.pack(side=tk.LEFT, padx=10)
        
        # Add Cancel button
        cancel_button = tk.Button(button_frame, text="Back To Dashboard", command=self.open_userashboard, 
                                bg="white", fg="#dc3545", font=("Arial", 14, "bold"),
                                width=20, relief=tk.SOLID, bd=1)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Bind selection event
        self.doctor_table.bind("<<TreeviewSelect>>", self.on_doctor_select)
        
        # Load initial doctors
        self.load_doctors()
        
    def show_calendar(self):
        # Create a calendar dialog
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Select Date")
        cal_window.geometry("300x300")
        cal_window.resizable(False, False)
        
        today = datetime.now()
        cal = Calendar(cal_window, selectmode='day', year=today.year, month=today.month, day=today.day)
        cal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        def get_date():
            selected_date = cal.get_date()
            # Convert from MM/DD/YY to YYYY-MM-DD
            date_parts = selected_date.split('/')
            if len(date_parts) == 3:
                month, day, year = date_parts
                if len(year) == 2:
                    year = f"20{year}"
                formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                self.date_var.set(formatted_date)
            cal_window.destroy()
        
        select_button = tk.Button(cal_window, text="Select", command=get_date, 
                                bg="#28a745", fg="white", font=("Arial", 12), width=10)
        select_button.pack(pady=10)
        
    def load_doctors(self):
        # Clear existing items
        for item in self.doctor_table.get_children():
            self.doctor_table.delete(item)
            
        # Add all doctors - removed ID column
        for doc in self.doctors:
            self.doctor_table.insert("", "end", values=(
                doc["name"],
                doc["specialization"],
                f"{doc['experience']} years",
                doc["availability"]
            ))
    
    def filter_doctors(self, event=None):
        # Get filter values
        specialization = self.specialization_var.get()
        min_experience = int(self.experience_var.get())
        
        # Clear existing items
        for item in self.doctor_table.get_children():
            self.doctor_table.delete(item)
            
        # Filter and add doctors - removed ID column
        for doc in self.doctors:
            if (specialization == "All" or doc["specialization"] == specialization) and doc["experience"] >= min_experience:
                self.doctor_table.insert("", "end", values=(
                    doc["name"],
                    doc["specialization"],
                    f"{doc['experience']} years",
                    doc["availability"]
                ))
    
    def on_doctor_select(self, event):
        selected_items = self.doctor_table.selection()
        if selected_items:
            item = selected_items[0]
            values = self.doctor_table.item(item, "values")
            doctor_name = values[0]  # Extract doctor's name
            self.selected_doctor_var.set(doctor_name)
            
            # Store doctor name in a variable
            self.doctor_name = doctor_name  # <-- Store doctor's name

            # Find the doctor ID and username from the name
            for doc in self.doctors:
                if doc["name"] == doctor_name:
                    self.selected_doctor_id = doc["id"]
                    self.selected_doctor_username = doc["username"]  # Store the username
                    break
    
    def book_appointment(self):
        # Check if doctor is selected
        if not hasattr(self, "selected_doctor_id"):
            messagebox.showerror("Error", "Please select a doctor")
            return
            
        # Get appointment details
        date = self.date_var.get().strip()
        time = self.time_var.get()
            
        if not date or not time:
            messagebox.showerror("Error", "Please select appointment date and time")
            return
            
        # Get selected doctor
        doctor = next((doc for doc in self.doctors if doc["id"] == self.selected_doctor_id), None)
        if not doctor:
            messagebox.showerror("Error", "Invalid doctor selection")
            return
            
        # Create appointment
        appointment = {
            "doctor_id": self.selected_doctor_id,
            "doctor_name": doctor["name"],
            "doctor_username": doctor["username"],  # Add doctor username
            "patient_username": self.p_username,
            "patient_name": self.p_name,  # Add patient name
            "specialization": doctor["specialization"],
            "date": date,
            "time": time,
            "status": "requested"
        }
        
        # Save appointment to JSON file
        self.appointments.append(appointment)
        with open("doctor_appointments.json", "w") as file:
            json.dump(self.appointments, file, indent=4)
            
        # Insert appointment into MySQL database
        connection = None
        try:
            # Establish a database connection
            connection = pymysql.connect(
                host='localhost',
                database='medimate',
                user='root',
                password='Drishti2005@'
            )
            cursor = connection.cursor()
            
            # Prepare the SQL query with correct parameters
            sql_insert_query = "INSERT INTO appointment (d_username, p_username, p_name, appoint_date, appoint_time) VALUES (%s, %s, %s, %s, %s)"
            
            # Execute the query with all required parameters
            cursor.execute(sql_insert_query, (
                self.selected_doctor_username,  # d_username
                self.p_username,                # p_username
                self.p_name,                    # p_name
                date,                           # appoint_date
                time                            # appoint_time
            ))
            
            connection.commit()
        
        except Exception as e:
            messagebox.showerror("Database Error", f"Error while connecting to MySQL: {e}")
        
        finally:
            if connection:
                connection.close()
        
        # Show success message
        details = f"Doctor: {doctor['name']}\n"
        details += f"Specialization: {doctor['specialization']}\n"
        details += f"Experience: {doctor['experience']} years\n"
        details += f"Date: {date}\n"
        details += f"Time: {time}"
        
        messagebox.showinfo("Appointment Requested!", 
                        f"Your appointment has been requested successfully!\n\nDETAILS:\n{details}")
        
        # Clear form
        self.clear_form()
        
    def open_userashboard(self):
        self.root.destroy()
        # Run the user dashboard script
        from userdashboard import NavigationApp
        root = tk.Tk()
        app = NavigationApp(root,self.p_name,self.p_username)  # Pass patient name and username
        root.mainloop()

    def clear_form(self):
        self.date_var.set("")
        self.time_var.set("")
        self.selected_doctor_var.set("None selected")
        if hasattr(self, "selected_doctor_id"):
            delattr(self, "selected_doctor_id")
        if hasattr(self, "selected_doctor_username"):
            delattr(self, "selected_doctor_username")
        
        # Clear selection in treeview
        self.doctor_table.selection_remove(self.doctor_table.selection())

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = BookAppointment(root, "patient_username", "Patient Name")  # Example values
    root.mainloop()