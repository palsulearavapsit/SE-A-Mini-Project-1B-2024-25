from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, OptionMenu

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\Chat")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_Chat_page(previous_window, user_id, user_name):
    previous_window.destroy()

    # Create a dictionary of questions and answers
    qa_pairs = {
        "What are the payment methods you accept?": "We accept credit cards, PayPal, and bank transfers.",
        "How long does it take to respond to inquiries?": "We typically respond within 24 hours.",
        "Do I need to provide any materials for the service?": "It depends on the service. We'll inform you if needed.",
        "Can I book multiple services at once?": "Yes, you can book multiple services simultaneously.",
        "Can I choose a specific service provider?": "Yes, you can request a preferred provider."
    }

    def open_home():
        from Home import open_home_page
        open_home_page(window,user_id,user_name)

    def on_question_select(*args):
        selected_question = question_var.get()
        answer = qa_pairs.get(selected_question, "")
        entry_2.delete(0, "end")
        entry_2.insert(0, answer)

    window = Tk()
    window.geometry("700x840")
    window.configure(bg="#FFFFFF")

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

    # Create a variable for the selected question
    question_var = StringVar(window)
    question_var.set("Select a question")  # default value

    # For Python 3.13+ compatibility, we'll use trace_add instead of trace
    question_var.trace_add("write", on_question_select)

    # Replace the Text widget with an OptionMenu for questions
    question_menu = OptionMenu(
        window,
        question_var,
        *qa_pairs.keys()
    )
    question_menu.config(
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        borderwidth=0,
        activebackground="#D9D9D9",
        activeforeground="#000716",
        font=("Arial", 12)
    )
    question_menu.place(
        x=35.0,
        y=618.0,
        width=631.0,
        height=57.0
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(
        x=2.0,
        y=719.0,
        width=700.0,
        height=121.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(
        x=603.0,
        y=758.0,
        width=49.0,
        height=49.0
    )

    canvas.create_text(
        14.0,
        90.0,
        anchor="nw",
        text="Chat",
        fill="#000000",
        font=("RoundedMplus1c Bold", 40 * -1)
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(
        x=0.0,
        y=0.0,
        width=700.0,
        height=76.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(
        x=33.0,
        y=19.0,
        width=77.0,
        height=31.0
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        636.0,
        33.0,
        image=image_image_1
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_5 clicked"),
        relief="flat"
    )
    button_5.place(
        x=408.0,
        y=758.0,
        width=49.0,
        height=49.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=open_home,
        relief="flat"
    )
    button_6.place(
        x=43.0,
        y=760.0,
        width=49.0,
        height=49.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_7 clicked"),
        relief="flat"
    )
    button_7.place(
        x=214.0,
        y=760.0,
        width=49.0,
        height=49.0
    )

    canvas.create_text(
        567.0,
        102.0,
        anchor="nw",
        text="Hello!",
        fill="#000000",
        font=("Urbanist Medium", 36 * -1)
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        185.0,
        117.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        653.0,
        648.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        349.0,
        202.0,
        image=image_image_4
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        350.5,
        347.0,
        image=entry_image_2
    )
    entry_2 = Entry(   #Answer
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0,
        font=("Arial", 12)
    )
    entry_2.place(
        x=25.0,
        y=317.0,
        width=651.0,
        height=58.0
    )

    canvas.create_rectangle(
        -2.0,
        152.0,
        700.0,
        154.0,
        fill="#000000",
        outline="")

    window.resizable(False, False)
    window.mainloop()