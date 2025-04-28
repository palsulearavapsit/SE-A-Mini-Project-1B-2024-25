from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Frame, Label
import HomePage

class HistoryPage(tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\Poolify3\Tkinter-Designer-master\build\assets\frame0")

    def __init__(self,user_email):
        super().__init__()

        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")

        self.image_references = []  # Prevent garbage collection
        self.menu_frame = None  # Global frame reference
        self.user_email = user_email
        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        # Create the main canvas
        self.canvas = Canvas(self, bg="#FFFFFF", height=720, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Black frames and Poolify label
        self.canvas.create_rectangle(0, 0, 1280, 50, fill="#000000", outline="")
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        # Poolify Label
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -30), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", self.poolify)

        # Buttons for different details
        buttons = [
            ("Upcoming.png", 146, 90, self.create_details_window),
            ("Completed.png", 497, 90, self.create_details_window),
            ("Cancelled.png", 848, 90, self.create_details_window)
        ]

        # Create buttons dynamically
        for img_file, x, y, cmd in buttons:
            btn_img = PhotoImage(file=self.relative_to_assets(img_file))
            self.image_references.append(btn_img)  # Prevent garbage collection
            Button(self, image=btn_img, borderwidth=0, highlightthickness=0, relief="flat", bg="#FFFFFF",cursor="hand2",
                   command=cmd).place(x=x, y=y, width=310, height=80)

    def poolify(self, event=None):
        self.destroy()
        HomePage.HomePage(self.user_email)  # Replace with your HomePage module when needed

    def create_details_window(self):
        """Creates a menu frame with 15 labels while ensuring only one frame exists at a time."""
        if self.menu_frame is not None:
            self.menu_frame.destroy()

        self.menu_frame = Frame(self, bg="white", width=1280, height=480, bd=2, relief="solid",
                                highlightbackground="black", highlightcolor="black")
        self.menu_frame.place(x=0, y=205)

        self.create_back_button()  # Add the back button inside the menu_frame

        positions = [
            (3.0, 25.0), (428.0, 25.0), (853.0, 25.0),
            (3.0, 115.0), (428.0, 115.0), (853.0, 115.0),
            (3.0, 205.0), (428.0, 205.0), (853.0, 205.0),
            (3.0, 295.0), (428.0, 295.0), (853.0, 295.0),
            (3.0, 385.0), (428.0, 385.0), (853.0, 385.0)
        ]

        blank_img = PhotoImage(file=self.relative_to_assets("Blank.png"))
        self.image_references.append(blank_img)

        for x, y in positions:
            Label(self.menu_frame, image=blank_img, bg="white").place(x=x, y=y, width=420.0, height=70.0)

    def create_back_button(self):
        """Creates a back button that reliably destroys the current menu_frame."""

        def back():
            """Destroys the active menu frame."""
            if self.menu_frame is not None:
                self.menu_frame.destroy()

        back_img = PhotoImage(file=self.relative_to_assets("BB.png"))
        self.image_references.append(back_img)

        Button(self, image=back_img, borderwidth=0, highlightthickness=0, relief="flat",
               bg="white",cursor="hand2", command=back).place(x=6.0, y=90.0, width=44.0, height=48.0)

        self.canvas.create_text(48.0, 100.0, anchor="nw", text="Back", fill="#000000", font=("Poppins Medium", 24 * -1))


if __name__ == "__main__":
    user_email = "user@example.com"
    app = HistoryPage(user_email)
    app.resizable(False, False)
    app.mainloop()
