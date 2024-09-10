import dataclasses
import hashlib
import json as JSON
from datetime import datetime, date


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

    def __init__(self):
        self.login()
        if self.logged_in:
            self.show_diary_entries()
            entry = self.ask_to_chose_entry()
            print(entry.title)

    def login(self):
        """Log the user in."""
        self.user_name = input("Wat is je gebruikersnaam? ")
        password = input("Wat is je wachtwoord? ")
        if self.validate_password(password):
            print("Je bent ingelogd.")
            self.logged_in = True
            self.get_entries()
        else:
            print("Ongeldige gebruikersnaam of wachtwoord")
            self.login()

    def get_entries(self):
        """Get the user's diary entries."""
        if not self.logged_in:
            return
        for entry in self.user["Diary"]:
            # https://stackoverflow.com/questions/2803852/python-date-string-to-date-object
            date_object = datetime.strptime(entry["Date"], "%d-%m-%Y").date()
            self.entries.append(Entry(date=date_object, title=entry["Title"], content=entry["Content"]))

    def get_user_credentials(self) -> str | None:
        """Get the user's diary entries."""
        json = open("../data/diary/diary.json", "r").read()
        for user in JSON.loads(json):
            if user["Username"] == self.user_name:
                self.user = user
                return user["PasswordHash"]

        return None

    def hash_password(self, password: str) -> str:
        """Hash the user's password."""
        # https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/
        password += "5a1d"
        return hashlib.md5(password.encode()).hexdigest()

    def validate_password(self, password: str) -> bool:
        """Validate the user's password."""
        # https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/
        password_hash = self.get_user_credentials()
        if not password_hash:
            return False

        return self.hash_password(password) == password_hash

    def show_diary_entries(self):
        i = 1
        print("Opgeslagen dagen:")
        for entry in self.entries:
            print(f"{i}: {entry.date}")
            i += 1

    def ask_to_chose_entry(self) -> Entry:
        entry_number = input("Welke dag wil je bekijken? ")
        try:
            return self.entries[int(entry_number) - 1]
        except ValueError:
            print("Ongeldige keuze")
            return self.ask_to_chose_entry()

    def ask_wat_todo(self):
        print("Wat wil je doen?")
        print("1: Nieuwe dag toevoegen")
        print("2: Dag verwijderen")
        print("3: Dag aanpassen")
        print("4: Dag bekijken")
        print("5: Stoppen")
        choice = input("Keuze: ")

        match choice:
            case "1":
                self.add_new_day()
            case "2":
                self.delete_day()
            case "3":
                self.edit_day()
            case "4":
                self.view_day()
            case "5":
                self.stop()
            case _:
                print("Ongeldige keuze")
                self.ask_wat_todo()

    def add_new_day(self):
        date = input("Wat is de datum van de dag? (dd-mm-jjjj) ")
        try :
            date = datetime.strptime(date, "%d-%m-%Y").date()
        except ValueError:
            print("Ongeldige datum")
            self.add_new_day()

        title = input("Wat is de titel van de dag? ")
        content = input("Wat is de inhoud van de dag? ")

        self.entries.append(Entry(date=date, title=title, content=content))






if __name__ == "__main__":
    diary = Diary()
