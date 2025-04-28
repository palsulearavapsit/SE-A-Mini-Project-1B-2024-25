# Hey there! This is our user profile page for the EV charging station app.
# It lets users manage their account, view bookings, and handle memberships.
# Last updated: January 2024

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import random

# Our app's color scheme - keeping it fresh and modern
COLORS = {
    'primary': "#4CAF50",    # Green for main actions
    'secondary': "#2b2b2b",  # Dark theme background
    'accent': "#d77337",     # Orange pop for highlights
    'text_light': "#ffffff", # White text that stands out
    'text_dark': "#333333",  # Easy to read dark text
    'warning': "#FFA500",    # Yellow for alerts
    'error': "#FF0000",      # Red for critical stuff
    'success': "#28a745",    # Green for success messages
    'card_bg': "#ffffff"     # Clean white backgrounds
}

# Font settings to keep everything looking consistent
STYLES = {
    'title': ('Arial', 24, 'bold'),    # Big headers
    'subtitle': ('Arial', 18),         # Section titles
    'button': ('Arial', 16),           # Nice clickable buttons
    'text': ('Arial', 14),             # Regular text
    'small_text': ('Arial', 12)        # Small details
}

# Database connection settings - might want to move this to a config file later
DB_CONFIG = {
    'host': "127.0.0.1",
    'user': "root",
    'password': "Shardul203",  # Remember to change in production!
    'database': "ev_station"
}

