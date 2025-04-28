from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage, Listbox, Scrollbar, messagebox
from Recipe_View import open_view_page
from controllers.recipe_controller import search_recipes, get_recipe_by_id

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame4")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_ingredients_page(previous_window, user_id):
    previous_window.destroy()

    def open_home():
        from Home_Login import open_hlogin_page
        open_hlogin_page(window, user_id)

    def perform_search():
        """Search recipes based on ingredients."""
        keyword = entry_1.get().strip()
        if not keyword:
            messagebox.showerror("Error", "Please enter ingredients to search.")
            return
        
        results = search_recipes(keyword, "ingredients")
        results_listbox.delete(0, tk.END)
        
        if results:
            for recipe in results:
                results_listbox.insert(tk.END, f"{recipe['recipe_id']} - {recipe['name']}")
        else:
            messagebox.showinfo("No Results", "No matching recipes found.")

    def show_recipe_details(event):
        """Open a new window with full recipe details."""
        selected_index = results_listbox.curselection()
        if not selected_index:
            return
        
        selected_recipe = results_listbox.get(selected_index[0])
        recipe_id = selected_recipe.split(" - ")[0]
        
        try:
            recipe_id = int(recipe_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid recipe selection.")
            return
        
        recipe = open_view_page(window,recipe_id,user_id)

    # GUI Setup
    window = tk.Tk()
    window.geometry("1095x660")
    window.configure(bg="#FFFFFF")
    canvas = Canvas(window, bg="#FFFFFF", height=660, width=1095, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(547.0, 330.0, image=image_image_1)
    canvas.create_rectangle(0.0, 0.0, 1095.0, 62.0, fill="#7B5401", outline="")
    canvas.create_text(76.0, 8.0, anchor="nw", text="Search Your Recipe", fill="#FFFFFF", font=("Inika", 36 * -1))
    canvas.create_text(49.0, 85.0, anchor="nw", text="Enter your ingredients", fill="#010101", font=("Inika", 32 * -1))

    # Search Entry Field
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(435.0, 156.5, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_1.place(x=32.0, y=136.0, width=806.0, height=39.0)

    # Search Button
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=perform_search, relief="flat")
    button_1.place(x=638.0, y=85.0, width=210.0, height=46.0)

    canvas.create_text(49.0, 204.0, anchor="nw", text="Recipe Results", fill="#000000", font=("Inika", 32 * -1))

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
        x=35,
        y=30,
        radius=20,
        color="brown",
        text="←",
        text_color="white",
        command=open_home
    )

    # Results Listbox with Scrollbar
    frame = tk.Frame(window)
    frame.place(x=49, y=250, width=900, height=300)
    results_listbox = Listbox(frame, bg="white", fg="black", font=("Arial", 14))
    results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=results_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    results_listbox.config(yscrollcommand=scrollbar.set)
    results_listbox.bind("<<ListboxSelect>>", show_recipe_details)

    window.resizable(False, False)
    window.mainloop()
