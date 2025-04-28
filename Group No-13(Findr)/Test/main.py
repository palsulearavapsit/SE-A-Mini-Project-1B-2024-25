import tkinter as tk
from login_page import open_login_page

def open_start_page():
    root = tk.Tk()
    root.title("Main Page")
    root.geometry("300x200")

    btn_start = tk.Button(root, text="Start Application", command=lambda: open_login_page(root))
    btn_start.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    open_start_page()