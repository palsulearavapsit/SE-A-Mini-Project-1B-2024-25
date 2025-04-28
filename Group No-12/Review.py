from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import mysql.connector

# Database configuration (update with your credentials)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Aayush@0909',
    'database': 'findr',
    'auth_plugin': 'mysql_native_password'
}

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/Review")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_review_page(previous_window, user_id, user_name):
    previous_window.destroy()
    window = Tk()

    window.geometry("700x840")
    window.configure(bg = "#FFFFFF")

    def open_home():
        from Home import open_home_page
        open_home_page(window, user_id, user_name)

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 840,
        width = 700,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        352.0,
        422.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=33.0,
        y=19.0,
        width=77.0,
        height=31.0
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        322.5,
        441.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=33.0,
        y=306.0,
        width=579.0,
        height=269.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=open_home,
        relief="flat"
    )
    button_2.place(
        x=414.0,
        y=749.0,
        width=207.17578125,
        height=52.344825744628906
    )
    window.resizable(False, False)
    window.mainloop()