class ProfilePage:
    def __init__(self, root, username):
        # Set up our main window and keep track of who's logged in
        self.root = root
        self.username = username
        self.user_data = None
        
        # Make it look nice and responsive
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')  # Start maximized
        self.root.title("User Profile")
        self.root.config(bg=COLORS['secondary'])
        
        # Main container for all our content
        self.container = tk.Frame(self.root, bg=COLORS['secondary'])
        self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Load up the user's profile
        self.refresh_profile()

    def get_user_data(self):
        # Grab the user's info from our database
        try:
            with mysql.connector.connect(**DB_CONFIG) as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # First, make sure the user exists
                    cursor.execute("SELECT id FROM users WHERE username = %s", 
                                 (self.username,))
                    user_result = cursor.fetchone()
                    
                    if not user_result:
                        # Create a new user if they don't exist yet
                        cursor.execute("INSERT INTO users (username) VALUES (%s)",
                                     (self.username,))
                        conn.commit()
                        cursor.execute("SELECT id FROM users WHERE username = %s",
                                     (self.username,))
                        user_result = cursor.fetchone()
                    
                    user_id = user_result['id']
                    
                    # Now get their profile data
                    cursor.execute("SELECT * FROM user_profiles WHERE user_id = %s",
                                 (user_id,))
                    user_data = cursor.fetchone()
                    
                    if not user_data:
                        # Set up a new profile if they don't have one
                        cursor.execute("""
                            INSERT INTO user_profiles 
                            (user_id, username, email, is_member) 
                            VALUES (%s, %s, %s, FALSE)
                        """, (user_id, self.username, None))
                        conn.commit()
                        
                        cursor.execute("SELECT * FROM user_profiles WHERE user_id = %s",
                                     (user_id,))
                        user_data = cursor.fetchone()
                    
                    return user_data
                    
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            return {'username': self.username}

    def refresh_profile(self):
        # Clear existing widgets
        for widget in self.container.winfo_children():
            widget.destroy()

        # Get fresh user data and recreate profile view
        self.user_data = self.get_user_data()
        self.create_profile_view()

    def create_profile_view(self):
        # Profile Header
        header_frame = tk.Frame(self.container, bg=COLORS['card_bg'], padx=20, pady=20)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Welcome message with username
        tk.Label(
            header_frame,
            text=f"Welcome, {self.username}!",
            font=STYLES['title'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(side=tk.LEFT)

        # Modify membership badge to show duration
        if self.user_data.get('is_member'):
            membership_frame = tk.Frame(header_frame, bg=COLORS['warning'], padx=10, pady=5)
            membership_frame.pack(side=tk.RIGHT)
            
            tk.Label(
                membership_frame,
                text="Premium Member",
                font=STYLES['subtitle'],
                bg=COLORS['warning'],
                fg=COLORS['text_dark']
            ).pack()
            
            # Add membership duration
            if self.user_data.get('membership_end_date'):
                end_date = datetime.strptime(str(self.user_data['membership_end_date']), '%Y-%m-%d')
                days_left = (end_date - datetime.now()).days
                
                tk.Label(
                    membership_frame,
                    text=f"Valid until: {end_date.strftime('%d %b %Y')}\n{days_left} days remaining",
                    font=STYLES['small_text'],
                    bg=COLORS['warning'],
                    fg=COLORS['text_dark']
                ).pack()

        # Profile Content
        content_frame = tk.Frame(self.container, bg=COLORS['card_bg'], padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Profile Information
        self.create_profile_info(content_frame)

        # Add Booking History Section
        history_frame = tk.Frame(self.container, bg=COLORS['card_bg'], padx=20, pady=20)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        tk.Label(
            history_frame,
            text="Booking History",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 10))

        self.create_booking_history(history_frame)

        # Buttons Frame
        button_frame = tk.Frame(content_frame, bg=COLORS['card_bg'])
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Edit Profile",
            font=STYLES['button'],
            bg=COLORS['accent'],
            fg=COLORS['text_light'],
            command=self.edit_profile
        ).pack(side=tk.LEFT, padx=10)

        if not self.user_data.get('is_member'):
            tk.Button(
                button_frame,
                text="Buy Membership",
                font=STYLES['button'],
                bg=COLORS['primary'],
                fg=COLORS['text_light'],
                command=self.buy_membership
            ).pack(side=tk.LEFT, padx=10)

        # Add Exit Button
        tk.Button(
            button_frame,
            text="Exit",
            font=STYLES['button'],
            bg=COLORS['error'],
            fg=COLORS['text_light'],
            command=self.root.destroy
        ).pack(side=tk.LEFT, padx=10)

    def create_profile_info(self, parent):
        info_frame = tk.Frame(parent, bg=COLORS['card_bg'])
        info_frame.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("Username", self.user_data.get('username', '')),
            ("Phone", self.user_data.get('phone_number', 'Not set')),
            ("Email", self.user_data.get('email', 'Not set')),
            ("Date of Birth", self.user_data.get('date_of_birth', 'Not set')),
            ("Country", self.user_data.get('country', 'Not set')),
            ("City", self.user_data.get('city', 'Not set')),
            ("Membership Status", "Premium Member" if self.user_data.get('is_member') else "Non-Member"),
        ]

        #if self.user_data.get('is_member'):
           # fields.append(("Member Since", self.user_data.get('membership_date', 'Not available')))

        for label, value in fields:
            field_frame = tk.Frame(info_frame, bg=COLORS['card_bg'])
            field_frame.pack(fill=tk.X, pady=5)

            tk.Label(
                field_frame,
                text=label,
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['text_dark'],
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)

            tk.Label(
                field_frame,
                text=str(value),
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['accent']
            ).pack(side=tk.LEFT, padx=10)

    def create_booking_history(self, parent):
        # Create a frame for the history table
        table_frame = tk.Frame(parent, bg=COLORS['card_bg'])
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Modified columns to match what we have in the database
        columns = ('Date', 'Time', 'Station Name', 'Price', 'Status')  # Removed Bill Number
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # Configure column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)  # Adjust width as needed

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Pack the tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Fetch and display booking history
        self.load_booking_history(tree)

    def load_booking_history(self, tree):
        try:
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Shardul203",
                database="ev_station"
            )
            cursor = conn.cursor()

            # Get user_id
            cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
            user_result = cursor.fetchone()
            if not user_result:
                # Don't show error message, just return silently
                cursor.close()
                conn.close()
                return
            user_id = user_result[0]

            # Simplified query that only uses tables and columns we know exist
            query = """
            SELECT
                b.booking_date,
                b.time_slot,
                s.name AS station_name,
                b.price,
                CASE
                    WHEN b.booking_date >= CURDATE() THEN 'Upcoming'
                    ELSE 'Completed'
                END as status
            FROM bookings b
            JOIN stations s ON b.station_id = s.station_id
            WHERE b.user_id = %s
            ORDER BY b.booking_date DESC, b.time_slot DESC
            """
            cursor.execute(query, (user_id,))
            bookings = cursor.fetchall()

            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)

            # Insert bookings into tree
            if bookings:
                for booking in bookings:
                    tree.insert('', 'end', values=booking)

            cursor.close()
            conn.close()

        except mysql.connector.Error:
            # Silently handle database errors without showing error messages
            pass
        except Exception:
            # Silently handle any other errors without showing error messages
            pass

    def view_bill_details(self, bill_number):
        # Since we're not showing bill numbers anymore, this method won't be called
        pass

    def show_bill_window(self, bill_data):
        # Since we're not showing bills anymore, this method won't be called
        pass

    def edit_profile(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("500x600")
        edit_window.config(bg=COLORS['card_bg'])

        tk.Label(
            edit_window,
            text="Edit Profile",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(pady=20)

        # Create entry fields
        entries = {}
        fields = [
            ("Phone Number", 'phone_number'),
            ("Email", 'email'),
            ("Date of Birth (YYYY-MM-DD)", 'date_of_birth'),
            ("Country", 'country'),
            ("City", 'city')
        ]

        for label, key in fields:
            frame = tk.Frame(edit_window, bg=COLORS['card_bg'])
            frame.pack(fill=tk.X, padx=20, pady=5)

            tk.Label(
                frame,
                text=label,
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['text_dark']
            ).pack(anchor='w')

            entry = tk.Entry(frame, font=STYLES['text'])
            current_value = self.user_data.get(key, '')
            if current_value is not None:
                entry.insert(0, str(current_value))
            entries[key] = entry
            entry.pack(fill=tk.X, pady=5)

        def save_changes():
            try:
                conn = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="Shardul203",
                    database="ev_station"
                )
                cursor = conn.cursor()

                # First get user_id
                cursor.execute("SELECT id FROM users WHERE username = %s", (self.username,))
                user_result = cursor.fetchone()
                if not user_result:
                    raise Exception("User not found")
                
                user_id = user_result[0]

                # Handle date format
                date_of_birth = entries['date_of_birth'].get()
                if date_of_birth and date_of_birth != 'Not set':
                    try:
                        # Validate date format
                        datetime.strptime(date_of_birth, '%Y-%m-%d')
                    except ValueError:
                        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                        return
                else:
                    date_of_birth = None

                # Modified update query with proper column names
                update_query = """
                    UPDATE user_profiles
                    SET 
                        username = %s,
                        email = %s,
                        date_of_birth = %s,
                        country = %s,
                        city = %s
                    WHERE user_id = %s
                """
                
                values = (
                    self.username,
                    entries['email'].get() or None,
                    date_of_birth,
                    entries['country'].get() or None,
                    entries['city'].get() or None,
                    user_id
                )
                
                cursor.execute(update_query, values)
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Profile updated successfully!")
                edit_window.destroy()
                self.refresh_profile()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

        tk.Button(
            edit_window,
            text="Save Changes",
            font=STYLES['button'],
            bg=COLORS['primary'],
            fg=COLORS['text_light'],
            command=save_changes
        ).pack(pady=20)

    def buy_membership(self):
        if messagebox.askyesno("Membership", "Would you like to purchase a membership for ₹1000?"):
            try:
                conn = mysql.connector.connect(
                    host="127.0.0.1",
                    user="root",
                    password="Shardul203",
                    database="ev_station"
                )
                cursor = conn.cursor()

                # Update user profile with membership dates
                current_date = datetime.now().date()
                end_date = current_date.replace(year=current_date.year + 1)
                
                cursor.execute("""
                    UPDATE user_profiles
                    SET 
                        is_member = TRUE, 
                        membership_start_date = %s,
                        membership_end_date = %s
                    WHERE username = %s
                """, (current_date, end_date, self.username))

                conn.commit()
                cursor.close()
                conn.close()

                self.show_receipt()
                self.refresh_profile()

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to process membership: {str(e)}")

    def show_receipt(self):
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Membership Receipt")
        receipt_window.geometry("400x500")
        receipt_window.config(bg=COLORS['card_bg'])

        receipt_frame = tk.Frame(receipt_window, bg=COLORS['card_bg'], padx=20, pady=20)
        receipt_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            receipt_frame,
            text="Membership Receipt",
            font=STYLES['subtitle'],
            bg=COLORS['card_bg'],
            fg=COLORS['text_dark']
        ).pack(pady=(0, 20))

        details = [
            ("Receipt No:", f"MEM{random.randint(10000,99999)}"),
            ("Date:", datetime.now().strftime("%Y-%m-%d")),
            ("Username:", self.username),
            ("Amount Paid:", "₹1000"),
            ("Membership Status:", "Active"),
            ("Valid Until:", (datetime.now().replace(year=datetime.now().year + 1)).strftime("%Y-%m-%d"))
        ]

        for label, value in details:
            detail_frame = tk.Frame(receipt_frame, bg=COLORS['card_bg'])
            detail_frame.pack(fill=tk.X, pady=5)

            tk.Label(
                detail_frame,
                text=label,
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['text_dark']
            ).pack(side=tk.LEFT)

            tk.Label(
                detail_frame,
                text=value,
                font=STYLES['text'],
                bg=COLORS['card_bg'],
                fg=COLORS['accent']
            ).pack(side=tk.RIGHT)

        tk.Label(
            receipt_frame,
            text="Thank you for becoming a member!",
            font=STYLES['text'],
            bg=COLORS['card_bg'],
            fg=COLORS['success']
        ).pack(pady=20)

def main(root, username):
    # Fire up the profile page!
    ProfilePage(root, username)

if __name__ == "__main__":
    root = tk.Tk()
    main(root, "admin")  # Using admin for testing - change this in production
    root.mainloop()