# Hey there! This is our admin dashboard where we manage EV station users.
# Built with tkinter for the UI and MySQL for storing user data.


import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Button, Entry, StringVar, Toplevel
import mysql.connector

# Database connection settings - might want to move this to a config file later
DB_CONFIG = {
    'host': "127.0.0.1",
    'user': "root",
    'password': "Shardul203",  # Remember to change this in production!
    'database': "ev_station"
}

# Our app's color scheme - keeping it clean and professional
COLORS = {
    'primary': "#4CAF50",    # Nice green for main actions
    'secondary': "#2b2b2b",  # Dark theme background
    'accent': "#d77337",     # Orange pop for highlights
    'text_light': "#ffffff", # White text that stands out
    'text_dark': "#333333",  # Easy to read dark text
    'warning': "#FFA500",    # Yellow for heads-up messages
    'error': "#FF0000",      # Red for delete/remove actions
    'success': "#28a745",    # Green for success messages
    'card_bg': "#ffffff"     # White for our cards
}

# Font styles to keep everything consistent
STYLES = {
    'title': ('Arial', 24, 'bold'),    # Big headers
    'subtitle': ('Arial', 18),         # Section titles
    'button': ('Arial', 16),           # Button text
    'text': ('Arial', 14),             # Regular text
    'small_text': ('Arial', 12)        # Small details
}

class AdminPage:
    def __init__(self, root):
        # Initialize our admin dashboard
        self.root = root
        self.setup_window()
        self.create_interface()
        self.load_users()  # Get our initial user list

    def setup_window(self):
        # Set up our main window - make it look nice and professional
        self.root.title("Admin Dashboard")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.state('zoomed')  # Start maximized
        self.root.resizable(True, True)  # Let users resize if needed

    def create_interface(self):
        # Build our main UI container
        self.container = Frame(self.root, bg=COLORS['secondary'])
        self.container.pack(fill=tk.BOTH, expand=True)
        self.create_header()
        self.create_user_list()

    def execute_db_operation(self, operation, params=None):
        # Helper function to handle database operations safely
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(operation, params or ())
                if operation.lower().startswith('select'):
                    return cursor.fetchall()
                conn.commit()
                return None

    def create_styled_button(self, parent, text, command, bg_color=COLORS['primary']):
        # Create a consistently styled button
        return Button(
            parent, text=text, font=STYLES['button'],
            bg=bg_color, fg=COLORS['text_light'],
            command=command
        )

    def load_users(self):
        # Refresh our user list display
        for widget in self.users_frame.winfo_children()[3:]:
            widget.destroy()

        try:
            # Grab all users from the database
            users = self.execute_db_operation("SELECT username, status FROM users")
            
            # Create a row for each user
            for i, (username, status) in enumerate(users, 1):
                # Username column
                Label(self.users_frame, text=username, font=STYLES['text'],
                      bg=COLORS['card_bg']).grid(row=i, column=0, padx=10, pady=5, sticky='w')
                
                # Status column with color coding
                status_color = COLORS['success'] if status == 'active' else COLORS['warning']
                Label(self.users_frame, text=status or "Inactive", font=STYLES['text'],
                      fg=status_color, bg=COLORS['card_bg']).grid(row=i, column=1, padx=10, pady=5, sticky='w')
                
                # Action buttons column
                action_frame = Frame(self.users_frame, bg=COLORS['card_bg'])
                action_frame.grid(row=i, column=2, padx=10, pady=5, sticky='w')
                
                # View details button
                Button(action_frame, text="Show", font=STYLES['small_text'],
                      bg=COLORS['accent'], fg=COLORS['text_light'],
                      command=lambda u=username: self.edit_user(u)).pack(side=tk.LEFT, padx=5)
                
                # Delete user button
                Button(action_frame, text="Delete", font=STYLES['small_text'],
                      bg=COLORS['error'], fg=COLORS['text_light'],
                      command=lambda u=username: self.delete_user(u)).pack(side=tk.LEFT, padx=5)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load users: {str(e)}")

    def edit_user(self, username):
        # Pop up a window to view user details
        try:
            edit_window = Toplevel(self.root)
            edit_window.title(f"User Details: {username}")
            edit_window.geometry("400x400")
            edit_window.configure(bg=COLORS['card_bg'])

            # Get the user's info from the database
            user_data = self.execute_db_operation(
                "SELECT username, password, status FROM users WHERE username=%s",
                (username,)
            )[0]

            # Show all the user details
            Label(edit_window, text="User Details", font=STYLES['subtitle'], 
                  bg=COLORS['card_bg']).pack(pady=20)

            # Display fields (username, password, status)
            for field, value in zip(["Username:", "Password:", "Status:"], user_data):
                Label(edit_window, text=field, font=STYLES['text'], 
                      bg=COLORS['card_bg']).pack(pady=5)
                var = StringVar(value=value if value else 'active')
                Entry(edit_window, textvariable=var, state='readonly', 
                     font=STYLES['text']).pack(pady=5)

            # Close button
            Button(edit_window, text="OK", font=STYLES['button'],
                  bg=COLORS['primary'], fg=COLORS['text_light'],
                  command=edit_window.destroy).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Couldn't load user data: {str(e)}")
            if 'edit_window' in locals():
                edit_window.destroy()

    def delete_user(self, username):
        # Handle user deletion with confirmation
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete {username}?"):
            try:
                self.execute_db_operation(
                    "DELETE FROM users WHERE username=%s",
                    (username,)
                )
                messagebox.showinfo("Success", "User deleted!")
                self.load_users()  # Refresh our list
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Couldn't delete user: {str(e)}")

# Fire up the admin dashboard!
def run_admin_page():
    root = tk.Tk()
    AdminPage(root)
    root.mainloop()

if __name__ == "__main__":
    run_admin_page()