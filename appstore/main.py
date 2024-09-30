import dataclasses
import os
import re
import importlib
import customtkinter


@dataclasses.dataclass
class App:
    """The App class."""
    path: str
    name: str
    class_name: str
    description: str


class AppStore:
    """The hub of all the apps and games in the AppStore."""
    app: customtkinter.CTk
    apps_games: list[App] = []

    def __init__(self) -> None:
        """Initialize the AppStore class."""
        self.app = customtkinter.CTk()
        self.app.geometry("720x480")
        self.app.title("AppStore")
        label = customtkinter.CTkLabel(self.app, text="AppStore", font=("Arial", 24))
        label.pack(pady=10)
        self.show_home_screen()

    def get_apps(self) -> None:
        """Populate a list of apps in the AppStore."""
        path = "apps_games/"
        filter_out = ["__init__.py", "__pycache__"]
        dir_list = os.listdir(path)

        for item in filter_out:
            if item in dir_list:
                dir_list.remove(item)

        for file_name in dir_list:
            if file_name.endswith(".py"):
                name = re.sub(r"\.py", "", file_name)
                name_display = re.sub(r"(\w)([A-Z])", r"\1 \2", name).capitalize()
                class_name = name[0].upper() + name[1:]
                self.apps_games.append(App(path=f"appstore.apps_games.{name}", name=name_display, description="", class_name=class_name))

    def show_home_screen(self) -> None:
        """Show the home screen of the AppStore with apps and games."""
        self.get_apps()
        main_frame = customtkinter.CTkFrame(self.app)
        main_frame.pack(pady=10)

        for index, app in enumerate(self.apps_games):
            button = customtkinter.CTkButton(main_frame, text=app.name, command=lambda i=index: self.show_app(i))
            button.pack(pady=5)

    def show_app(self, index: int) -> None:
        """Show and launch the app in a separate customtkinter window."""
        app = self.apps_games[index]
        print(f"Launching {app.name}")
        try:

            # Dynamically import the app module and run the main function or class
            print(app.path, app.class_name)
            module = importlib.import_module(app.path)
            if hasattr(module, app.class_name):
                self.app.withdraw()
                app_class = getattr(module, app.class_name)
                app_class()  # Create an instance of the class

                exit()

            else:
                print(f"Error: Class {app.class_name} not found in {app.path}.")
        except Exception as e:
            print(f"Error launching {app.name}: {e}")


if __name__ == "__main__":
    AppStore().app.mainloop()
