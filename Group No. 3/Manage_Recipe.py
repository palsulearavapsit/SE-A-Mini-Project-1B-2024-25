from pathlib import Path
import subprocess
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import io

from config import get_db_connection

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame13")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Global variables
uploaded_image_data = None
selected_recipe_id = None

# Function to populate the recipes table
def populate_recipes_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT recipe_id, name, category FROM recipes")
        recipes = cursor.fetchall()
        
        # Clear existing data
        for row in recipes_tree.get_children():
            recipes_tree.delete(row)
            
        # Insert new data
        for recipe in recipes:
            recipes_tree.insert("", "end", values=(recipe['recipe_id'], recipe['name'], recipe['category']))
            
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to fetch recipes: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to handle table selection
def on_recipe_select(event):
    global selected_recipe_id, uploaded_image_data
    
    selected_item = recipes_tree.focus()
    if not selected_item:
        return
        
    recipe_id = recipes_tree.item(selected_item)['values'][0]
    selected_recipe_id = recipe_id
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM recipes WHERE recipe_id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        
        if recipe:
            # Clear all fields first
            entry_1.delete(0, "end")
            entry_2.delete("1.0", "end")
            entry_3.delete(0, "end")
            entry_4.delete(0, "end")
            entry_5.delete(0, "end")
            
            # Populate fields
            entry_1.insert(0, recipe['name'])
            entry_2.insert("1.0", recipe['ingredients'])
            entry_3.insert(0, recipe['recipe_link'])
            entry_4.insert(0, recipe['instructions'])
            entry_5.insert(0, recipe['category'])
            
            # Handle image
            if recipe['image']:
                uploaded_image_data = recipe['image']
                display_image_from_blob(recipe['image'])
            else:
                uploaded_image_data = None
                canvas.itemconfig(image_2, image=image_image_2)
                
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to fetch recipe details: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to display image from BLOB data
def display_image_from_blob(blob_data):
    try:
        image = Image.open(io.BytesIO(blob_data))
        image = image.resize((302, 144))
        photo = ImageTk.PhotoImage(image)
        canvas.itemconfig(image_2, image=photo)
        canvas.image = photo
    except Exception as e:
        print(f"Error displaying image: {e}")
        canvas.itemconfig(image_2, image=image_image_2)

# Upload image function (unchanged from original)
def upload_image():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
    except:
        try:
            file_path = filedialog.askopenfilename()
        except Exception as e:
            print(f"Error opening file dialog: {e}")
            return

    if file_path:
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif')
        if not file_path.lower().endswith(valid_extensions):
            messagebox.showerror("Error", "Please select a valid image file (PNG, JPG, JPEG, GIF)")
            return
            
        global uploaded_image_data
        uploaded_image_data = convert_image_to_blob(file_path)
        load_image(file_path)
        print(f"Image selected and uploaded: {file_path}")

def load_image(image_path):
    image = Image.open(image_path)
    image = image.resize((302, 144))
    photo = ImageTk.PhotoImage(image)
    canvas.itemconfig(image_2, image=photo)
    canvas.image = photo

def convert_image_to_blob(image_path):
    image = Image.open(image_path)
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
    return img_byte_array.getvalue()

# Store recipe function (unchanged from original except for recipe_id)
def store_recipe_in_db():
    if not uploaded_image_data:
        messagebox.showerror("Error", "No image uploaded! Please upload an image before adding the recipe.")
        return
    
    if not entry_1.get() or not entry_2.get("1.0", "end-1c") or not entry_4.get() or not entry_5.get():
        messagebox.showerror("Error", "Please fill in all fields before adding the recipe.")
        return

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO recipes (name, category, ingredients, instructions, recipe_link, image) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        data = (
            entry_1.get(),
            entry_5.get(),
            entry_2.get("1.0", "end-1c"),
            entry_4.get(),
            entry_3.get(),
            uploaded_image_data
        )

        cursor.execute(insert_query, data)
        connection.commit()
        messagebox.showinfo("Success", "Recipe added successfully!")
        populate_recipes_table()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to add recipe: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Update recipe function (using recipe_id)
def update_recipe():
    global selected_recipe_id
    
    if not selected_recipe_id:
        messagebox.showerror("Error", "No recipe selected! Please select a recipe to update.")
        return
        
    if not uploaded_image_data:
        messagebox.showerror("Error", "No image uploaded! Please upload an image before updating the recipe.")
        return
    
    if not entry_1.get() or not entry_2.get("1.0", "end-1c") or not entry_4.get() or not entry_5.get():
        messagebox.showerror("Error", "Please fill in all fields before updating the recipe.")
        return

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        update_query = """
        UPDATE recipes 
        SET name = %s, category = %s, ingredients = %s, 
            instructions = %s, recipe_link = %s, image = %s
        WHERE recipe_id = %s
        """
        
        data = (
            entry_1.get(),
            entry_5.get(),
            entry_2.get("1.0", "end-1c"),
            entry_4.get(),
            entry_3.get(),
            uploaded_image_data,
            selected_recipe_id
        )

        cursor.execute(update_query, data)
        connection.commit()
        messagebox.showinfo("Success", "Recipe updated successfully!")
        populate_recipes_table()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to update recipe: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Delete recipe function (using recipe_id)
