from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, filedialog
from PIL import Image, ImageTk
import io
from database import create_connection

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/Registration")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_regi_page(previous_window, user_id, user_name):
    previous_window.destroy()
    window = Tk()

    window.geometry("700x840")
    window.configure(bg="#FFFFFF")

    # Variables to store image data
    image_data = None
    image_preview = None

    # Fetch user data
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, phone, address, image FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
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
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        350.0,
        420.0,
        image=image_image_1
    )

    # Phone field (entry_1)
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        168.5,
        508.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=32.0,
        y=490.0,
        width=273.0,
        height=35.0
    )
    entry_1.insert(0, user_data[2] if user_data[2] else "")  # Phone

    # Address field (entry_2) - Changed from email to address
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        273.5,
        397.5,
        image=entry_image_2
    )
    entry_2 = Text(  # Changed from Entry to Text for multi-line address
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=31.0,
        y=379.0,
        width=485.0,
        height=35.0
    )
    entry_2.insert("1.0", user_data[3] if user_data[3] else "")  # Address

    # Name field (entry_3)
    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        207.5,
        286.5,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=31.0,
        y=268.0,
        width=353.0,
        height=35.0
    )
    entry_3.insert(0, user_data[0])  # Name

    # Image display area (using the existing image_2 element)
    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        591.0,
        230.0,
        image=image_image_2
    )

    # Function to handle image display
    def display_image(img_data):
        nonlocal image_preview
        try:
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            image_preview = ImageTk.PhotoImage(img)
            canvas.itemconfig(image_2, image=image_preview)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image: {str(e)}")

    # Load existing image if available
    if user_data[4]:
        image_data = user_data[4]
        display_image(image_data)

    # Email field (entry_4) - Changed from address to email
    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        203.5,
        633.5,
        image=entry_image_4
    )
    entry_4 = Entry(  # Changed from Text to Entry for single-line email
        bd=0,
        bg="#EDEDED",
        fg="#000716",
        highlightthickness=0
    )
    entry_4.place(
        x=27.0,
        y=615.0,
        width=353.0,
        height=35.0
    )
    entry_4.insert(0, user_data[1])  # Email

    def upload_image():
        nonlocal image_data
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    image_data = file.read()
                display_image(image_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def update_info():
        name = entry_3.get()
        email = entry_4.get()  # Now getting email from entry_4
        phone = entry_1.get()
        address = entry_2.get("1.0", "end-1c")  # Now getting address from entry_2
        
        if not name or not email:
            messagebox.showerror("Error", "Name and Email are required")
            return
            
        conn = create_connection()
        if conn is not None:
            try:
                cursor = conn.cursor()
                update_values = (name, email, phone, address, user_id)
                
                if image_data is not None:
                    cursor.execute(
                        "UPDATE users SET name=%s, email=%s, phone=%s, address=%s, image=%s WHERE id=%s",
                        (*update_values[:4], image_data, update_values[4]))
                else:
                    cursor.execute(
                        "UPDATE users SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s",
                        update_values)
                
                conn.commit()
                messagebox.showinfo("Success", "Information updated successfully!")
                from Home import open_home_page
                open_home_page(window, user_id, name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update info: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    def cancel():
        from Home import open_home_page
        open_home_page(window, user_id, user_name)

    # Update button
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=update_info,
        relief="flat"
    )
    button_1.place(
        x=101.0,
        y=727.0,
        width=187.0,
        height=47.0
    )

    # Cancel button
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=cancel,
        relief="flat"
    )
    button_2.place(
        x=404.0,
        y=727.0,
        width=187.0,
        height=47.0
    )

    # Add image upload functionality to the existing image area
    canvas.tag_bind(image_2, "<Button-1>", lambda e: upload_image())

    window.resizable(False, False)
    window.mainloop()