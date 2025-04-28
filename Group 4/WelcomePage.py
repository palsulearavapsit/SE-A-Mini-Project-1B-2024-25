from pathlib import Path
import tkinter as tk
from tkinter import Canvas, PhotoImage, Button
import SignUp
import LoginPage
import AdminLogin

class WelcomePage(tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\Poolify3\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self):
        super().__init__()

        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")

        self.image_references = []  # Prevent garbage collection
        self.setup_ui()

    def signup_page(self):
        self.destroy()
        SignUp.SignupPage()

    def login_page(self):
        self.destroy()
        LoginPage.LoginPage()

    def admin_page(self):
        self.destroy()
        AdminLogin.AdminLoginPage()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_text(self, canvas, x, y, text, font_size, anchor="nw", fill="#000000"):
        canvas.create_text(x, y, anchor=anchor, text=text, fill=fill, font=("Italiana Regular", font_size * -1))

    def create_image(self, canvas, x, y, image_file):
        image_image = PhotoImage(file=self.relative_to_assets(image_file))
        canvas.create_image(x, y, image=image_image)
        return image_image  # Return the image so that it persists

    def about_us(self):
        print("About Us button clicked!")

    def setup_ui(self):
        # Setup Canvas
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Draw Rectangles
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 50.0, fill="#000000", outline="")
        self.canvas.create_rectangle(0.0, 696.0, 1280.0, 721.0, fill="#000000", outline="")

        self.canvas.create_text(15, 9, anchor="nw", text="POOLIFY", fill="#FFFFFF", font=("Italiana Regular", -30))

        # Create Text
        self.create_text(self.canvas, 100.0, 177.0, "Your Smart", 48, fill="#1E1E1E")
        self.create_text(self.canvas, 50.0, 240.0, "Commute Solution", 48, fill="#1E1E1E")

        self.create_text(self.canvas, 104.0, 390.0, "Find a ride", 36, fill="#000000")
        self.create_text(self.canvas, 650.0, 635.0, "There’s a Poolify ride for everyone", 40, fill="#000000")

        # Image
        self.Greeen_car = PhotoImage(file=self.relative_to_assets("CarSurrounding.png"))
        self.canvas.create_image(920.0, 350.0, image=self.Greeen_car)

        # About Us Button
        self.about_us_button = Button(
            text="About Us",
            command=self.about_us,  # This will call the about_us() method when clicked
            bd=0,
            fg="#FFFFFF",
            bg="#000000",
            font=("Italiana Regular", 20 * -1),
            relief="flat",
            highlightthickness=0,
            activebackground="#000000",
            activeforeground="#FFFFFF"
        )
        self.about_us_button.place(x=1179.0, y=10.0)

        create_account = PhotoImage(file=self.relative_to_assets("CreateAccount.png"))
        self.button_1 = Button(image=create_account, borderwidth=0,cursor="hand2", command=self.signup_page,highlightthickness=0, relief="flat", bg="#FFFFFF")
        self.button_1.place(x=100.0, y=470.0, width=340.0, height=54)
        self.button_image_1 = create_account  # Keep reference

        login_button = PhotoImage(file=self.relative_to_assets("LogInAccount.png"))
        self.button_2 = Button(image=login_button, borderwidth=0,cursor="hand2", highlightthickness=0,
                               command=self.login_page, relief="flat")
        self.button_2.place(x=100.0, y=550.0, width=340.0, height=54.0)
        self.button_image_2 = login_button  # Keep reference

        button_image_3 = PhotoImage(file=self.relative_to_assets("Admin_button.png"))
        self.button_3 = Button(image=button_image_3, borderwidth=0, cursor="hand2", highlightthickness=0,
                               command=self.admin_page,
                               relief="flat", bg="#FFFFFF")
        self.button_3.place(x=100.0, y=630.0, width=340.0, height=54)
        self.button_image_3 = button_image_3


if __name__ == "__main__":
    app = WelcomePage()
    app.resizable(False, False)
    app.mainloop()
