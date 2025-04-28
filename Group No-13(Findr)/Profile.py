from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from PIL import Image, ImageTk, ImageDraw
import io
from database import create_connection

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/Profile")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_profile_page(previous_window, user_id, user_name):
    previous_window.destroy()
    window = Tk()
    window.geometry("700x840")
    window.configure(bg="#FFFFFF")

    # Fetch user data including profile picture
    user_image_data = None
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT image FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if result and result[0]:
                user_image_data = result[0]
                print(f"Successfully fetched image data ({len(user_image_data)} bytes)")
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=840,
        width=700,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Background image
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    canvas.create_image(352.0, 422.0, image=image_image_1)

    # Profile picture display (90x90)
    PROFILE_SIZE = 90
    profile_x, profile_y = 354, 148  # Original coordinates

    # Create container frame for profile image
    profile_frame = Canvas(canvas, width=PROFILE_SIZE, height=PROFILE_SIZE, 
                         bg='white', highlightthickness=0)
    canvas.create_window(profile_x, profile_y, window=profile_frame)

    if user_image_data:
        try:
            # First try opening as normal image
            try:
                img = Image.open(io.BytesIO(user_image_data))
                print(f"Opened image: {img.format}, size: {img.size}")
            except:
                # If normal open fails, try treating as raw bytes
                from PIL import ImageFile
                ImageFile.LOAD_TRUNCATED_IMAGES = True
                img = Image.frombytes('RGB', (700, 840), user_image_data)
                print("Created image from raw bytes")

            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create circular mask
            mask = Image.new('L', (PROFILE_SIZE, PROFILE_SIZE), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, PROFILE_SIZE, PROFILE_SIZE), fill=255)
            
            # Resize and apply mask
            img = img.resize((PROFILE_SIZE, PROFILE_SIZE), Image.Resampling.LANCZOS)
            img.putalpha(mask)
            
            # Convert to PhotoImage and display
            profile_img = ImageTk.PhotoImage(img)
            profile_frame.create_image(PROFILE_SIZE//2, PROFILE_SIZE//2, image=profile_img)
            window.profile_img = profile_img
            print("Successfully displayed profile image")
            
        except Exception as e:
            print(f"Image processing error: {e}")
            # Fall back to default image
            default_img = PhotoImage(file=relative_to_assets("image_2.png"))
            profile_frame.create_image(PROFILE_SIZE//2, PROFILE_SIZE//2, image=default_img)
            window.default_img = default_img
    else:
        print("No profile image in database")
        default_img = PhotoImage(file=relative_to_assets("image_2.png"))
        profile_frame.create_image(PROFILE_SIZE//2, PROFILE_SIZE//2, image=default_img)
        window.default_img = default_img

    # Display user name
    canvas.create_text(
        326.0,
        205.0,
        anchor="nw",
        text=user_name,
        fill="#000000",
        font=("Urbanist Regular", 24 * -1)
    )

    # Navigation functions
    def open_home():
        from Home import open_home_page
        open_home_page(window, user_id, user_name)

    def open_regi():
        from Registration import open_regi_page
        open_regi_page(window, user_id, user_name)

    def open_login():
        from Login import open_login_page
        open_login_page(window)

    # Original buttons (all positions and sizes preserved)
    button_images = []
    for i in range(1, 8):
        button_image = PhotoImage(file=relative_to_assets(f"button_{i}.png"))
        button_images.append(button_image)
        setattr(window, f"button_image_{i}", button_image)

    button_1 = Button(image=button_images[0], borderwidth=0, command=open_login, relief="flat")
    button_1.place(x=68.0, y=712.0, width=568.0, height=70.0)

    button_2 = Button(image=button_images[1], borderwidth=0, command=lambda: print("button_2 clicked"), relief="flat")
    button_2.place(x=69.0, y=630.0, width=568.0, height=70.0)

    button_3 = Button(image=button_images[2], borderwidth=0, command=lambda: print("button_3 clicked"), relief="flat")
    button_3.place(x=67.0, y=465.0, width=569.0, height=70.0)

    button_4 = Button(image=button_images[3], borderwidth=0, command=lambda: print("button_4 clicked"), relief="flat")
    button_4.place(x=67.0, y=548.0, width=568.0, height=70.0)

    button_5 = Button(image=button_images[4], borderwidth=0, command=open_regi, relief="flat")
    button_5.place(x=69.0, y=305.0, width=567.7224731445312, height=70.0)

    button_6 = Button(image=button_images[5], borderwidth=0, command=lambda: print("button_6 clicked"), relief="flat")
    button_6.place(x=68.0, y=385.0, width=568.0, height=70.0)

    button_7 = Button(image=button_images[6], borderwidth=0, command=open_home, relief="flat")
    button_7.place(x=75.0, y=61.0, width=79.0, height=33.0)

    window.resizable(False, False)
    window.mainloop()