import tkinter as tk
from update_page import open_update_page

def open_home_page(previous_window, user_id, user_name):
    previous_window.destroy()
    
    root = tk.Tk()
    root.title("Home")
    root.geometry("400x300")

    greeting = tk.Label(root, text=f"Hello {user_name}!", font=("Arial", 16))
    greeting.pack(pady=(50, 20))

    btn_update = tk.Button(root, text="Update Info", command=lambda: open_update_page(root, user_id, user_name))
    btn_update.pack(pady=(10, 0))

    root.mainloop()