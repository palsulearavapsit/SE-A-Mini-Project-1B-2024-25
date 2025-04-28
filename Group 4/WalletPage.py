import tkinter as Tk
from tkinter import ttk, messagebox, Canvas, PhotoImage, Label
from pathlib import Path
import mysql.connector
from mysql.connector import Error
import HomePage
import CreateRide

class WalletApp(Tk.Tk):
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(
        r"C:\Users\Nikhil\PycharmProjects\Poolify3\Tkinter-Designer-master\build\assets\frame0"
    )

    def relative_to_assets(self, path: str) -> Path:
        """Helper method to handle relative paths for assets."""
        return self.ASSETS_PATH / Path(path)

    def __init__(self, user_email,user_type):
        super().__init__()
        self.title("Poolify App")
        self.geometry("1280x720")
        self.configure(bg="#FFFFFF")
        self.user_email = user_email
        self.user_type = user_type
        self.connection = self.create_db_connection()
        self.cursor = self.connection.cursor()
        self.create_ui()
        self.create_wallet_if_not_exists()
        self.fetch_balance()

    def poolify(self, event=None):
        self.destroy()
        HomePage.HomePage(self.user_email)

    def create_db_connection(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                database="carpooling_db",
                user="root",
                password="root"
            )
        except Error as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
            self.quit()

    def create_wallet_if_not_exists(self):
        """Create wallet if it does not exist for the logged-in user."""
        query = "SELECT wallet_id FROM Wallet WHERE email = %s"
        self.cursor.execute(query, (self.user_email,))
        result = self.cursor.fetchone()

        if not result:
            query = "INSERT INTO Wallet (email) VALUES (%s)"
            self.cursor.execute(query, (self.user_email,))
            self.connection.commit()
            messagebox.showinfo("Info", "Wallet created successfully for this email.")

    def fetch_balance(self):
        """Fetch and display the account balance."""
        query = "SELECT wallet_id FROM Wallet WHERE email = %s"
        self.cursor.execute(query, (self.user_email,))
        result = self.cursor.fetchone()

        if result:
            wallet_id = result[0]
            query = """
                   SELECT SUM(CASE WHEN transaction_type = 'credit' THEN amount ELSE -amount END) AS balance
                   FROM WalletTransactions WHERE wallet_id = %s
               """
            self.cursor.execute(query, (wallet_id,))
            result = self.cursor.fetchone()
            balance = result[0] if result[0] is not None else 0.0
            self.balance_label.config(text=f"${balance:.2f}")
        else:
            self.balance_label.config(text="No wallet found.")

    def deposit(self):
        """Add money to the wallet."""
        amount = self.deposit_entry.get().strip()
        if not amount or not amount.isdigit() or float(amount) <= 0:
            messagebox.showerror("Error", "Please enter a valid deposit amount.")
            return

        query = "SELECT wallet_id FROM Wallet WHERE email = %s"
        self.cursor.execute(query, (self.user_email,))
        result = self.cursor.fetchone()

        if result:
            wallet_id = result[0]
            query = "INSERT INTO WalletTransactions (email, wallet_id, transaction_type, amount) VALUES ( %s, %s, 'credit', %s)"
            self.cursor.execute(query, (self.user_email, wallet_id, float(amount)))
            self.connection.commit()
            messagebox.showinfo("Success", "Amount deposited successfully.")
            self.deposit_entry.delete(0, Tk.END)
            self.fetch_balance()

    def view_transaction_history(self):
        if hasattr(self, "transaction_frame"):
            self.transaction_frame.destroy()

        self.transaction_frame = Tk.Frame(self, bg="white", width=820, height=510)
        self.transaction_frame.place(x=640, y=65)

        self.transaction_button = Tk.Button(
            self.transaction_frame,
            text="View Transactions",
            font=("Arial", 14),
            bg="black",
            fg="white",
            command=self.view_transaction_history
        )
        self.transaction_button.place(x=170, y=1, width=340, height=30)

        tree = ttk.Treeview(self.transaction_frame, columns=("type", "amount", "date"), show="headings", height=20)
        tree.heading("type", text="Type")
        tree.heading("amount", text="Amount")
        tree.heading("date", text="Date")
        tree.place(x=10, y=35, width=620, height=470)

        try:
            self.cursor.execute("SELECT wallet_id FROM Wallet WHERE email = %s", (self.user_email,))
            result = self.cursor.fetchone()

            if result:
                wallet_id = result[0]
                self.cursor.execute(
                    "SELECT transaction_type, amount, created_at FROM WalletTransactions WHERE wallet_id = %s ORDER BY created_at DESC",
                    (wallet_id,)
                )
                transactions = self.cursor.fetchall()
                for transaction in transactions:
                    tree.insert("", Tk.END, values=transaction)
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    def create_ui(self):
        self.canvas = Canvas(self, bg="white", height=720, width=1280)
        self.canvas.place(x=0, y=0)

        # Create the top and bottom rectangles
        self.canvas.create_rectangle(0, 0, 1280, 60, fill="#000000", outline="")
        self.canvas.create_rectangle(0, 696, 1280, 721, fill="#000000", outline="")
        poolify_label = Label(self, text="POOLIFY", fg="white", bg="#000000",
                              font=("Italiana Regular", -36), cursor="hand2")
        poolify_label.place(x=15, y=9)
        poolify_label.bind("<Button-1>", self.poolify)
        # Transaction and other frames
        self.canvas.create_rectangle(638, 49, 640, 584, fill="#000000", outline="")
        self.canvas.create_rectangle(-1, 583, 640, 584, fill="#000000", outline="")
        self.canvas.create_rectangle(639, 583, 1280, 585, fill="#000000", outline="")
        # self.canvas.create_text(647, 58, anchor="nw", text="Transactions", fill="#414141",
        #                         font=("Poppins SemiBold", -16))


        # Transaction Frame
        self.transaction_frame = Tk.Frame(self, bg="white", width=820, height=510)
        self.transaction_frame.place(x=640, y=65)

        self.transaction_button = Tk.Button(
            self.transaction_frame,
            text="View Transactions",
            font=("Arial", 14),
            bg="black",
            fg="white",
            command=self.view_transaction_history
        )
        self.transaction_button.place(x=170, y=1, width=340, height=30)

        # Transaction Treeview
        self.transaction_tree = ttk.Treeview(self.transaction_frame, columns=("type", "amount", "date"),
                                             show="headings", height=20)
        self.transaction_tree.heading("type", text="Type")
        self.transaction_tree.heading("amount", text="Amount")
        self.transaction_tree.heading("date", text="Date")

        # Place the treeview inside the transaction_frame with specific positioning
        self.transaction_tree.place(x=10, y=35, width=620, height=470)

        # Loading the background images for the UI
        self.image_objects = []  # Store references to prevent garbage collection

        for img, x, y in [("TotalSpent.png", 480, 196), ("AvailableBalance.png", 200, 196)]:
            img_obj = PhotoImage(file=self.relative_to_assets(img))
            self.image_objects.append(img_obj)  # Keep a reference
            self.canvas.create_image(x, y, image=img_obj)

        # Buttons
        buttons = [
            {"file": "Addmoney.png", "x": 212, "y": 420, "w": 171, "h": 54},
        ]

        for i, btn in enumerate(buttons, start=1):
            btn_image = PhotoImage(file=self.relative_to_assets(btn["file"]))
            # Since we only have one button, directly assign the deposit function
            command = self.deposit

            Tk.Button(
                image=btn_image, borderwidth=0, highlightthickness=0,
                command=command, relief="flat"
            ).place(x=btn["x"], y=btn["y"], width=btn["w"], height=btn["h"])
            globals()[f"button_image_{i}"] = btn_image  # Keep references to images

        # Balance label
        self.balance_label = Tk.Label(self, text="Loading...", font=("Arial", 16), bg="black", fg="white")
        self.balance_label.place(x=155, y=160)

        # Deposit input field and label
        self.deposit_label = Tk.Label(self, text="Deposit Amount:", font=("Arial", 14), bg="white", fg="#333333")
        self.deposit_label.place(x=50, y=350)
        entry_image_1 = PhotoImage(file=self.ASSETS_PATH / "EntryImage.png")
        entry_bg_1 = self.canvas.create_image(220.0, 350.0, image=entry_image_1)
        self.deposit_entry = ttk.Entry(self, font=("Arial", 14))
        self.deposit_entry.place(x=220, y=350, width=200)

        self.back_button = ttk.Button(self, text="← Back", command=self.go_home_back)
        self.back_button.place(x=5, y=65)

    def go_home_back(self):
        self.destroy()
        if self.user_type == "driver":
            import DriverHomePage
            DriverHomePage.HomePage(self.user_email)
        else:  # passenger
            import HomePage
            HomePage.HomePage(self.user_email)


if __name__ == "__main__":
    user_email = "user@example.com"  # Replace with actual user's email
    user_type = "user"
    app = WalletApp(user_email,user_type)
    app.resizable(False, False)
    app.mainloop()
