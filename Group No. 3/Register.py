import tkinter as tk
from tkinter import messagebox
import mysql.connector
from pathlib import Path
import subprocess
import re
from Login import open_login_page
from config import get_db_connection

# Function to handle user registration
def register_user():
    username = entry_1.get().strip()
    email = entry_2.get().strip()
    password_ = entry_3.get().strip()
    phone = entry_4.get().strip()

    if not username or not email or not phone or not password_:
        messagebox.showerror("Input Error", "All fields are required!")
        return
    
    if not re.match(r"^\d{10}$", phone):
        messagebox.showerror("Invalid Phone Number", "Phone number must be 10 digits!")
        return

    if len(password_) < 6:
        messagebox.showerror("Invalid Password", "Password must be at least 6 characters long!")
        return

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email, password_hash, phone) VALUES (%s, %s, %s, %s)", 
                      (username, email, password_, phone))
        db.commit()
        open_file()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    finally:
        cursor.close()
        db.close()

def open_file():
    window.destroy()
    subprocess.Popen(["python3", "Homepage.py"])

def go_back():
    window.destroy()
    subprocess.Popen(["python3", "Homepage.py"])

def toggle_password():
    if entry_3.cget('show') == '*':
        entry_3.config(show='')
        toggle_btn.config(fg='#555555')
    else:
        entry_3.config(show='*')
        toggle_btn.config(fg='#777777')

# Setup tkinter window
window = tk.Tk()
window.geometry("578x658")
window.configure(bg="#FFFFFF")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

canvas = tk.Canvas(
    window,
    bg="#FFFFFF",
    height=658,
    width=578,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Add back button (cross icon) in top-left corner
back_button = tk.Button(
    window,
    text="✕",
    command=go_back,
    font=("Arial", 14),
    relief="flat",
    bg="#FFFFFF",
    activebackground="#FFFFFF",
    borderwidth=0,
    fg="#000000",
    activeforeground="#555555"
)
back_button.place(x=20, y=20, width=30, height=30)

image_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(289.0, 329.0, image=image_image_1)

canvas.create_text(289, 240, anchor="center", text="Register", fill="#000000", font=("Arial", 20, "bold"))

# Username field
entry_image_1 = tk.PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(287.5, 242.0, image=entry_image_1)
entry_1 = tk.Entry(window, bd=0, bg="#CFB9B9", fg="#000716", highlightthickness=0)
entry_1.place(x=138.0, y=225.0, width=299.0, height=32.0)
canvas.create_text(133.0, 196.0, anchor="nw", text="Name", fill="#000000", font=("Inika", 16 * -1))

# Email field
entry_image_2 = tk.PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(289.5, 318.0, image=entry_image_2)
entry_2 = tk.Entry(window, bd=0, bg="#CFB9B9", fg="#000716", highlightthickness=0)
entry_2.place(x=140.0, y=301.0, width=299.0, height=32.0)
canvas.create_text(133.0, 273.0, anchor="nw", text="Email", fill="#000000", font=("Inika", 16 * -1))

# Password field with toggle button
entry_image_3 = tk.PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(289.5, 397.5, image=entry_image_3)
entry_3 = tk.Entry(window, bd=0, bg="#CFB9B9", fg="#000716", highlightthickness=0, show="*")
entry_3.place(x=140.0, y=381.0, width=299.0, height=31.0)
canvas.create_text(135.0, 350.0, anchor="nw", text="Password", fill="#000000", font=("Inika", 16 * -1))

# Password toggle button
toggle_btn = tk.Button(
    window,
    text="👁",
    command=toggle_password,
    font=("Arial", 10),
    relief="flat",
    bg="#CFB9B9",
    activebackground="#CFB9B9",
    borderwidth=0,
    padx=0,
    pady=0,
    fg="#777777",
    activeforeground="#555555",
    highlightthickness=0
)
toggle_btn.place(x=415.0, y=381.0, width=25.0, height=31.0)

# Phone field
entry_image_4 = tk.PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(289.5, 478.5, image=entry_image_4)
entry_4 = tk.Entry(window, bd=0, bg="#CFB9B9", fg="#000716", highlightthickness=0)
entry_4.place(x=140.0, y=462.0, width=299.0, height=31.0)
canvas.create_text(135.0, 423.0, anchor="nw", text="Phone No", fill="#000000", font=("Inika", 16 * -1))

# Register Button
button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = tk.Button(window, image=button_image_1, borderwidth=0, highlightthickness=0, command=register_user, relief="flat")
button_1.place(x=224.0, y=520.0, width=131.0, height=44.0)

canvas.create_text(
    188.0,
    110.0,
    anchor="nw",
    text="Register Here",
    fill="#000000",
    font=("Inika Bold", 32 * -1)
)

window.resizable(False, False)
window.mainloop()