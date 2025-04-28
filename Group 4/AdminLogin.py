import mysql.connector
import tkinter as Tk
from tkinter import messagebox, Canvas, PhotoImage, Button, Entry, Label
from pathlib import Path
from PIL import Image, ImageTk
import Admin_Page
import WelcomePage

class AdminLoginPage(Tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\Poolify\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self):
        super().__init__()
        self.title("Admin Login Page")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def poolify(self, event=None):
        self.destroy()  # Destroys the current window or frame
        WelcomePage.WelcomePage()

    def create_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="carpooling_db"
        )

    def verify_login(self, in_userid, in_password):
        conn = self.create_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE admin_id = %s AND password = %s", (in_userid, in_password))
        result = cursor.fetchone()
        conn.close()
        return result

    def on_login(self):
        in_userid = self.userid.get().strip()
        in_password = self.password.get().strip()

        if self.verify_login(in_userid, in_password):
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.destroy()
            admin_page = Admin_Page.AdminDashboard(in_userid)
            admin_page.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid AdminID or password")

    def setup_ui(self):
        canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Load and display image
        image_path = r"C:\Users\Nikhil\OneDrive\Pictures\poolify\Blue_half_page.png"
        image = Image.open(image_path)
        image_1 = ImageTk.PhotoImage(image)
        canvas.create_image(950.0, 377.0, image=image_1)
        self.image_1 = image_1  # Keep reference

        # Black frames and text
        canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        canvas.create_text(51.0, 92.0, anchor="nw", text="Welcome back, Admin!", fill="#000000",
                           font=("Poppins Medium", 32 * -1))
        canvas.create_text(51.0, 150.0, anchor="nw", text="Enter your Credentials to access the admin panel",
                           fill="#000000", font=("Poppins Medium", 16 * -1))
        # Poolify Label
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -30), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", self.poolify)

        # Entry fields and labels
        canvas.create_text(51.0, 203.0, anchor="nw", text="Admin ID", fill="#000000",
                           font=("Poppins Medium", 14 * -1))
        canvas.create_text(55.0, 282.0, anchor="nw", text="Password", fill="#000000", font=("Poppins Medium", 14 * -1))

        entry_image = PhotoImage(file=self.relative_to_assets("EntryImage1.png"))
        canvas.create_image(253.0, 324.0, image=entry_image)
        canvas.create_image(249.0, 245.0, image=entry_image)
        self.entry_image = entry_image  # Keep reference

        self.userid = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("Poppins Medium", 15))
        self.userid.place(x=57.0, y=229.0, width=384.0, height=30.0)

        self.password = Entry(bd=0, bg="#FFFFFF", fg="#000716", show="*", highlightthickness=0, font=("Poppins Medium", 15))
        self.password.place(x=61.0, y=308.0, width=384.0, height=30.0)

        # Login Button
        button_image_1 = PhotoImage(file=self.relative_to_assets("Login.png"))
        self.button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, cursor="hand2", command=self.on_login,
                               relief="flat", bg="#FFFFFF")
        self.button_1.place(x=51.0, y=396.0, width=404.0, height=35)
        self.button_image_1 = button_image_1  # Keep reference


if __name__ == "__main__":
    app = AdminLoginPage()
    app.resizable(False, False)
    app.mainloop()