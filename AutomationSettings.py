# Imports

import customtkinter as ctk
from json import load, dump


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)


class AutomationSettingsGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Automation Settings")
        self.root.geometry("600x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.settings = self.load_settings()

        # Create scrollable frame
        self.scrollable_frame = ScrollableFrame(self.root)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.create_widgets()

    def load_settings(self):
        try:
            with open("automation_settings.json", "r") as f:
                return load(f)
        except FileNotFoundError:
            return None

    def create_widgets(self):
        # Directory selection
        self.dir_frame = ctk.CTkFrame(self.scrollable_frame)
        self.dir_frame.pack(pady=10, padx=10, fill="x")

        self.dir_label = ctk.CTkLabel(self.dir_frame, text="Screenshot Directory:")
        self.dir_label.pack(side="left", padx=5)

        self.dir_entry = ctk.CTkEntry(self.dir_frame, width=300)
        self.dir_entry.pack(side="left", padx=5)
        self.dir_entry.insert(
            0,
            (
                self.settings.get(
                    "screenshot_directory", "C:/Users/Muzna/Pictures/Screenshots"
                )
                if self.settings
                else "C:/Users/Muzna/Pictures/Screenshots"
            ),
        )

        self.dir_button = ctk.CTkButton(
            self.dir_frame, text="Browse", command=self.browse_directory
        )
        self.dir_button.pack(side="left", padx=5)

        # Boolean toggles
        self.bool_frame = ctk.CTkFrame(self.scrollable_frame)
        self.bool_frame.pack(pady=10, padx=10, fill="x")

        self.bool_vars = {
            "msg_show": ctk.BooleanVar(
                value=(
                    self.settings["boolean_settings"]["msg_show"]
                    if self.settings and "boolean_settings" in self.settings
                    else False
                )
            ),
            "tab_close": ctk.BooleanVar(
                value=(
                    self.settings["boolean_settings"]["tab_close"]
                    if self.settings and "boolean_settings" in self.settings
                    else False
                )
            ),
            "Whatsapp_msg_send": ctk.BooleanVar(
                value=(
                    self.settings["boolean_settings"]["Whatsapp_msg_send"]
                    if self.settings and "boolean_settings" in self.settings
                    else False
                )
            ),
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
        self.template_entry.insert(
            0,
            (
                self.settings.get("template_name", "Enter Template Name")
                if self.settings
                else "Enter Template Name"
            ),
        )

        self.email_label = ctk.CTkLabel(self.template_frame, text="Email:")
        self.email_label.pack(side="left", padx=5)

        self.email_entry = ctk.CTkEntry(self.template_frame, width=300)
        self.email_entry.pack(side="left", padx=5)
        self.email_entry.insert(
            0,
            (
                self.settings.get("email_name", "Enter Your Email")
                if self.settings
                else "Enter Your Email"
            ),
        )

        # Numeric inputs
        self.num_frame = ctk.CTkFrame(self.scrollable_frame)
        self.num_frame.pack(pady=10, padx=10, fill="x")

        self.num_vars = {
            "number_of_tabs": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["number_of_tabs"])
                    if self.settings and "numeric_settings" in self.settings
                    else "80"
                )
            ),
            "starting_delay": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["starting_delay"])
                    if self.settings and "numeric_settings" in self.settings
                    else "4"
                )
            ),
            "general_pause": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["general_pause"])
                    if self.settings and "numeric_settings" in self.settings
                    else "0.4"
                )
            ),
            "main_page_refresh_delay": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["main_page_refresh_delay"])
                    if self.settings and "numeric_settings" in self.settings
                    else "0"
                )
            ),
            "msg_page_refresh_delay": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["msg_page_refresh_delay"])
                    if self.settings and "numeric_settings" in self.settings
                    else "5"
                )
            ),
            "msg_box_selection_delay": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["msg_box_selection_delay"])
                    if self.settings and "numeric_settings" in self.settings
                    else "0.0"
                )
            ),
            "template_selection_delay": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings"]["template_selection_delay"])
                    if self.settings and "numeric_settings" in self.settings
                    else "0.4"
                )
            ),
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
            "scroll_amount": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["scroll_amount"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "-600"
                )
            ),
            "profiles_to_check": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["profiles_to_check"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "2"
                )
            ),
            "distance_to_msg": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["distance_to_msg"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "780"
                )
            ),
            "purple_threshold": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["purple_threshold"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "0.1"
                )
            ),
            "grey_threshold": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["grey_threshold"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "0.19"
                )
            ),
            "delay_after_first_click_on_profile": ctk.StringVar(
                value=(
                    str(
                        self.settings["numeric_settings_page2"][
                            "delay_after_first_click_on_profile"
                        ]
                    )
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "1"
                )
            ),
            "delay_after_every_msg": ctk.StringVar(
                value=(
                    str(
                        self.settings["numeric_settings_page2"]["delay_after_every_msg"]
                    )
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "1"
                )
            ),
            "delay_for_msg_loading": ctk.StringVar(
                value=(
                    str(
                        self.settings["numeric_settings_page2"]["delay_for_msg_loading"]
                    )
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "3"
                )
            ),
            "delay_for_scrolling": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["delay_for_scrolling"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "0.5"
                )
            ),
            "delay_for_next_page": ctk.StringVar(
                value=(
                    str(self.settings["numeric_settings_page2"]["delay_for_next_page"])
                    if self.settings and "numeric_settings_page2" in self.settings
                    else "4"
                )
            ),
        }

        ctk.CTkLabel(self.num_frame2, text="Search Page Settings:").grid(
            row=0, column=0, columnspan=2, pady=5, padx=10, sticky="w"
        )

        for i, (key, var) in enumerate(self.num_vars2.items(), start=1):
            label = ctk.CTkLabel(self.num_frame2, text=f"{key}:")
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")
            entry = ctk.CTkEntry(self.num_frame2, textvariable=var, width=100)
            entry.grid(row=i, column=1, pady=5, padx=10, sticky="w")

        # Twilio Settings
        self.twilio_frame = ctk.CTkFrame(self.scrollable_frame)
        self.twilio_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(self.twilio_frame, text="Twilio Settings:").grid(
            row=0, column=0, columnspan=2, pady=5, padx=10, sticky="w"
        )

        self.twilio_vars = {
            "account_sid": ctk.StringVar(
                value=self.settings.get("twilio_settings", {}).get("account_sid", "N/A")
            ),
            "auth_token": ctk.StringVar(
                value=self.settings.get("twilio_settings", {}).get("auth_token", "N/A")
            ),
            "twilio_default_number": ctk.StringVar(
                value=self.settings.get("twilio_settings", {}).get(
                    "twilio_default_number", "N/A"
                )
            ),
            "user_phone_number": ctk.StringVar(
                value=self.settings.get("twilio_settings", {}).get(
                    "user_phone_number", "N/A"
                )
            ),
        }

        for i, (key, var) in enumerate(self.twilio_vars.items(), start=1):
            label = ctk.CTkLabel(
                self.twilio_frame, text=f"{key.replace('_', ' ').title()}:"
            )
            label.grid(row=i, column=0, pady=5, padx=10, sticky="e")
            entry = ctk.CTkEntry(self.twilio_frame, textvariable=var, width=300)
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
            "email_name": self.email_entry.get(),
            "boolean_settings": {k: v.get() for k, v in self.bool_vars.items()},
            "numeric_settings": {k: float(v.get()) for k, v in self.num_vars.items()},
            "numeric_settings_page2": {
                k: float(v.get()) for k, v in self.num_vars2.items()
            },
            "twilio_settings": {k: v.get() for k, v in self.twilio_vars.items()},
        }

        with open("automation_settings.json", "w") as f:
            dump(settings, f, indent=4)

        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    settings = AutomationSettingsGUI()
    settings.run()
