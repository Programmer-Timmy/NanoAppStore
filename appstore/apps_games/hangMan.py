""" HangMan game """
# TODO: Add GUI for HangMan
import random
from datetime import datetime

from appstore.apps_games.getalgoeroe import Difficulty
import json
import customtkinter


class HangMan:
    """HangMan game class"""
    app: customtkinter.CTk = customtkinter.CTk()
    difficulty: str
    word: str
    user_name: str

    max_tries: int
    tries: int = 1
    guessed_letters: list = []

    def __init__(self):
        self.app.geometry("720x480")
        self.app.title("Hang Man")
        customtkinter.CTkLabel(self.app, text="Hang Man", font=("Arial", 24)).pack(pady=10)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Show the welcome screen."""
        self.remove_old_elements()
        customtkinter.CTkLabel(self.app, text="Naam:", font=("arial", 15)).pack()
        self.name_entry = customtkinter.CTkEntry(self.app, font=("Arial", 18), width=350)  # Create the entry widget
        self.name_entry.pack(pady=5)  # Then pack it separately
        start_button = customtkinter.CTkButton(self.app, text="Start", command=self.save_user_name)
        start_button.pack()

    def save_user_name(self):
        """Save the user's name and ask for the difficulty level."""
        self.user_name = self.name_entry.get()  # Now self.name_entry will not be None
        self.ask_difficulty()

    def _get_max_tries(self):
        """Set the maximum number of tries based on the difficulty level."""
        match self.difficulty:
            case Difficulty.easy:
                self.max_tries = 20
            case Difficulty.medium:
                self.max_tries = 15
            case Difficulty.hard:
                self.max_tries = 10

    def get_random_word(self):
        """Get a random word based on the difficulty level."""
        json_file = open("../data/hangMan/words.json", "r").read()
        words = json.loads(json_file)
        match self.difficulty:
            case Difficulty.easy:
                self.word = random.choice(words["easy"])
            case Difficulty.medium:
                self.word = random.choice(words["medium"])
            case Difficulty.hard:
                self.word = random.choice(words["hard"])

    def ask_difficulty(self) -> None:
        """
        This method asks the user to choose a difficulty level and sets the difficulty attribute.

        :return: None
        """
        self.remove_old_elements()
        possible_difficulties = [Difficulty.easy, Difficulty.medium, Difficulty.hard]
        difficulty_message = customtkinter.CTkLabel(self.app, text="Kies een moeilijkheidsgraad:", font=("Arial", 18))
        difficulty_message.pack(pady=10)

        for difficulty in possible_difficulties:
            difficulty_button = customtkinter.CTkButton(self.app, text=difficulty, font=("Arial", 18),
                                                        command=lambda d=difficulty: self.set_difficulty(d))
            difficulty_button.pack(pady=5)

    def set_difficulty(self, difficulty: str) -> None:
        """
        This method sets the difficulty attribute based on the user's choice.

        :param difficulty: The difficulty level chosen by the user
        :return: None
        """
        self.difficulty = difficulty
        self._get_max_tries()
        self.get_random_word()
        self.tries = 1
        self.remove_old_elements()
        self.start_game()

    def start_game(self):
        """Start the game."""
        self.display_status()
        customtkinter.CTkLabel(self.app, font=("Arial", 15), text="Raad een letter:").pack()
        self.guessed_letter = customtkinter.CTkEntry(self.app, font=("Arial", 18), width=350)
        self.guessed_letter.pack(pady=5)
        customtkinter.CTkButton(self.app, text="Start", command=self.check_letter).pack()

    def display_status(self):
        """Display the game status."""
        customtkinter.CTkLabel(self.app, text=f"Poging: {self.tries}/{self.max_tries}", font=("arial", 15)).pack(pady=5)
        display_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "

        customtkinter.CTkLabel(self.app, text=display_word, font=("arial", 15)).pack()

    def check_letter(self):
        """Check if the guessed letter is correct."""
        letter = self.guessed_letter.get()
        self.remove_old_elements()
        if letter in self.word:
            if letter not in self.guessed_letters:
                customtkinter.CTkLabel(self.app, text="Goed geraden!", text_color="green", font=("arial", 15)).pack()
                self.guessed_letters.append(letter)
            else:
                customtkinter.CTkLabel(self.app, text="Deze letter is al geraden!", text_color="orange", font=("arial", 15)).pack()
        else:
            customtkinter.CTkLabel(self.app, text="Fout geraden!", text_color="red", font=("arial", 15)).pack()
            self.tries += 1

        if not self.check_win_or_lose():
            self.start_game()

    def check_win_or_lose(self) -> bool:
        """
        Check if the player has won or lost the game.

        :return: True if the game is over, False otherwise
        """
        # Check if all letters in the word are guessed
        if all(letter in self.guessed_letters for letter in self.word):
            self.remove_old_elements()
            self.save_score(True)
            customtkinter.CTkLabel(self.app, text=f"Goed gedaan! Het woord was: {self.word}", text_color="green", font=("arial", 20)).pack()

            customtkinter.CTkButton(self.app, text="Terug", font=("Arial", 18), command=self.show_welcome_screen).pack()
            return True
        elif self.tries > self.max_tries:
            self.tries -= 1
            self.remove_old_elements()
            customtkinter.CTkLabel(self.app, text=f"Helaas! Het woord was: {self.word}", text_color="red", font=("arial", 20)).pack()
            self.save_score(False)

            customtkinter.CTkButton(self.app, text="Terug", font=("Arial", 18), command=self.show_welcome_screen).pack()

            # Return True to break the loop
            return True
        return False

    def play_again(self):
        """Ask the player if they want to play again."""
        yes_tuple = ("ja", "yes", "j", "y")
        no_tuple = ("nee", "no", "n")
        choice = input("Wil je nog een keer spelen? (ja/nee): ")
        match choice:
            case choice if choice in yes_tuple:
                self.tries = 1
                self.guessed_letters = []
                self.ask_difficulty()
                self.get_random_word()
                self.start_game()
            case choice if choice in no_tuple:
                print("Bedankt voor het spelen!")

            # If the user enters anything other than the yes or no options, ask again.
            case _:
                print("Ongeldige keuze. Kies ja of nee.")
                self.play_again()

    def save_score(self, guessed: bool):
        """Save the score to a JSON file."""
        with open("../data/hangMan/scores.json", "r+") as file:
            scores = json.loads(file.read())
            score = {
                "userName": self.user_name,
                "guessed": guessed,
                "timesGuessed": self.tries,
                "dateTime": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            scores.append(score)

            # Reset file pointer to beginning of file. So we can overwrite the file.
            file.seek(0)
            file.write(json.dumps(scores))

    def remove_old_elements(self) -> None:
        """
        This method removes old UI elements from the screen except the title.

        :return: None
        """
        for widget in self.app.winfo_children():
            if widget != self.app.winfo_children()[0]:
                widget.destroy()

if __name__ == "__main__":
    hang_man = HangMan().app.mainloop()