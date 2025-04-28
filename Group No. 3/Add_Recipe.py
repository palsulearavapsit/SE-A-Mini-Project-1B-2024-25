from pathlib import Path
import subprocess
import mysql.connector
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox
from PIL import Image, ImageTk
from config import get_db_connection
import io

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame12")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def open_uadd_page(previous_window, user_id):
    previous_window.destroy()
    # Initialize uploaded_image_data as None
    uploaded_image_data = None

    def open_home():
        from Home_Login import open_hlogin_page
        open_hlogin_page(window, user_id)
    # Function to open the file dialog and choose an image
    def upload_image():
        try:
            # Use a more robust file dialog approach for macOS
            file_path = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
            )
            
            if file_path:  # If the user selects a file
                global uploaded_image_data
                uploaded_image_data = convert_image_to_blob(file_path)
                # Load and display the image in the canvas
                load_image(file_path)
            else:
                print("No image selected!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {str(e)}")

    # Function to load and display the selected image in the canvas
    def load_image(image_path):
        try:
            # Open the image using Pillow
            image = Image.open(image_path)
            image = image.resize((305, 185))  # Resize the image to fit into the canvas
            photo = ImageTk.PhotoImage(image)

            # Update the image in the canvas
            canvas.itemconfig(image_3, image=photo)
            canvas.image = photo  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    # Function to convert image to BLOB
    def convert_image_to_blob(image_path):
        try:
            image = Image.open(image_path)
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format='PNG')
            return img_byte_array.getvalue()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")
            return None

    # Function to store recipe details in the database
    def store_recipe_in_db():
        global uploaded_image_data
        
        if not uploaded_image_data:
            messagebox.showerror("Error", "No image uploaded! Please upload an image before adding the recipe.")
            return
        
        # Validate that all required fields are filled
        if not entry_1.get() or not entry_2.get() or not entry_3.get("1.0", "end-1c") or not entry_5.get():
            messagebox.showerror("Error", "Please fill in all fields before adding the recipe.")
            return

        # Insert the recipe details and image into the database
        try:
            # Connect to MySQL database
            connection = get_db_connection()

            cursor = connection.cursor()

            # Define your INSERT query with the correct column name (recipe_link)
            insert_query = """
            INSERT INTO recipes (name, ingredients, instructions, category, recipe_link, image) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            # Prepare the data to insert
            data = (
                entry_1.get(),          # Recipe Name
                entry_2.get(),          # Ingredients
                entry_3.get("1.0", "end-1c"),  # Instructions (Text widget)
                entry_5.get(),          # Category
                entry_4.get(),          # Recipe Link
                uploaded_image_data     # Image as BLOB
            )

            # Execute the query
            cursor.execute(insert_query, data)

            # Commit the transaction
            connection.commit()

            print("Recipe and image details stored successfully!")

            # Show a success message
            messagebox.showinfo("Success", "Recipe added successfully!")
            open_home

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", f"Failed to add recipe: {err}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    # Function to clear all fields
    def clear_fields():
        entry_1.delete(0, 'end')
        entry_2.delete(0, 'end')
        entry_3.delete("1.0", "end")  # For Text widget
        entry_4.delete(0, 'end')
        entry_5.delete(0, 'end')
        global uploaded_image_data
        uploaded_image_data = None  # Reset the image
        # Reset the image display
        image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        canvas.itemconfig(image_3, image=image_image_3)
        canvas.image = image_image_3  # Keep reference

    # Initialize the main window
    window = Tk()
    window.geometry("1096x661")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=661,
        width=1096,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    # Background images
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(548.0, 330.0, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    canvas.create_image(548.0, 35.0, image=image_image_2)

    # Labels and Entry fields
    canvas.create_text(39.0, 93.0, anchor="nw", text="Name", fill="#FAFAFA", font=("Inika Bold", 40 * -1))
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(416.5, 113.0, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_1.place(x=292.0, y=87.0, width=249.0, height=50.0)

    canvas.create_text(39.0, 167.0, anchor="nw", text="Ingredients", fill="#FFFFFF", font=("Inika Bold", 40 * -1))
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(502.0, 191.5, image=entry_image_2)
    entry_2 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_2.place(x=292.0, y=163.0, width=420.0, height=55.0)

    canvas.create_text(37.0, 238.0, anchor="nw", text="Instructions", fill="#FFFFFF", font=("Inika Bold", 40 * -1))
    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    canvas.create_image(334.5, 386.5, image=entry_image_3)
    entry_3 = Text(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_3.place(x=47.0, y=294.0, width=575.0, height=183.0)

    # Category and Video Link
    canvas.create_text(770.0, 87.0, anchor="nw", text="Category", fill="#FFFFFF", font=("Inika Bold", 40 * -1))
    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    canvas.create_image(617.5, 533.5, image=entry_image_4)
    entry_4 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_4.place(x=292.0, y=506.0, width=651.0, height=53.0)

    # Video Link Label
    canvas.create_text(39.0, 509.0, anchor="nw", text="Video Link", fill="#FFFFFF", font=("Inika Bold", 40 * -1))

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    canvas.create_image(898.5, 193.5, image=entry_image_5)
    entry_5 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_5.place(x=780.0, y=167.0, width=237.0, height=51.0)

    # Add Recipe button
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=store_recipe_in_db,
        relief="flat"
    )
    button_1.place(x=36.0, y=583.0, width=224.0, height=71.0)

    # Clear button
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=clear_fields,
        relief="flat"
    )
    button_2.place(x=301.0, y=583.0, width=224.0, height=71.0)

    # Image placeholder
    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(874.0, 386.0, image=image_image_3)

    # Button to upload image
    upload_button = Button(
        text="Upload Img", 
        command=upload_image,
        font=("Arial", 12),
        bg="#D9D9D9",
        fg="#000716",
        relief="flat"
    )
    upload_button.place(x=720.0, y=294.0 - 35, width=130, height=30)

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
        x=37,
        y=35,
        radius=20,
        color="brown",
        text="←",
        text_color="white",
        command=open_home
    )

    window.resizable(False, False)
    window.mainloop()