import dataclasses
import hashlib
import json as JSON
from datetime import datetime, date
from tkinter import messagebox

import customtkinter as ctk

@dataclasses.dataclass()
class Entry:
    date: date
    title: str
    content: str


class Diary:
    user_name: str
    logged_in: bool = False
    entries: list[Entry] = []
    user: JSON = None
    app: ctk.CTk = ctk.CTk()

    def __init__(self):
        self.app.geometry("720x480")
        self.app.title("Dagboek")
        self.app.protocol("WM_DELETE_WINDOW", self.stop)
        self.create_login_interface()
        self.app.mainloop()

    def create_login_interface(self):
        """Create the login interface using Tkinter."""
        self.app.title("Inloggen")
        center_frame = ctk.CTkFrame(self.app)
        ctk.CTkLabel(center_frame, text="Gebruikersnaam", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ctk.CTkEntry(center_frame, font=("Arial", 18))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(center_frame, text="Wachtwoord", font=("Arial", 18)).grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ctk.CTkEntry(center_frame, show="*", font=("Arial", 18))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button = ctk.CTkButton(center_frame, text="Inloggen", command=self.login, font=("Arial", 18), width=100)
        login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        center_frame.pack(pady=50)

    def login(self):
        """Log the user in using the GUI inputs."""
        self.user_name = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_password(password):
            messagebox.showinfo("Succes", "Je bent ingelogd.")
            self.logged_in = True
            self.get_entries()
        else:
            messagebox.showerror("Fout", "Ongeldige gebruikersnaam of wachtwoord")
            self.password_entry.delete(0, ctk.END)

    def show_entry_list(self):
        """Replace the login screen with a scrollable list of entries and action buttons."""
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.title("Dagboekitems")
        scroll_frame = ctk.CTkScrollableFrame(self.app, width=680, height=400)
        scroll_frame.grid(row=0, column=0, padx=10, pady=5)

        for idx, entry in enumerate(self.entries):
            entry_label = ctk.CTkLabel(scroll_frame, text=f"{entry.date}: {entry.title}")
            entry_label.grid(row=idx, column=0, padx=5, pady=5)

            open_button = ctk.CTkButton(scroll_frame, text="Openen", command=lambda e=entry: self.view_day(e), width=100, font=("Arial", 18))
            open_button.grid(row=idx, column=1, padx=5, pady=5)

            edit_button = ctk.CTkButton(scroll_frame, text="Bewerken", command=lambda e=entry: self.edit_day(e), width=100, font=("Arial", 18))
            edit_button.grid(row=idx, column=2, padx=5, pady=5)

            delete_button = ctk.CTkButton(scroll_frame, text="Verwijderen", command=lambda e=entry: self.delete_day(e), width=100, font=("Arial", 18))
            delete_button.grid(row=idx, column=3, padx=5, pady=5)

        button_frame = ctk.CTkFrame(self.app)
        add_button = ctk.CTkButton(button_frame, text="Nieuwe Invoer", command=self.add_new_day, font=("Arial", 18), width=100)
        add_button.grid(row=1, column=0, padx=10, pady=5)

        stop_button = ctk.CTkButton(button_frame, text="Stoppen", command=self.stop, font=("Arial", 18), width=100)
        stop_button.grid(row=1, column=1, padx=5, pady=5)

        button_frame.grid(row=1, column=0, padx=10, pady=5)

    def get_entries(self):
        """Get the user's diary entries."""
        if not self.logged_in:
            return

        for entry in self.user.get("Diary", []):
            try:
                date_object = datetime.strptime(entry["Date"], "%d-%m-%Y").date()
                new_entry = Entry(date=date_object, title=entry["Title"], content=entry["Content"])
                self.entries.append(new_entry)
            except (KeyError, ValueError) as e:
                messagebox.showerror("Fout", f"Fout bij het verwerken van de invoer: {e}")

        self.show_entry_list()

    def get_user_credentials(self) -> str | None:
        """Get the user's diary entries."""
        json = open("data/diary/diary.json", "r").read()
        for user in JSON.loads(json):
            if user["Username"] == self.user_name:
                self.user = user
                return user["PasswordHash"]

        return None

    def hash_password(self, password: str) -> str:
        """Hash the user's password."""
        password += "5a1d"
        return hashlib.md5(password.encode()).hexdigest()

    def validate_password(self, password: str) -> bool:
        """Validate the user's password."""
        password_hash = self.get_user_credentials()
        if not password_hash:
            return False

        return self.hash_password(password) == password_hash

    def add_new_day(self):
        """Open a window to add a new entry."""
        add_window = ctk.CTkToplevel(self.app)
        add_window.title("Nieuwe Invoer Toevoegen")

        ctk.CTkLabel(add_window, text="Datum (dd-mm-jjjj)").grid(row=0, column=0, padx=10, pady=10)
        date_entry = ctk.CTkEntry(add_window)
        date_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(add_window, text="Titel").grid(row=1, column=0, padx=10, pady=10)
        title_entry = ctk.CTkEntry(add_window)
        title_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(add_window, text="Inhoud").grid(row=2, column=0, padx=10, pady=10)
        content_entry = ctk.CTkTextbox(add_window, height=80)
        content_entry.grid(row=2, column=1, padx=10, pady=10)

        save_button = ctk.CTkButton(add_window, text="Opslaan", command=lambda: self.save_new_entry(date_entry.get(), title_entry.get(), content_entry.get("1.0", ctk.END), add_window))
        save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        add_window.attributes("-topmost", True)

    def save_new_entry(self, date_str, title, content, window):
        """Save the new entry."""
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            messagebox.showerror("Fout", "Ongeldige datum.")
            return

        new_entry = Entry(date=date, title=title, content=content.strip())
        self.entries.append(new_entry)
        self.show_entry_list()
        self.save_entries()
        window.destroy()

    def delete_day(self, entry: Entry):
        """Delete the selected entry."""
        self.entries.remove(entry)
        self.save_entries()
        messagebox.showinfo("Invoer Verwijderd", "De dag is verwijderd.")
        self.show_entry_list()

    def edit_day(self, entry: Entry):
        """Open a window to edit the entry."""
        edit_window = ctk.CTkToplevel(self.app, width=400, height=300)
        edit_window.title("Invoer Bewerken")

        ctk.CTkLabel(edit_window, text="Datum (dd-mm-jjjj)").grid(row=0, column=0, padx=10, pady=10)
        date_entry = ctk.CTkEntry(edit_window)
        date_entry.insert(0, entry.date.strftime("%d-%m-%Y"))
        date_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(edit_window, text="Titel").grid(row=1, column=0, padx=10, pady=10)
        title_entry = ctk.CTkEntry(edit_window)
        title_entry.insert(0, entry.title)
        title_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(edit_window, text="Inhoud").grid(row=2, column=0, padx=10, pady=10)
        content_entry = ctk.CTkTextbox(edit_window, height=80)
        content_entry.insert("1.0", entry.content)
        content_entry.grid(row=2, column=1, padx=10, pady=10)

        save_button = ctk.CTkButton(edit_window, text="Opslaan", command=lambda: self.save_edited_entry(entry, date_entry.get(), title_entry.get(), content_entry.get("1.0", ctk.END), edit_window))
        save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        edit_window.attributes("-topmost", True)

    def save_edited_entry(self, old_entry: Entry, date_str, title, content, window):
        """Save the edited entry."""
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            messagebox.showerror("Fout", "Ongeldige datum.")
            return

        self.entries.remove(old_entry)
        updated_entry = Entry(date=date, title=title, content=content.strip())
        self.entries.append(updated_entry)
        self.save_entries()
        self.show_entry_list()
        window.destroy()

    def view_day(self, entry: Entry):
        """Open a window to view the entry."""

        view_window = ctk.CTkToplevel(self.app)
        view_window.title(entry.title)

        ctk.CTkLabel(view_window, text=f"Datum: {entry.date}", font=("Arial", 18), width=300).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(view_window, text=f"Titel: {entry.title}", font=("Arial", 18), width=300).grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkLabel(view_window, text="Inhoud:", font=("Arial", 18), width=300).grid(row=2, column=0, padx=10, pady=1)

        content_label = ctk.CTkLabel(view_window, text=entry.content, width=300, wraplength=600, justify="left", font=("Arial", 14))
        content_label.grid(row=3, column=0, padx=10, pady=5)

        close_button = ctk.CTkButton(view_window, text="Sluiten", command=view_window.destroy)
        close_button.grid(row=4, column=0, padx=10, pady=5)

        view_window.attributes("-topmost", True)

    def save_entries(self):
        """Save the diary entries to a JSON file."""
        entries_data = [{"Date": e.date.strftime("%d-%m-%Y"), "Title": e.title, "Content": e.content} for e in self.entries]
        with open("data/diary/diary.json", "r+") as f:
            json = JSON.loads(f.read())
            for user in json:
                if user["Username"] == self.user_name:
                    user["Diary"] = entries_data
                    break

            f.seek(0)
            f.write(JSON.dumps(json, indent=4))
            f.truncate()


    def stop(self):
        """Exit the application."""
        self.app.quit()
        exit()

if __name__ == "__main__":
    diary = Diary()
