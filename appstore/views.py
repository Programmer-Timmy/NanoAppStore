import os
import re

import _tkinter
import customtkinter
from CTkMessagebox import CTkMessagebox
from satisfactory_api_client import SatisfactoryAPI, APIError


class ServerSettingsWindow(customtkinter.CTkToplevel):
    """Window to display server settings."""
    def __init__(self, settings: dict):
        super().__init__()
        self.settings = settings
        self.show_settings()

    def show_settings(self):
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=400, height=300)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        title_label = customtkinter.CTkLabel(self.scrollable_frame, text="Settings", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 10))

        for key, value in self.settings.items():
            key = key.replace("FG.", "").replace("DS", "")
            print(key)
            for char in key:
                if char.isupper() and key.index(char) != 0:
                    key = key.replace(char, f" {char}")

            label_frame = customtkinter.CTkFrame(self.scrollable_frame)
            label_frame.pack(pady=5, padx=10, fill="x")

            setting_label = customtkinter.CTkLabel(label_frame, text=f"{key}: {value}", font=("Arial", 14))
            setting_label.pack(anchor="w")

            # Optionally, add a separator line between settings
            separator = customtkinter.CTkFrame(label_frame, height=1)
            separator.pack(fill="x", padx=5, pady=(2, 2))

class DownloadSaveGameWindow(customtkinter.CTkToplevel):
    """Window to download a save game."""
    def __init__(self, possible_save_games: list, api: SatisfactoryAPI):
        super().__init__()
        self.api = api
        self.create_widgets(possible_save_games)
        self.attributes("-topmost", True)

    def create_widgets(self, possible_save_games):
        frame = customtkinter.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        title_label = customtkinter.CTkLabel(frame, text="Download Save Game", font=("Arial", 18, "bold"))
        title_label.pack(pady=(10, 20))  # Add space below the title

        self.save_game_combo = customtkinter.CTkComboBox(
            frame,
            values=possible_save_games,
            font=("Arial", 14),
            state="readonly",
            width=300
        )
        self.save_game_combo.pack(pady=(0, 20))

        instructions_label = customtkinter.CTkLabel(frame, text="Select a save game to download:", font=("Arial", 12))
        instructions_label.pack(pady=(0, 10))

        self.download_button = customtkinter.CTkButton(
            frame,
            text="Download",
            font=("Arial", 14),
            command=self.download_save_game,
            width=300
        )
        self.download_button.pack(pady=10)

    def download_save_game(self):
        save_game_name = self.save_game_combo.get()

        if not save_game_name:
            CTkMessagebox(title="Error", message="Please select a save game to download.", icon="cancel", sound=True)
            return

        save_file_name = re.search(r'\((.*?)\)', save_game_name).group(1)
        try:
            save_game = self.api.download_save_game(save_file_name).data
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(f"{project_dir}/appstore/data/satisfactoryApiInterface/{save_file_name}", "wb") as f:
                f.write(save_game)

            CTkMessagebox(title="Success", message="Save game downloaded successfully.", icon="info", sound=True)

            if self.winfo_exists():
                self.withdraw()

        except APIError as e:
            error_message = e.message
            CTkMessagebox(title="Error", message=str(error_message), icon="cancel", sound=True)




