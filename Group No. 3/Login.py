import subprocess
import mysql.connector
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from tkinter import messagebox
from pathlib import Path

from Home_Login import open_hlogin_page
from config import get_db_connection

# Set up asset path handling
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_login_page(previous_window):
    previous_window.destroy()

    def login_user():
        email = entry_1.get().strip()
        password = entry_2.get().strip()

        if not email:
            messagebox.showerror("Input Error", "Email is required!")
            return
        if not password:
            messagebox.showerror("Input Error", "Password is required!")
            return

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s", (email, password))
            user = cursor.fetchone()
            if user:
                if user[5] == 'YES':
                    open_file("Admin.py")
                else:
                    open_hlogin_page(window, user[0])         
            else:
                messagebox.showerror("Invalid Credentials", "Incorrect email or password!")
                return
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"An error occurred: {err}")
            return
        finally:
            cursor.close()
            db.close()

    def open_file(pyfile):
        window.destroy()
        subprocess.Popen(["python3", pyfile])

    def go_to_homepage():
        window.destroy()
        subprocess.Popen(["python3", "Homepage.py"])

    def toggle_password():
        if entry_2.cget('show') == '*':
            entry_2.config(show='')
            toggle_btn.config(fg='#555555')
        else:
            entry_2.config(show='*')
            toggle_btn.config(fg='#777777')

    window = Tk()
    window.geometry("915x610")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=610,
        width=915,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Add back button (cross icon) in top-left corner
    back_button = Button(
        window,
        text="✕",
        command=go_to_homepage,
        font=("Arial", 14),
        relief="flat",
        bg="#FFFFFF",
        activebackground="#FFFFFF",
        borderwidth=0,
        fg="#000000",
        activeforeground="#555555"
    )
    back_button.place(x=20, y=20, width=30, height=30)

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(457.0, 305.0, image=image_image_1)

    canvas.create_text(
        493.0,
        320.0,
        anchor="nw",
        text="Email",
        fill="#000000",
        font=("Inika", 36 * -1)
    )

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(749.5, 336.0, image=entry_image_1)
    entry_1 = Entry(
        bd=0,
        bg="#B3AFAF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(x=664.0, y=320.0, width=171.0, height=30.0)

    canvas.create_text(
        474.0,
        386.0,
        anchor="nw",
        text="Password",
        fill="#000000",
        font=("Inika", 32 * -1)
    )

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(749.5, 410.5, image=entry_image_2)
    entry_2 = Entry(
        bd=0,
        bg="#B4AFAF",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    entry_2.place(x=664.0, y=393.0, width=171.0, height=33.0)

    # Transparent gray toggle button
    toggle_btn = Button(
        window,
        text="👁",
        command=toggle_password,
        font=("Arial", 10),
        relief="flat",
        bg="#B4AFAF",
        activebackground="#B4AFAF",
        borderwidth=0,
        padx=0,
        pady=0,
        fg="#777777",
        activeforeground="#555555",
        highlightthickness=0
    )
    toggle_btn.place(x=810.0, y=395.0, width=25.0, height=25.0)

    toggle_btn.config(
        highlightbackground="#B4AFAF",
        highlightcolor="#B4AFAF"
    )

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=login_user,
        relief="flat"
    )
    button_1.place(x=684.0, y=469.0, width=131.0, height=44.0)

    canvas.create_text(
        443.0,
        153.0,
        anchor="nw",
        text="Login",
        fill="#FFFFFF",
        font=("Inika Bold", 40 * -1)
    )

    window.resizable(False, False)
    window.mainloop()