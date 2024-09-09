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

    def login(self):
        """Log the user in."""
        self.user_name = input("Wat is je gebruikersnaam? ")
        password = input("Wat is je wachtwoord? ")
        if self.validate_password(password):
            print("Je bent ingelogd.")
            self.logged_in = True
            self.get_entries()
            print(self.entries)
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

    def show_entries(self):




if __name__ == "__main__":
    diary = Diary()
