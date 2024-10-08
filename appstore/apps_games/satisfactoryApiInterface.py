import json
import math

import customtkinter
import requests
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkToplevel
from satisfactory_api_client import SatisfactoryAPI, APIError
from satisfactory_api_client.data import MinimumPrivilegeLevel

from appstore.views import ServerSettingsWindow, DownloadSaveGameWindow
# using my onw satisfactory api client SDK to interact with a satisfactory dedicated server https://pypi.org/project/satisfactory-api-client/


class SatisfactoryApiInterface:

    app: customtkinter.CTk
    api: SatisfactoryAPI

    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("720x480")
        self.app.title("Satisfactory API Interface")
        customtkinter.CTkLabel(self.app, text="Satisfactory API Interface", font=("Arial", 24)).pack(pady=10)
        self.app.protocol("WM_DELETE_WINDOW", self.close)
        self.show_welcome_screen()
        self.app.mainloop()

    def show_welcome_screen(self):
        """Show the welcome screen with login form."""
        self.remove_old_elements()
        customtkinter.CTkLabel(self.app, text="Please enter the server details and login credentials", font=("Arial", 18)).pack(pady=10)

        host_label = customtkinter.CTkLabel(self.app, text="Host:", font=("Arial", 16))
        host_label.pack(pady=5)

        self.host_entry = customtkinter.CTkEntry(self.app, font=("Arial", 16), width=350)
        self.host_entry.pack(pady=5)

        port_label = customtkinter.CTkLabel(self.app, text="Port:", font=("Arial", 16))
        port_label.pack(pady=5)

        self.port_entry = customtkinter.CTkEntry(self.app, font=("Arial", 16), width=350)
        self.port_entry.pack(pady=5)

        self.port_entry.insert(0, "7777")

        privilege_label = customtkinter.CTkLabel(self.app, text="Privilege Level:", font=("Arial", 16))
        privilege_label.pack(pady=5)

        self.privilege_entry = customtkinter.CTkComboBox(self.app, font=("Arial", 16), width=350, values=["CLIENT", "ADMINISTRATOR",])
        self.privilege_entry.pack(pady=5)

        password_label = customtkinter.CTkLabel(self.app, text="Password:", font=("Arial", 16))
        password_label.pack(pady=5)

        self.password_entry = customtkinter.CTkEntry(self.app, font=("Arial", 16), width=350, show="*")
        self.password_entry.pack(pady=5)
        password_info_label = customtkinter.CTkLabel(self.app,
                                                     text="Leave the password field empty if no password "
                                                          "is set for the specific privilege", font=("Arial", 12))
        password_info_label.pack(pady=5)

        login_button = customtkinter.CTkButton(self.app, text="Login", font=("Arial", 16), command=self.login)
        login_button.pack(pady=10)

    def show_server_data(self):
        """Show the server data in a new window."""
        server_data = self.get_server_data()

        if server_data is None:
            CTkMessagebox(title="Error", message="Failed to connect to the server", icon="cancel", sound=True)
            self.show_welcome_screen()
            return

        self.remove_old_elements()

        main_frame = customtkinter.CTkFrame(self.app)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        left_frame = customtkinter.CTkFrame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        right_frame = customtkinter.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        title_label = customtkinter.CTkLabel(left_frame, text="Server Data", font=("Arial", 20, "bold"))
        title_label.pack(pady=10, anchor="w")

        total_game_duration_seconds = server_data.get('totalGameDuration', 0)
        formatted_duration = self.seconds_to_hms(total_game_duration_seconds)

        section_1_label = customtkinter.CTkLabel(left_frame, text="General Information", font=("Arial", 16, "bold"))
        section_1_label.pack(pady=5, anchor="w")

        data_section_1 = [
            ("Session Name", server_data.get('activeSessionName', 'N/A')),
            ("Connected Players",
             f"{server_data.get('numConnectedPlayers', 'N/A')} / {server_data.get('playerLimit', 'N/A')}"),
            ("Tech Tier", server_data.get('techTier', 'N/A'))
        ]

        for key, value in data_section_1:
            customtkinter.CTkLabel(left_frame, text=f"{key}: {value}", font=("Arial", 14)).pack(pady=3, anchor="w")

        customtkinter.CTkLabel(left_frame, text="---", font=("Arial", 12)).pack(pady=5, anchor="w")

        section_2_label = customtkinter.CTkLabel(left_frame, text="Game Status", font=("Arial", 16, "bold"))
        section_2_label.pack(pady=5, anchor="w")

        data_section_2 = [
            ("Is Game Running", server_data.get('isGameRunning', 'N/A')),
            ("Total Game Duration", formatted_duration),
            ("Is Game Paused", 'Yes' if server_data.get('isPaused', True) else 'No'),
            ("Average Tick Rate", round(server_data.get('averageTickRate', 'N/A')))
        ]

        for key, value in data_section_2:
            customtkinter.CTkLabel(left_frame, text=f"{key}: {value}", font=("Arial", 14)).pack(pady=3, anchor="w")

        customtkinter.CTkLabel(left_frame, text="---", font=("Arial", 12)).pack(pady=5, anchor="w")

        customtkinter.CTkLabel(left_frame, text=f"Auto Load Session: {server_data.get('autoLoadSessionName', 'N/A')}",
                               font=("Arial", 14)).pack(pady=5, anchor="w")

        button_list = ["Download An Save File", "Show Server Settings", "Button 3", "Button 4"]  # Example buttons
        for button_name in button_list:
            customtkinter.CTkButton(right_frame, text=button_name,
                                    command=lambda b=button_name: self.button_action(b)).pack(pady=5, anchor="center")

    def button_action(self, button_name):
        """Handle button actions."""
        match button_name:
            case "Download An Save File":
                self.download_save_game()
            case "Show Server Settings":
                self.show_server_settings()

    def login(self):
        """Login to the satisfactory server using the provided details."""
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        privilege = self.privilege_entry.get()
        password = self.password_entry.get()

        if not host or not port:
            CTkMessagebox(title="Error", message="Please enter the host and port", icon="cancel", sound=True)
            return

        self.api = SatisfactoryAPI(host=host, port=port)

        match privilege:
            case "CLIENT":
                privilege = MinimumPrivilegeLevel.CLIENT
            case "ADMINISTRATOR":
                privilege = MinimumPrivilegeLevel.ADMINISTRATOR

        try:
            self.api.health_check()
        except requests.exceptions.ConnectionError:
            CTkMessagebox(title="Error", message="Failed to connect to the server", icon="cancel", sound=True)
            return

        if password:
            try:
                self.api.password_login(minimum_privilege_level=privilege, password=password)
            except APIError as e:
                CTkMessagebox(title="Error", message=str(e), icon="cancel", sound=True)
                return
        else:
            try:
                self.api.passwordless_login(minimum_privilege_level=privilege)
            except APIError as e:
                CTkMessagebox(title="Error", message=str(e), icon="cancel", sound=True)
                return

        response = self.api.verify_authentication_token()

        if response.success:
            self.show_server_data()

    def get_server_data(self) -> dict or None:
        try:
            return self.api.query_server_state().data['serverGameState']
        except APIError as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel", sound=True)
            return None


    def remove_old_elements(self):
        """Remove old elements from the window."""
        for widget in self.app.winfo_children():
            widget.destroy()

    def seconds_to_hms(self, seconds):
        """Convert seconds to HH:MM:SS format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f'{hours:02}:{minutes:02}:{seconds:02}'

    def close(self):
        """Close the application."""
        self.app.destroy()
        exit()

    def download_save_game(self):
        """Download the save game from the server."""
        # tkinter input dialog to get the save name
        possible_save_games = self.enumerate_latest_save_games()

        if not possible_save_games:
            CTkMessagebox(title="Error", message="No save games found on the server", icon="cancel", sound=True)
            return

        DownloadSaveGameWindow(possible_save_games, self.api)

    def show_server_settings(self):
        server_settings = self.get_server_settings()

        server_settings = server_settings['serverOptions']
        if not server_settings:
            CTkMessagebox(title="Error", message="Failed to get server settings", icon="cancel", sound=True)
            return

        ServerSettingsWindow(server_settings).attributes("-topmost", True)

    def enumerate_latest_save_games(self) -> list:
        """Enumerate all save games on the server and return a list of formatted save game strings."""
        list_save_games = []
        save_games = self.api.enumerate_sessions().data

        for session in save_games['sessions']:
            # Loop through the first three saveHeaders
            for header in session['saveHeaders'][:3]:
                save_entry = f"{session['sessionName']} ({header['saveName']})"
                list_save_games.append(save_entry)

        return list_save_games

    def get_server_settings(self):
        """Get the server settings."""
        try:
            return self.api.get_server_options().data
        except APIError as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel", sound=True)
            return None

if __name__ == "__main__":
    SatisfactoryApiInterface()


