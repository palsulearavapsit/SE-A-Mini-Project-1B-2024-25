import subprocess
import tkinter as tk
from tkinter import ttk, Canvas, Entry, Button, PhotoImage, messagebox
import mysql.connector
from pathlib import Path
from config import get_db_connection


# Database function to fetch data from MySQL
def fetch_data():
    try:
        # Establish MySQL connection
        db = get_db_connection()
        cursor = db.cursor()

        # Fetch the table column names
        cursor.execute("DESCRIBE users")  # Replace "users" with your actual table name
        columns = [col[0] for col in cursor.fetchall()]

        tree["columns"] = columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        # Fetch all rows from the users table
        cursor.execute("SELECT * FROM users")  # Replace "users" with your actual table name
        rows = cursor.fetchall()

        # Clear previous data in the treeview
        tree.delete(*tree.get_children())

        # Insert new data into the treeview
        for row in rows:
            tree.insert('', 'end', values=row)

        cursor.close()
        db.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}")

# Function to update selected user's data in the database
def update_data():
    selected_item = tree.selection()  # Get the selected row from the Treeview
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a user to update.")
        return

    # Get the current data from the selected row
    selected_data = tree.item(selected_item)["values"]
    user_id = selected_data[0]  # Assuming the first column is the user ID

    # Get the updated data from the Entry fields
    username = entry_1.get().strip()
    email = entry_2.get().strip()
    password_ = entry_3.get().strip()
    phone = entry_4.get().strip()

    # Validate the input data
    if not username or not email or not password_ or not phone:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    # Connect to the database and perform the update
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("UPDATE users SET username = %s, email = %s, password_hash = %s, phone = %s WHERE user_id = %s",
                       (username, email, password_, phone, user_id))
        db.commit()
        messagebox.showinfo("Success", "User information updated successfully!")

        # Refresh the table view to show the updated data
        fetch_data()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error updating data: {e}")
    finally:
        cursor.close()
        db.close()

# Function to delete selected user's data from the database
def delete_data():
    selected_item = tree.selection()  # Get the selected row from the Treeview
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a user to delete.")
        return

    # Get the current data from the selected row
    selected_data = tree.item(selected_item)["values"]
    user_id = selected_data[0]  # Assuming the first column is the user ID

    # Connect to the database and perform the delete operation
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        db.commit()
        messagebox.showinfo("Success", "User deleted successfully!")

        # Refresh the table view to reflect the changes
        fetch_data()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error deleting data: {e}")
    finally:
        cursor.close()
        db.close()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame6")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = tk.Tk()
window.geometry("1095x661")
window.configure(bg="#BE9494")

canvas = Canvas(
    window,
    bg="#BE9494",
    height=661,
    width=1095,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_text(
    42.0,
    90.0,
    anchor="nw",
    text="Username",
    fill="#000000",
    font=("Inika Bold", 24 * -1)
)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=201.0, y=85.0, width=251.0, height=39.0)

canvas.create_text(42.0, 162.0, anchor="nw", text="Email", fill="#000000", font=("Inika Bold", 24 * -1))
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_2 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_2.place(x=201.0, y=157.0, width=251.0, height=39.0)

canvas.create_text(42.0, 234.0, anchor="nw", text="Password", fill="#000000", font=("Inika Bold", 24 * -1))
entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_3 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_3.place(x=201.0, y=229.0, width=251.0, height=39.0)

canvas.create_text(524.0, 90.0, anchor="nw", text="Phone No", fill="#000000", font=("Inika Bold", 24 * -1))
entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_4 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_4.place(x=675.0, y=85.0, width=251.0, height=39.0)

canvas.create_rectangle(0.0, 0.0, 1095.0, 61.0, fill="#471212", outline="")
canvas.create_text(83.0, 7.0, anchor="nw", text="Manage Profile", fill="#FFFFFF", font=("Inika Bold", 36 * -1))

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=update_data, relief="flat")
button_1.place(x=516.0, y=226.0, width=172.0, height=44.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=delete_data, relief="flat")
button_2.place(x=764.0, y=225.0, width=172.0, height=44.0)

# Create back button as a Canvas widget that acts as a button
class CircleButton:
    def __init__(self, canvas, x, y, radius, color, text, text_color, command):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.command = command
        
        # Create circle
        self.circle = canvas.create_oval(
            x-radius, y-radius,
            x+radius, y+radius,
            fill=color, outline=""
        )
        
        # Create text
        self.text = canvas.create_text(
            x, y,
            text=text,
            fill=text_color,
            font=("Arial", 24, "bold")
        )
        
        # Bind click events to both circle and text
        canvas.tag_bind(self.circle, "<Button-1>", self.on_click)
        canvas.tag_bind(self.text, "<Button-1>", self.on_click)
        
    def on_click(self, event):
        self.command()

# Create the back button
def back_command():
    window.destroy()
    subprocess.Popen(["python3", "Admin.py"])

back_button = CircleButton(
    canvas=canvas,
    x=30,
    y=28,
    radius=20,
    color="brown",
    text="←",
    text_color="white",
    command=back_command
)

# Frame to hold the MySQL Table
table_frame = tk.Frame(window)
table_frame.place(x=25, y=355, width=1045, height=267)

# Create the Treeview widget
tree = ttk.Treeview(table_frame, selectmode="browse")
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
vsb.pack(side="right", fill="y")
tree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
hsb.pack(side="bottom", fill="x")
tree.configure(xscrollcommand=hsb.set)

tree.pack(fill="both", expand=True)

# Refresh button
refresh_button = tk.Button(window, text="Refresh Data", command=fetch_data)
refresh_button.place(x=500, y=630)

# Initial fetch to populate the table
fetch_data()

# Handle treeview item selection
def on_treeview_select(event):
    selected_item = tree.selection()  # Get the selected row
    if selected_item:
        selected_data = tree.item(selected_item)["values"]
        entry_1.delete(0, tk.END)
        entry_2.delete(0, tk.END)
        entry_3.delete(0, tk.END)
        entry_4.delete(0, tk.END)
        
        entry_1.insert(0, selected_data[1])  # Assuming the second column is username
        entry_2.insert(0, selected_data[2])  # Assuming the third column is email
        entry_3.insert(0, selected_data[3])  # Assuming the fourth column is password
        entry_4.insert(0, selected_data[4])  # Assuming the fifth column is phone number

tree.bind("<<TreeviewSelect>>", on_treeview_select)

window.resizable(False, False)
window.mainloop()










