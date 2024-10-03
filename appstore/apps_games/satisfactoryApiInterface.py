import math

import customtkinter
from CTkMessagebox import CTkMessagebox
from satisfactory_api_client import SatisfactoryAPI, APIError
from satisfactory_api_client.data import MinimumPrivilegeLevel
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

        # default port for satisfactory is 7777
        self.port_entry.insert(0, "7777")

        # password type administator or client
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

        # Main title with bold font
        title_label = customtkinter.CTkLabel(self.app, text="Server Data", font=("Arial", 20, "bold"))
        title_label.pack(pady=10, anchor="w")

        # Format total game duration
        total_game_duration_seconds = server_data.get('totalGameDuration', 0)
        formatted_duration = self.seconds_to_hms(total_game_duration_seconds)

        # Section title (for first group)
        section_1_label = customtkinter.CTkLabel(self.app, text="General Information", font=("Arial", 16, "bold"))
        section_1_label.pack(pady=5, anchor="w")

        # Grouping related fields
        data_section_1 = [
            ("Session Name", server_data.get('activeSessionName', 'N/A')),
            ("Connected Players",
             f"{server_data.get('numConnectedPlayers', 'N/A')} / {server_data.get('playerLimit', 'N/A')}"),
            ("Tech Tier", server_data.get('techTier', 'N/A'))
        ]

        # Section 1 data display with key-value pairs
        for key, value in data_section_1:
            customtkinter.CTkLabel(self.app, text=f"{key}: {value}", font=("Arial", 14)).pack(pady=3, anchor="w")

        # Adding a separator
        customtkinter.CTkLabel(self.app, text="---", font=("Arial", 12)).pack(pady=5, anchor="w")

        # Section title (for second group)
        section_2_label = customtkinter.CTkLabel(self.app, text="Game Status", font=("Arial", 16, "bold"))
        section_2_label.pack(pady=5, anchor="w")

        # Grouping more related fields
        data_section_2 = [
            ("Is Game Running", server_data.get('isGameRunning', 'N/A')),
            ("Total Game Duration", formatted_duration),
            ("Is Game Paused", 'Yes' if server_data.get('isPaused', True) else 'No'),
            ("Average Tick Rate", round(server_data.get('averageTickRate', 'N/A')))
        ]

        # Section 2 data display with key-value pairs
        for key, value in data_section_2:
            customtkinter.CTkLabel(self.app, text=f"{key}: {value}", font=("Arial", 14)).pack(pady=3, anchor="w")

        # Adding another separator
        customtkinter.CTkLabel(self.app, text="---", font=("Arial", 12)).pack(pady=5, anchor="w")

        # Optional Auto Load Session
        customtkinter.CTkLabel(self.app, text=f"Auto Load Session: {server_data.get('autoLoadSessionName', 'N/A')}",
                               font=("Arial", 14)).pack(pady=5, anchor="w")

    def login(self):
        """Login to the satisfactory server using the provided details."""
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        privilege = self.privilege_entry.get()
        password = self.password_entry.get()
        self.api = SatisfactoryAPI(host=host, port=port)

        match privilege:
            case "CLIENT":
                privilege = MinimumPrivilegeLevel.CLIENT
            case "ADMINISTRATOR":
                privilege = MinimumPrivilegeLevel.ADMINISTRATOR

        try:
            self.api.health_check()
        except APIError:
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

if __name__ == "__main__":
    SatisfactoryApiInterface()