def delete_recipe():
    global selected_recipe_id
    
    if not selected_recipe_id:
        messagebox.showerror("Error", "No recipe selected! Please select a recipe to delete.")
        return
        
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this recipe?"):
        return

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        delete_query = "DELETE FROM recipes WHERE recipe_id = %s"
        cursor.execute(delete_query, (selected_recipe_id,))
        connection.commit()
        
        messagebox.showinfo("Success", "Recipe deleted successfully!")
        clear_form()
        populate_recipes_table()
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to delete recipe: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to clear the form
def clear_form():
    global selected_recipe_id, uploaded_image_data
    selected_recipe_id = None
    uploaded_image_data = None
    
    entry_1.delete(0, "end")
    entry_2.delete("1.0", "end")
    entry_3.delete(0, "end")
    entry_4.delete(0, "end")
    entry_5.delete(0, "end")
    canvas.itemconfig(image_2, image=image_image_2)

# Initialize the main window (unchanged from original)
window = Tk()
window.geometry("1138x746")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=746,
    width=1138,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Original GUI elements (unchanged)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(569.0, 373.0, image=image_image_1)

canvas.create_text(28.0, 69.0, anchor="nw", text="Recipe name", fill="#F7F7F7", font=("Inika", 36 * -1))
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(384.5, 95.0, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=283.0, y=74.0, width=203.0, height=40.0)

canvas.create_text(30.0, 153.0, anchor="nw", text="Ingredients", fill="#FFFFFF", font=("Inika", 36 * -1))
canvas.create_text(28.0, 239.0, anchor="nw", text="Instructions", fill="#FFFFFF", font=("Inika", 36 * -1))

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(520.5, 305.0, image=entry_image_2)
entry_2 = Text(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_2.place(x=283.0, y=233.0, width=475.0, height=142.0)

canvas.create_text(511.0, 69.0, anchor="nw", text="Video Link", fill="#FFFFFF", font=("Inika", 36 * -1))
entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(910.0, 90.5, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_3.place(x=716.0, y=69.0, width=388.0, height=41.0)

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(443.0, 174.0, image=entry_image_4)
entry_4 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_4.place(x=283.0, y=150.0, width=320.0, height=46.0)

canvas.create_text(632.0, 151.0, anchor="nw", text="Category", fill="#FFFFFF", font=("Inika", 36 * -1))
entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(956.5, 173.0, image=entry_image_5)
entry_5 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_5.place(x=809.0, y=150.0, width=295.0, height=44.0)

upload_button = Button(
    text="Upload Img",
    command=upload_image,
    font=("Arial", 12),
    bg="#D9D9D9",
    fg="#000716",
    relief="flat"
)
upload_button.place(x=963.0, y=385.0, width=130, height=30)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(963.0, 305.0, image=image_image_2)

add_button = Button(
    text="Add Recipe",
    borderwidth=0,
    highlightthickness=0,
    command=store_recipe_in_db,
    relief="flat",
    font=("Arial", 12)
)
add_button.place(x=283.0, y=400.0, width=170.0, height=53.0)

update_button = Button(
    text="Update Recipe",
    borderwidth=0,
    highlightthickness=0,
    command=update_recipe,
    relief="flat",
    font=("Arial", 12)
)
update_button.place(x=459.0, y=400.0, width=170.0, height=53.0)

delete_button = Button(
    text="Delete Recipe",
    borderwidth=0,
    highlightthickness=0,
    command=delete_recipe,
    relief="flat",
    font=("Arial", 12)
)
delete_button.place(x=635.0, y=400.0, width=170.0, height=53.0)

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

# Create a frame for the table below the existing GUI
table_frame = ttk.Frame(window)
table_frame.place(x=50, y=480, width=1038, height=250)

# Create a treeview with scrollbars
style = ttk.Style()
style.configure("Treeview", font=('Arial', 10), rowheight=25)
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

recipes_tree = ttk.Treeview(table_frame, columns=("recipe_id", "Name", "Category"), show="headings")
recipes_tree.heading("recipe_id", text="ID")
recipes_tree.heading("Name", text="Name")
recipes_tree.heading("Category", text="Category")
recipes_tree.column("recipe_id", width=50, anchor="center")
recipes_tree.column("Name", width=300, anchor="w")
recipes_tree.column("Category", width=200, anchor="w")

# Add scrollbars
v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=recipes_tree.yview)
h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=recipes_tree.xview)
recipes_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

# Grid layout
recipes_tree.grid(row=0, column=0, sticky="nsew")
v_scroll.grid(row=0, column=1, sticky="ns")
h_scroll.grid(row=1, column=0, sticky="ew")

# Configure grid weights
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# Bind selection event
recipes_tree.bind("<<TreeviewSelect>>", on_recipe_select)

# Populate the table on startup
populate_recipes_table()

window.resizable(False, False)
window.mainloop()