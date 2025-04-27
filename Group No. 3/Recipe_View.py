from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import webbrowser
import mysql.connector

from Rating import RatingPage
from config import get_db_connection  # Added for database connection

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame10")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_rating_stars(rating):
    """Convert a rating (0-5) to star symbols"""
    rating = int(rating or 0)  # Convert None to 0 and ensure it's an integer
    filled_stars = '★' * rating
    empty_stars = '☆' * (5 - rating)
    return filled_stars + empty_stars

def open_view_page(previous_window, recipe_id, user_id):
    previous_window.destroy()
    window = Tk()
    window.geometry("1095x660")
    window.configure(bg="#FFFFFF")

    def open_home():
        from Home_Login import open_hlogin_page
        open_hlogin_page(window, user_id)

    def open_rating():
        # Create the RatingPage window with only required parameters
        rating_page = RatingPage(window, recipe_id)  # Only parent and recipe_id
        
        # Wait for the rating window to close using the top-level window
        window.wait_window(rating_page.top)
        
        # After rating window is closed, open home
        open_home()

    # Fetch recipe data and rating
    recipe_data = None
    rating = 0
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Fetch recipe data
            cursor.execute(
                "SELECT name, category, ingredients, instructions, recipe_link, image, ratings FROM recipes WHERE recipe_id = %s", 
                (recipe_id,)
            )
            recipe_data = cursor.fetchone()
            
            if recipe_data and recipe_data[6] is not None:
                rating = int(recipe_data[6])
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=660,
        width=1095,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png")) #recipe Photo
    image_1 = canvas.create_image(
        547.0,
        330.0,
        image=image_image_1
    )

    # Recipe Photo - use placeholder if no image in database
    try:
        if recipe_data and recipe_data[5]:  # Using index 5 for image blob
            try:
                # Convert BLOB to PhotoImage
                from PIL import Image, ImageTk
                import io
                pil_image = Image.open(io.BytesIO(recipe_data[5]))
                # Resize to match your layout (adjust dimensions as needed)
                pil_image = pil_image.resize((400, 300), Image.LANCZOS)  
                image_image_2 = ImageTk.PhotoImage(pil_image)
                # Position matches your original (883.0, 237.0)
                canvas.create_image(883.0, 237.0, image=image_image_2)  
            except Exception as e:
                print(f"Image error: {e}")
                # Fallback to default recipe image
                image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
                canvas.create_image(883.0, 237.0, image=image_image_2)
    except IndexError:
        pass 

    # Add rating display below the recipe image
    rating_stars = get_rating_stars(rating)
    canvas.create_text(
        883.0,
        400.0,  # Position below the recipe image
        anchor="center",
        text=f"Rating: {rating_stars}",
        fill="#000000",
        font=("Inika", 24 * -1)
    )

    # Recipe Name - populate with actual data if available
    recipe_name = recipe_data[0] if recipe_data else "Recipe Name"
    canvas.create_text(
        92.0,
        64.0,
        anchor="nw",
        text=recipe_name,
        fill="#000000",
        font=("Inika", 36 * -1)
    )

    # Ingredients - populate with actual data
    ingredients_text = recipe_data[2] if recipe_data else "Ingredients will appear here"
    entry_1 = Text(
        window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Arial", 12)
    )
    entry_1.place(
        x=92.0,
        y=169.0,
        width=476.0,
        height=210.0
    )
    entry_1.insert("1.0", ingredients_text)
    entry_1.config(state="disabled")  # Make it read-only

    # Instructions - populate with actual data
    instructions_text = recipe_data[3] if recipe_data else "Instructions will appear here"
    entry_2 = Text(
        window,
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Arial", 12)
    )
    entry_2.place(
        x=92.0,
        y=433.0,
        width=476.0,
        height=212.0
    )
    entry_2.insert("1.0", instructions_text)
    entry_2.config(state="disabled")  # Make it read-only

    # Video Link - populate with actual data if available
    video_link = recipe_data[4] if recipe_data and recipe_data[4] else "No video link provided"
    # Create the text on canvas
    text_id = canvas.create_text(
        626.0,
        564.0,
        anchor="nw",
        text=video_link,
        fill="#000000",
        font=("Inika", 20),
        tags="clickable_text"  # Add a tag to identify this item
    )

    # Make it look like a hyperlink (blue and underlined)
    canvas.itemconfig(text_id, fill="blue")
    canvas.tag_bind("clickable_text", "<Button-1>", lambda e: webbrowser.open(video_link))

    # Optional: Change cursor to hand when hovering
    canvas.tag_bind("clickable_text", "<Enter>", lambda e: canvas.config(cursor="hand2"))
    canvas.tag_bind("clickable_text", "<Leave>", lambda e: canvas.config(cursor=""))

    # Static UI elements
    canvas.create_text(
        612.0,
        519.0,
        anchor="nw",
        text="Video Link",
        fill="#000000",
        font=("Inika", 32 * -1)
    )

    canvas.create_text(
        411.0,
        0.0,
        anchor="nw",
        text="Your Recipe",
        fill="#000000",
        font=("Inika Bold", 48 * -1)
    )

    canvas.create_text(
        92.0,
        117.0,
        anchor="nw",
        text="Ingredients",
        fill="#783000",
        font=("Inika Bold", 40 * -1)
    )

    canvas.create_text(
        97.0,
        381.0,
        anchor="nw",
        text="Instructions",
        fill="#783000",
        font=("Inika Bold", 40 * -1)
    )

    # Navigation button (placeholder)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=open_rating,
        relief="flat"
    )
    button_1.place(
        x=0.0,
        y=0.0,
        width=1095.0,
        height=64.0
    )

    # Make sure to keep references to images
    window.image_references = [image_image_1, button_image_1]
    
    window.resizable(False, False)
    window.mainloop()