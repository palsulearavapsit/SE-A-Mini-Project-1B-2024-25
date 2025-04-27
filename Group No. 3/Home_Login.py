from pathlib import Path
import mysql.connector
from PIL import Image, ImageTk
import io
import subprocess
from tkinter import Tk, Canvas, Button, PhotoImage
from config import get_db_connection

# Import other pages
from Add_Recipe import open_uadd_page
from Search_Category import open_category_page
from Search_Ingredients import open_ingredients_page
from User_Account import open_user_page

# Path setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame11")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class AdSlideshow:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.ads = []
        self.current_ad = 0
        self.ad_images = []  # To keep references
        self.ad_item = None
        self.after_id = None
        self.load_ads()
        
    def load_ads(self):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT image FROM ads")
            self.ads = cursor.fetchall()
            cursor.close()
            connection.close()
            
            if not self.ads:
                self.load_default_ad()
            else:
                self.display_next_ad()
        except Exception as e:
            print(f"Error loading ads: {e}")
            self.load_default_ad()
    
    def load_default_ad(self):
        try:
            default_img = PhotoImage(file=relative_to_assets("image_2.png"))
            self.ad_item = self.canvas.create_image(
                self.x,
                self.y,
                image=default_img,
                anchor="center"
            )
            self.ad_images.append(default_img)  # Keep reference
        except Exception as e:
            print(f"Error loading default ad: {e}")
    
    def display_next_ad(self):
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            
        if not self.ads:
            return
            
        try:
            # Clear previous ad if exists
            if self.ad_item:
                self.canvas.delete(self.ad_item)
            
            # Get current ad image
            image_data = self.ads[self.current_ad % len(self.ads)][0]
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((686, 522))
            photo = ImageTk.PhotoImage(image)
            
            # Display new ad
            self.ad_item = self.canvas.create_image(
                self.x,
                self.y,
                image=photo,
                anchor="center"
            )
            self.ad_images.append(photo)  # Keep reference
            
            # Schedule next ad
            self.current_ad += 1
            self.after_id = self.canvas.after(2500, self.display_next_ad)  # 5 seconds
            
        except Exception as e:
            print(f"Error displaying ad: {e}")
            self.after_id = self.canvas.after(2500, self.display_next_ad)  # Try again

    def stop(self):
        if self.after_id:
            self.canvas.after_cancel(self.after_id)

def open_hlogin_page(previous_window, user_id):
    previous_window.destroy()
    
    def open_file(pyfile):
        # Stop the ad slideshow before navigating away
        if hasattr(window, 'ad_slideshow'):
            window.ad_slideshow.stop()
        window.destroy()
        subprocess.Popen(["python3", pyfile])

    window = Tk()
    window.geometry("1096x658")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=658,
        width=1096,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Background image
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(548.0, 329.0, image=image_image_1)
    canvas.image = image_image_1  # Keep reference

    # Initialize ad slideshow
    window.ad_slideshow = AdSlideshow(canvas, 393.0, 361.0)

    # Buttons
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.ad_slideshow.stop(), open_ingredients_page(window, user_id)],
        relief="flat"
    )
    button_1.place(x=787.0, y=210.0, width=310.0, height=65.0)
    canvas.button_image_1 = button_image_1  # Keep reference

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.ad_slideshow.stop(), open_uadd_page(window, user_id)],
        relief="flat"
    )
    button_2.place(x=787.0, y=329.0, width=310.0, height=65.0)
    canvas.button_image_2 = button_image_2  # Keep reference

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.ad_slideshow.stop(), open_category_page(window, user_id)],
        relief="flat"
    )
    button_3.place(x=787.0, y=449.0, width=310.0, height=65.0)
    canvas.button_image_3 = button_image_3  # Keep reference

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: [window.ad_slideshow.stop(), open_user_page(window, user_id)],
        relief="flat"
    )
    button_4.place(x=942.0, y=5.0, width=53.0, height=55.0)
    canvas.button_image_4 = button_image_4  # Keep reference

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: open_file("Homepage.py"),
        relief="flat"
    )
    button_5.place(x=1016.0, y=5.0, width=53.0, height=55.0)
    canvas.button_image_5 = button_image_5  # Keep reference

    def on_closing():
        window.ad_slideshow.stop()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.resizable(False, False)
    window.mainloop()