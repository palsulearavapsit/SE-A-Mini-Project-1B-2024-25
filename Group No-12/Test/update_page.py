import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from database import create_connection
import io

def open_update_page(previous_window, user_id, user_name):
    previous_window.destroy()
    
    root = tk.Tk()
    root.title("Update Info")
    root.geometry("400x500")

    # Constants
    PREVIEW_SIZE = 50  # 50x50 dimensions
    BG_COLOR = '#e0e0e0'  # Light gray background for empty preview
    BORDER_COLOR = '#a0a0a0'  # Border color for the preview area

    # Variables
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

    # Main frame
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Define entry fields as instance variables
    entry_name = tk.Entry(main_frame)
    entry_email = tk.Entry(main_frame)
    entry_phone = tk.Entry(main_frame)
    entry_address = tk.Text(main_frame, height=3)

    # Form fields
    fields = [
        ("Name:", entry_name, user_data[0]),
        ("Email:", entry_email, user_data[1]),
        ("Phone:", entry_phone, user_data[2] if user_data[2] else ""),
    ]
    
    for label, entry, value in fields:
        tk.Label(main_frame, text=label).pack(pady=(10, 0), anchor='w')
        entry.insert(0, value)
        entry.pack(fill=tk.X)

    tk.Label(main_frame, text="Address:").pack(pady=(10, 0), anchor='w')
    entry_address.insert("1.0", user_data[3] if user_data[3] else "")
    entry_address.pack(fill=tk.X)

    # Image preview section
    preview_frame = tk.Frame(main_frame)
    preview_frame.pack(pady=15)

    # Create 50x50 preview area with border
    preview_canvas = tk.Canvas(preview_frame, 
                             width=PREVIEW_SIZE+2, 
                             height=PREVIEW_SIZE+2,
                             bg=BORDER_COLOR,
                             highlightthickness=0)
    preview_canvas.pack()

    # This will be our image placeholder (50x50 inside the bordered canvas)
    preview_placeholder = tk.Canvas(preview_canvas, 
                                 width=PREVIEW_SIZE, 
                                 height=PREVIEW_SIZE,
                                 bg=BG_COLOR,
                                 highlightthickness=0)
    preview_canvas.create_window(1, 1, anchor='nw', window=preview_placeholder)

    # Image buttons below preview
    btn_frame = tk.Frame(preview_frame)
    btn_frame.pack(pady=(5, 0))

    def create_placeholder():
        """Create a 50x50 placeholder rectangle"""
        preview_placeholder.delete("all")
        preview_placeholder.create_rectangle(0, 0, PREVIEW_SIZE, PREVIEW_SIZE, 
                                          fill=BG_COLOR, outline='')

    def resize_image(img_data):
        """Resize image to fit exactly in 50x50 preview area"""
        img = Image.open(io.BytesIO(img_data))
        img = img.resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def upload_image():
        nonlocal image_data, image_preview
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    image_data = file.read()
                image_preview = resize_image(image_data)
                preview_placeholder.create_image(0, 0, image=image_preview, anchor='nw')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def remove_image():
        nonlocal image_data, image_preview
        image_data = None
        image_preview = None
        create_placeholder()

    btn_upload = tk.Button(btn_frame, text="Upload", command=upload_image, width=8)
    btn_upload.pack(side=tk.LEFT, padx=2)
    
    btn_remove = tk.Button(btn_frame, text="Remove", command=remove_image, width=8)
    btn_remove.pack(side=tk.LEFT, padx=2)

    # Initialize preview
    if user_data[4]:
        try:
            image_data = user_data[4]
            image_preview = resize_image(image_data)
            preview_placeholder.create_image(0, 0, image=image_preview, anchor='nw')
        except Exception as e:
            print(f"Error loading existing image: {e}")
            create_placeholder()
    else:
        create_placeholder()

    # Action buttons
    action_frame = tk.Frame(main_frame)
    action_frame.pack(pady=(20, 0))

    def update_info():
        name = entry_name.get()
        email = entry_email.get()
        phone = entry_phone.get()
        address = entry_address.get("1.0", tk.END).strip()
        
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
                elif image_preview is None and user_data[4]:
                    cursor.execute(
                        "UPDATE users SET name=%s, email=%s, phone=%s, address=%s, image=NULL WHERE id=%s",
                        update_values)
                else:
                    cursor.execute(
                        "UPDATE users SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s",
                        update_values)
                
                conn.commit()
                messagebox.showinfo("Success", "Information updated successfully!")
                from home_page import open_home_page
                open_home_page(root, user_id, name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update info: {str(e)}")
            finally:
                cursor.close()
                conn.close()

    btn_update = tk.Button(action_frame, text="Update", command=update_info, width=10)
    btn_update.pack(side=tk.LEFT, padx=5)

    def cancel():
        from home_page import open_home_page
        open_home_page(root, user_id, user_name)

    btn_cancel = tk.Button(action_frame, text="Cancel", command=cancel, width=10)
    btn_cancel.pack(side=tk.LEFT, padx=5)

    root.mainloop()