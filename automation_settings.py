import customtkinter as ctk
import json


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)


class AutomationSettingsGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Automation Settings")
        self.root.geometry("600x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create scrollable frame
        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Directory selection
        self.dir_frame = ctk.CTkFrame(self.scrollable_frame)
        self.dir_frame.pack(pady=10, padx=10, fill="x")

        self.dir_label = ctk.CTkLabel(self.dir_frame, text="Screenshot Directory:")
        self.dir_label.pack(side="left", padx=5)

        self.dir_entry = ctk.CTkEntry(self.dir_frame, width=300)
        self.dir_entry.pack(side="left", padx=5)
        self.dir_entry.insert(0, "C:/Users/Muzna/Pictures/Screenshots")

        self.dir_button = ctk.CTkButton(
            self.dir_frame, text="Browse", command=self.browse_directory
        )
        self.dir_button.pack(side="left", padx=5)

        # Boolean toggles
        self.bool_frame = ctk.CTkFrame(self.scrollable_frame)
        self.bool_frame.pack(pady=10, padx=10, fill="x")

        self.bool_vars = {
            "msg_show": ctk.BooleanVar(value=False),
            "twilio_destroy": ctk.BooleanVar(value=False),
            "tab_close": ctk.BooleanVar(value=False),
            "Whatsapp_msg_send": ctk.BooleanVar(value=False),
        }

        for i, (key, var) in enumerate(self.bool_vars.items()):
            switch = ctk.CTkSwitch(self.bool_frame, text=key, variable=var)
            switch.grid(row=i // 2, column=i % 2, pady=5, padx=10, sticky="w")

        # Template name
        self.template_frame = ctk.CTkFrame(self.scrollable_frame)
        self.template_frame.pack(pady=10, padx=10, fill="x")

        self.template_label = ctk.CTkLabel(self.template_frame, text="Template Name:")
        self.template_label.pack(side="left", padx=5)

        self.template_entry = ctk.CTkEntry(self.template_frame, width=300)
        self.template_entry.pack(side="left", padx=5)
        self.template_entry.insert(0, "Enter Template Name")

        # Numeric inputs
        self.num_frame = ctk.CTkFrame(self.scrollable_frame)
        self.num_frame.pack(pady=10, padx=10, fill="x")

        self.num_vars = {
            "number_of_tabs": ctk.StringVar(value="80"),
            "starting_delay": ctk.StringVar(value="4"),
            "general_pause": ctk.StringVar(value="0.4"),
            "main_page_refresh_delay": ctk.StringVar(value="0"),
            "msg_page_refresh_delay": ctk.StringVar(value="5"),
            "template_selection_delay": ctk.StringVar(value="0.4"),
            "screenshot_delay": ctk.StringVar(value="3"),
        }

        for i, (key, var) in enumerate(self.num_vars.items()):
            label = ctk.CTkLabel(self.num_frame, text=f"{key}:")
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")
            entry = ctk.CTkEntry(self.num_frame, textvariable=var, width=100)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")

        # Second page numeric inputs
        self.num_frame2 = ctk.CTkFrame(self.scrollable_frame)
        self.num_frame2.pack(pady=10, padx=10, fill="x")

        self.num_vars2 = {
            "scroll_amount": ctk.StringVar(value="-600"),
            "delay_after_first_click_on_profile": ctk.StringVar(value="1"),
            "delay_after_every_msg": ctk.StringVar(value="1"),
            "delay_for_msg_loading": ctk.StringVar(value="3"),
            "delay_for_scrolling": ctk.StringVar(value="0.5"),
            "delay_for_next_page": ctk.StringVar(value="4"),
        }

        ctk.CTkLabel(self.num_frame2, text="Second Page Settings:").grid(
            row=0, column=0, columnspan=2, pady=5, padx=10, sticky="w"
        )

        for i, (key, var) in enumerate(self.num_vars2.items(), start=1):
            label = ctk.CTkLabel(self.num_frame2, text=f"{key}:")
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")
            entry = ctk.CTkEntry(self.num_frame2, textvariable=var, width=100)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")

        # Save button
        self.save_button = ctk.CTkButton(
            self.scrollable_frame, text="Save Settings", command=self.save_settings
        )
        self.save_button.pack(pady=20)

    def browse_directory(self):
        directory = ctk.filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, ctk.END)
            self.dir_entry.insert(0, directory)

    def save_settings(self):
        settings = {
            "screenshot_directory": self.dir_entry.get(),
            "template_name": self.template_entry.get(),
            "boolean_settings": {k: v.get() for k, v in self.bool_vars.items()},
            "numeric_settings": {k: float(v.get()) for k, v in self.num_vars.items()},
            "numeric_settings_page2": {
                k: float(v.get()) for k, v in self.num_vars2.items()
            },
        }

        with open("automation_settings.json", "w") as f:
            json.dump(settings, f, indent=4)

        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AutomationSettingsGUI()
    app.run()
