import customtkinter as ctk
from PIL import Image, ImageTk
import os

class WelcomePage(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.master = master
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Main container with gradient background
        container = ctk.CTkFrame(
            self, 
            fg_color=("#2C2C2C", "#2C2C2C"),
            corner_radius=0
        )
        container.pack(fill="both", expand=True)

        # Create a centered content frame
        content_frame = ctk.CTkFrame(
            container, 
            fg_color="transparent",
            corner_radius=0
        )
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Try to load logo (replace with your actual logo path)
        try:
            logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'logo.png')
            logo_image = ctk.CTkImage(
                Image.open(logo_path), 
                size=(200, 200)
            )
            logo_label = ctk.CTkLabel(
                content_frame, 
                image=logo_image, 
                text=""
            )
            logo_label.pack(pady=(0, 20))
        except Exception:
            # Fallback text if logo can't be loaded
            ctk.CTkLabel(
                content_frame,
                text="EduQuest",
                font=ctk.CTkFont(size=48, weight="bold"),
                text_color="white"
            ).pack(pady=(0, 10))

        # Tagline
        ctk.CTkLabel(
            content_frame,
            text="Master Your Exams, Elevate Your Future",
            font=ctk.CTkFont(size=20, weight="normal"),
            text_color=("#E0E0E0", "#E0E0E0")
        ).pack(pady=(0, 40))

        # Buttons frame with improved styling
        buttons_frame = ctk.CTkFrame(
            content_frame, 
            fg_color="transparent"
        )
        buttons_frame.pack(pady=20)

        # Login button with icon-like effect
        login_btn = ctk.CTkButton(
            buttons_frame,
            text="Login",
            command=self.app.show_login_page,
            width=250,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#2CC985", "#2CC985"),
            hover_color=("#25A36F", "#25A36F"),
            corner_radius=15,
            border_width=2,
            border_color=("white", "white")
        )
        login_btn.pack(pady=(0, 20))

        # Create Account button with different style
        create_account_btn = ctk.CTkButton(
            buttons_frame,
            text="Create Account",
            command=self.app.show_create_account_page,
            width=250,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="transparent",
            hover_color=("#3C3C3C", "#3C3C3C"),
            text_color=("white", "white"),
            border_width=2,
            border_color=("#2CC985", "#2CC985"),
            corner_radius=15
        )
        create_account_btn.pack()

        # Footer with version and subtle styling
        footer_frame = ctk.CTkFrame(
            container, 
            fg_color="transparent"
        )
        footer_frame.pack(side="bottom", pady=20)

        ctk.CTkLabel(
            footer_frame,
            text="Version 1.0 | © 2024 EduQuest",
            font=ctk.CTkFont(size=12),
            text_color=("#A0A0A0", "#A0A0A0")
        ).pack()

        # Optional: Add a subtle animation or hover effect
        login_btn.bind("<Enter>", lambda e: self.on_button_hover(login_btn))
        login_btn.bind("<Leave>", lambda e: self.on_button_leave(login_btn))
        create_account_btn.bind("<Enter>", lambda e: self.on_button_hover(create_account_btn))
        create_account_btn.bind("<Leave>", lambda e: self.on_button_leave(create_account_btn))

    def on_button_hover(self, button):
        """Add subtle effect on hover"""
        button.configure(border_width=3)

    def on_button_leave(self, button):
        """Reset button"""
        button.configure(border_width=2)