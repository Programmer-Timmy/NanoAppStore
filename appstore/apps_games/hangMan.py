""" HangMan game """
# TODO: Add GUI for HangMan
import random
from datetime import datetime

from appstore.apps_games.getalgoeroe import Difficulty
import json


class HangMan:
    """HangMan game class"""
    difficulty: str
    word: str
    user_name: str

    max_tries: int
    tries: int = 1
    guessed_letters: list = []

    def __init__(self):
        self.user_name = input("Wat is je naam? ")
        self.ask_difficulty()
        self.get_random_word()
        self._get_max_tries()
        self.start_game()

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

    def ask_difficulty(self):
        """Ask the player to choose a difficulty level."""
        possible_difficulties = [Difficulty.easy, Difficulty.medium, Difficulty.hard]

        print("Kies een moeilijkheidsgraad:")
        for difficulty in possible_difficulties:
            print(f"{possible_difficulties.index(difficulty) + 1}. {difficulty}")
     
        choice = input("Keuze: ")
        match choice:
            case "1":
                self.difficulty = Difficulty.easy
            case "2":
                self.difficulty = Difficulty.medium
            case "3":
                self.difficulty = Difficulty.hard
            case _:
                print("Ongeldige keuze. Kies getallen 1, 2 of 3.")
                self.ask_difficulty()
                return
        print(f"Je hebt gekozen voor moeilijkheidsgraad: {self.difficulty}")

    def start_game(self):
        """Start the game."""
        print("Welkom bij Galgje!")
        print(f"Je hebt {self.max_tries} pogingen.")

        # Use a while loop to keep the game running until the player wins or loses. (this is better than using for loop)
        while self.tries <= self.max_tries:
            self.display_status()
            letter = input("Raad een letter: ")
            self.check_letter(letter)
            if self.check_win_or_lose():
                break

    def display_status(self):
        """Display the game status."""
        print("--------------------")
        print(f"Poging: {self.tries}/{self.max_tries}")
        print("Raad het woord:")
        display_word = ""

        for letter in self.word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "

        print(display_word.strip())

    def check_letter(self, letter):
        """Check if the guessed letter is correct."""
        if letter in self.word:
            if letter not in self.guessed_letters:
                print("Goed geraden!")
                self.guessed_letters.append(letter)
            else:
                print("Je hebt deze letter al geraden.")
        else:
            print("Fout geraden!")
            self.tries += 1

    def check_win_or_lose(self) -> bool:
        """
        Check if the player has won or lost the game.

        :return: True if the game is over, False otherwise
        """
        print(self.max_tries, self.tries)
        # Check if all letters in the word are guessed
        if all(letter in self.guessed_letters for letter in self.word):
            self.save_score(True)
            print("Gefeliciteerd, je hebt het woord geraden! Het woord was:", self.word)
            self.play_again()
            # Return True to break the loop
            return True
        elif self.tries > self.max_tries:
            print(f"Je hebt het maximale aantal pogingen bereikt. Het woord was: {self.word}")
            self.save_score(False)
            self.play_again()
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


if __name__ == "__main__":
    hang_man = HangMan()