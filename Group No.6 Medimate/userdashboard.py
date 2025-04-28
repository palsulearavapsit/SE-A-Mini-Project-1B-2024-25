import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, scrolledtext
from PIL import Image, ImageTk
import pymysql
from book_appointment import BookAppointment
from datetime import datetime

class NavigationApp:
    def __init__(self, root, user_name="User", username=""):
        self.root = root
        self.user_name = user_name
        self.username = username
        
        self.root.geometry("1280x853")
        self.root.title("User Dashboard")

        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Load background image
        self.background_image = PhotoImage(file=r"F:\MINIPROJECT\userdashbaord_image.png")
        
        # Create a label to hold the background image
        self.background_label = tk.Label(self.main_container, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
          
        # Create menu button (three lines)
        self.menu_frame = ttk.Frame(self.main_container)
        self.menu_frame.pack(anchor='ne', padx=10, pady=10)
        
        # Style configuration with thicker borders
        self.style = ttk.Style()
        self.style.configure('Thick.TLabelframe', borderwidth=0, relief='flat')

        # Welcome label
        welcome_label = tk.Label(self.main_container, text=f"Welcome, {self.user_name}!", 
                                background="white", font=("Helvetica", 30), anchor="center")
        welcome_label.place(relx=0.35, rely=0.10, anchor='center')
        
        # Left box - Appoint Doctor
        appoint_label = ttk.Label(self.main_container, text="Book Doctor Appointment", 
                                 background="#e1f0da", font=("Helvetica", 16), 
                                 anchor="center", borderwidth=2, relief="solid")
        appoint_label.place(relx=0.25, rely=0.25, anchor='center', width=250, height=50)
        
        # Bind click event to the appoint doctor label
        appoint_label.bind('<Button-1>', self.open_bookapp)

        # Lower Box - Book Medical Tests
        medtests_label = ttk.Label(self.main_container, text="Book Medical Tests", 
                                  background="#e1f0da", font=("Helvetica", 16),
                                  anchor="center", borderwidth=2, relief="solid")
        medtests_label.place(relx=0.25, rely=0.45, anchor='center', width=250, height=50)
        medtests_label.bind('<Button-1>', self.open_medtests)

        #booked details
        booked_label = ttk.Label(self.main_container, text="Booked History", 
                                  background="#e1f0da", font=("Helvetica", 16),
                                  anchor="center", borderwidth=2, relief="solid")
        booked_label.place(relx=0.25, rely=0.55, anchor='center', width=250, height=50)
        booked_label.bind('<Button-1>', self.open_booking_history)

        # View Profile
        profile_label = ttk.Label(self.main_container, text="View Profile", 
                                 background="#e1f0da", font=("Helvetica", 16),
                                 anchor="center", borderwidth=2, relief="solid")
        profile_label.place(relx=0.25, rely=0.75, anchor='center', width=250, height=50)
        profile_label.bind('<Button-1>', lambda event: self.open_patientui())

        # Logout
        logout_label = ttk.Label(self.main_container, text="Logout", 
                                background="#e1f0da", foreground="red", 
                                font=("Helvetica", 12), anchor="center", 
                                borderwidth=2, relief="solid")
        logout_label.place(relx=0.25, rely=0.85, anchor='center', width=250, height=50)
        logout_label.bind('<Button-1>', lambda event: self.open_login())

        # Last appointment section
        last_appointment_label = ttk.Label(self.main_container, text="Last Appointment", 
                                          background="#e1f0da", font=("Helvetica", 16),
                                          anchor="center", borderwidth=2, relief="solid")
        last_appointment_label.place(relx=0.75, rely=0.25, anchor='center', width=250, height=50)
        
        # Container for last appointment data
        self.last_appt_frame = tk.Frame(self.main_container, background="white", 
                                        borderwidth=1, relief="solid")
        self.last_appt_frame.place(relx=0.75, rely=0.37, anchor='center', 
                                  width=500, height=150)

        # Upcoming appointment section
        upcoming_appointment_label = ttk.Label(self.main_container, text="Upcoming Appointment", 
                                              background="#e1f0da", font=("Helvetica", 16),
                                              anchor="center", borderwidth=2, relief="solid")
        upcoming_appointment_label.place(relx=0.75, rely=0.55, anchor='center', width=250, height=50)
        
        # Container for upcoming appointment data
        self.upcoming_appt_frame = tk.Frame(self.main_container, background="white", 
                                           borderwidth=1, relief="solid")
        self.upcoming_appt_frame.place(relx=0.75, rely=0.72, anchor='center', 
                                      width=500, height=200)
        
        # Load and display appointment data
        self.load_appointments()

    def toggle_menu(self, event):
        # Display popup menu at button location
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup_menu.grab_release()

    def open_bookapp(self, event):
        self.root.destroy()
        new_root = tk.Tk() 
        # Pass the username and name to the BookAppointment class
        app = BookAppointment(new_root, self.username, self.user_name)
        new_root.mainloop()

    def open_login(self):
        self.root.destroy()  # Close login window
        from login import LoginPage
        login_page = LoginPage() 
        login_page.run()

    def open_patientui(self):
        self.root.destroy()
        from patientui import PatientProfile
        root = tk.Tk()
        app = PatientProfile(root, self.user_name, self.username)
        root.mainloop()
    
    def db_connection(self):
        """Establish a database connection"""
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="Drishti2005@",  
                database="medimate"
            )
            return connection
        except Exception as e:
            return None

    def load_appointments(self):
        """Load and display appointment information"""
        connection = self.db_connection()
        if not connection:
            # Display error message in frames
            for frame in [self.last_appt_frame, self.upcoming_appt_frame]:
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, text="Database connection error", bg="white", fg="red").pack(fill=tk.BOTH, expand=True)
            return
        
        try:
            cursor = connection.cursor()
            
            # Clear the last appointment frame
            for widget in self.last_appt_frame.winfo_children():
                widget.destroy()
                
            # Create headers for the last appointment table
            headers = ["Doctor", "Specialization", "Date", "Status"]
            for i, header in enumerate(headers):
                label = tk.Label(self.last_appt_frame, text=header, font=("Helvetica", 10, "bold"),
                                borderwidth=1, relief="solid", bg="#e1f0da", width=12)
                label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            
            # Configure grid weights for last appointment frame
            self.last_appt_frame.rowconfigure(0, weight=1)
            for i in range(len(headers)):
                self.last_appt_frame.columnconfigure(i, weight=1)
                
            # Get completed appointments from appointment table
            completed_query = """
            SELECT a.d_username, a.appoint_date, a.status 
            FROM appointment a
            WHERE a.p_username = %s AND a.status = 'completed'
            ORDER BY a.appoint_date DESC
            """
            cursor.execute(completed_query, (self.username,))
            completed_appointments = cursor.fetchall()
            
            # Get records from patient_records table
            records_query = """
            SELECT d_name, d_username, specialization, appoint_date 
            FROM patient_records
            WHERE p_username = %s
            ORDER BY appoint_date DESC
            """
            cursor.execute(records_query, (self.username,))
            patient_records = cursor.fetchall()
            
            # Combine and format the data for display
            last_appointments = []
            
            # Process completed appointments
            for appt in completed_appointments:
                doctor_username = appt[0]
                appt_date = appt[1]
                status = "Completed"
                
                # Look for matching specialization in patient_records
                specialization = "Unknown"
                for record in patient_records:
                    if record[1] == doctor_username and record[3] == appt_date:
                        specialization = record[2]
                        break
                
                # Get doctor's name either from record or by lookup
                doctor_name = None
                for record in patient_records:
                    if record[1] == doctor_username:
                        doctor_name = record[0]
                        break
                
                if not doctor_name:
                    doctor_name = self.get_doctor_name(doctor_username)
                
                # Format date
                formatted_date = appt_date.strftime('%Y-%m-%d') if appt_date else "N/A"
                
                last_appointments.append((doctor_name, specialization, formatted_date, status))
            
            # Add any additional records from patient_records that aren't in completed_appointments
            for record in patient_records:
                doctor_name = record[0]
                doctor_username = record[1]
                specialization = record[2]
                appt_date = record[3]
                
                # Format date
                formatted_date = appt_date.strftime('%Y-%m-%d') if appt_date else "N/A"
                
                # Check if this record is already included from completed_appointments
                is_duplicate = False
                for existing_appt in last_appointments:
                    if (existing_appt[0] == doctor_name and 
                        existing_appt[2] == formatted_date):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    last_appointments.append((doctor_name, specialization, formatted_date, "Completed"))
            
            # Sort by date in descending order (newest first)
            last_appointments.sort(key=lambda x: x[2], reverse=True)
            
            # Display the last appointments (up to 5)
            if last_appointments:
                for row_idx, appt in enumerate(last_appointments[:5], start=1):
                    for col_idx, data in enumerate(appt):
                        label = tk.Label(self.last_appt_frame, text=data, font=("Helvetica", 10),
                                        borderwidth=1, relief="solid", bg="white")
                        label.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                    
                    # Configure row weight
                    self.last_appt_frame.rowconfigure(row_idx, weight=1)
            else:
                # No last appointment
                no_data = tk.Label(self.last_appt_frame, text="No completed appointments", 
                                  font=("Helvetica", 12), bg="white")
                no_data.grid(row=1, column=0, columnspan=len(headers), sticky="nsew")
                self.last_appt_frame.rowconfigure(1, weight=1)
            
            # Fetch upcoming appointments
            upcoming_query = """
            SELECT a.d_username, a.appoint_date, a.appoint_time, a.status 
            FROM appointment a
            WHERE a.p_username = %s AND a.status != 'completed'
            ORDER BY a.appoint_date ASC
            """
            cursor.execute(upcoming_query, (self.username,))
            upcoming_appointments = cursor.fetchall()
            
            # Clear the upcoming appointment frame
            for widget in self.upcoming_appt_frame.winfo_children():
                widget.destroy()
                
            # Create headers for the upcoming appointment table
            headers = ["Doctor", "Specialization", "Date", "Time", "Status"]
            for i, header in enumerate(headers):
                label = tk.Label(self.upcoming_appt_frame, text=header, font=("Helvetica", 10, "bold"),
                                borderwidth=1, relief="solid", bg="#e1f0da", width=10)
                label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)
            
            # Configure grid weights for upcoming appointment frame
            self.upcoming_appt_frame.rowconfigure(0, weight=1)
            for i in range(len(headers)):
                self.upcoming_appt_frame.columnconfigure(i, weight=1)
            
            # Display upcoming appointments
            if upcoming_appointments:
                for row_idx, appt in enumerate(upcoming_appointments[:5], start=1):
                    doctor_username = appt[0]
                    appt_date = appt[1]
                    appt_time = appt[2]
                    status = appt[3].capitalize()
                    
                    # Get doctor's name
                    doctor_name = self.get_doctor_name(doctor_username)
                    
                    # Get specialization
                    specialization = self.get_doctor_specialization(doctor_username)
                    
                    # Format date
                    formatted_date = appt_date.strftime('%Y-%m-%d') if appt_date else "N/A"
                    
                    # Create row data
                    row_data = [doctor_name, specialization, formatted_date, appt_time, status]
                    
                    # Add to table
                    for col_idx, data in enumerate(row_data):
                        label = tk.Label(self.upcoming_appt_frame, text=data, font=("Helvetica", 10),
                                        borderwidth=1, relief="solid", bg="white")
                        label.grid(row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1)
                    
                    # Configure row weight
                    self.upcoming_appt_frame.rowconfigure(row_idx, weight=1)
            else:
                # No upcoming appointments
                no_data = tk.Label(self.upcoming_appt_frame, text="No upcoming appointments", 
                                  font=("Helvetica", 12), bg="white")
                no_data.grid(row=1, column=0, columnspan=len(headers), sticky="nsew")
                self.upcoming_appt_frame.rowconfigure(1, weight=1)
            
            cursor.close()
            
        except Exception as e:
            # Show error message in frames
            for widget in self.last_appt_frame.winfo_children():
                widget.destroy()
            for widget in self.upcoming_appt_frame.winfo_children():
                widget.destroy()
                
            error_label1 = tk.Label(self.last_appt_frame, text=f"Error loading data: {e}", 
                                   font=("Helvetica", 12), bg="white", fg="red")
            error_label1.pack(expand=True, fill=tk.BOTH)
            
            error_label2 = tk.Label(self.upcoming_appt_frame, text=f"Error loading data: {e}", 
                                   font=("Helvetica", 12), bg="white", fg="red")
            error_label2.pack(expand=True, fill=tk.BOTH)
        finally:
            if connection:
                connection.close()
    
    def get_doctor_name(self, doctor_username):
        """Get doctor's name from username"""
        connection = self.db_connection()
        if not connection:
            return "Unknown Doctor"
        
        try:
            cursor = connection.cursor()
            query = "SELECT name FROM doc_info WHERE username = %s"
            cursor.execute(query, (doctor_username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                return result[0]
            else:
                return "Unknown Doctor"
        except Exception as e:
            if connection:
                connection.close()
            return "Unknown Doctor"

    def get_doctor_specialization(self, doctor_username):
        """Get doctor's specialization from username"""
        connection = self.db_connection()
        if not connection:
            return "Unknown"
        
        try:
            cursor = connection.cursor()
            query = "SELECT specialization FROM doc_info WHERE username = %s"
            cursor.execute(query, (doctor_username,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                return result[0]
            else:
                return "Unknown"
        except Exception as e:
            if connection:
                connection.close()
            return "Unknown"
        
    def open_medtests(self,event):
        # Close the current window and open the MedicalTestsApp
        self.root.destroy()
        new_root = tk.Tk()
        from medicaltest import MedimateBookingSystem
        app = MedimateBookingSystem(new_root, self.user_name, self.username)
        new_root.mainloop()

    def open_booking_history(self, event):
        """Open the medical booking history window"""
        self.root.destroy()
        new_root = tk.Tk()
        from booking_history import BookingHistory
        app = BookingHistory(new_root, self.user_name, self.username)
        new_root.mainloop()


def main():
    root = tk.Tk()
    # IMPORTANT: Pass actual username here for testing
    app = NavigationApp(root, "Test User", "test_username")
    root.mainloop()

if __name__ == "__main__":
    main()