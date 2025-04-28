def create_appearance_section(self):
    # ... existing code
    
    # REMOVE TOGGLE SWITCHES like this:
    # dark_mode_var = ctk.BooleanVar(value=True)
    # dark_mode_switch = ctk.CTkSwitch(
    #     appearance_frame,
    #     text="Dark Mode",
    #     variable=dark_mode_var,
    #     command=self.toggle_theme,
    #     onvalue=True,
    #     offvalue=False
    # )
    # dark_mode_switch.pack(anchor="w", padx=20, pady=10)
    
    # Instead, you can use static text if needed:
    theme_label = ctk.CTkLabel(
        appearance_frame,
        text="Dark Mode Enabled",
        font=ctk.CTkFont(size=14),
        text_color="#aaaaaa"
    )
    theme_label.pack(anchor="w", padx=20, pady=10) 