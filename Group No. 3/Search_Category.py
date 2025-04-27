from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from controllers.recipe_controller import get_categories, search_by_category, get_recipe_by_id
from Recipe_View import open_view_page

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame5")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_category_page(previous_window, user_id):
    previous_window.destroy()
    window = tk.Tk()
    window.geometry("1095x660")
    window.configure(bg="#FFFFFF")

    def open_home():
        from Home_Login import open_hlogin_page
        open_hlogin_page(window, user_id)

    canvas = tk.Canvas(
        window,
        bg="#FFFFFF",
        height=660,
        width=1095,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        547.0,
        330.0,
        image=image_image_1
    )

    canvas.create_rectangle(
        0.0,
        0.0,
        1095.0,
        60.0,
        fill="#3B1212",
        outline=""
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))  # Ensure the file exists in the assets folder
    image_3 = canvas.create_image(
        15.0,
        7.0,
        image=image_image_3,
        anchor="nw"
    )

    canvas.create_text(
        83.0,
        7.0,
        anchor="nw",
        text="Categorize Your Recipe",
        fill="#FFFFFF",
        font=("Inika", 36 * -1)
    )

    canvas.create_text(
        48.0,
        97.0,
        anchor="nw",
        text="Select the Category ",
        fill="#000000",
        font=("Inika", 32 * -1)
    )

    def update_table(*args):
        selected_category = category_var.get()
        recipes = search_by_category(selected_category)
        table.delete(*table.get_children())
        for recipe in recipes:
            table.insert("", "end", values=(recipe["recipe_id"], recipe["name"]))

    def show_recipe_details(event):
        selected_item = table.selection()
        if not selected_item:
            return
        recipe_id = table.item(selected_item, "values")[0]
        recipe = open_view_page(window, recipe_id, user_id)

    category_var = tk.StringVar()
    categories = get_categories()
    category_dropdown = ttk.Combobox(window, textvariable=category_var, values=categories, state="readonly")
    category_dropdown.place(x=50, y=140, width=300, height=40)
    category_var.trace_add("write", update_table)

    canvas.create_text(
        48.0,
        202.0,
        anchor="nw",
        text="Results",
        fill="#000000",
        font=("Inika", 32 * -1)
    )

    table = ttk.Treeview(window, columns=("ID", "Name"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.place(x=50, y=250, width=800, height=300)
    table.bind("<Double-1>", show_recipe_details)

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

    back_button = CircleButton(
        canvas=canvas,
        x=38,
        y=30,
        radius=20,
        color="brown",
        text="←",
        text_color="white",
        command=open_home
    )

    window.resizable(False, False)
    window.mainloop()
