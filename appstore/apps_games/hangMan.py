# TODO: Add GUI for HangMan
import random
from datetime import datetime

from appstore.apps_games.getalgoeroe import Difficulty
import json


class HangMan:
    difficulty: str
    word: str
    user_name: str

    max_tries: int
    tries: int = 0
    guessed_letters: list = []

    def __init__(self):
        self.user_name = input("Wat is je naam? ")
        self.ask_difficulty()
        self.get_random_word()
        self._get_max_tries()
        self.start_game()

    def _get_max_tries(self):
        match self.difficulty:
            case Difficulty.easy:
                self.max_tries = 20
            case Difficulty.medium:
                self.max_tries = 15
            case Difficulty.hard:
                self.max_tries = 10

    def get_random_word(self):
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
        print("Welkom bij Galgje!")
        print(f"Je hebt {self.max_tries} pogingen.")
        self.ask_letter()

    def ask_letter(self):
        print("--------------------")
        print("Raad het woord:")
        print(" ".join([letter if letter in self.guessed_letters else "_" for letter in self.word]))
        letter = input("Raad een letter: ")
        self.check_letter(letter)

    def check_letter(self, letter):
        if letter in self.word and letter not in self.guessed_letters:
            print("Goed geraden!")
            self.guessed_letters.append(letter)
            self.check_win()
        elif letter in self.guessed_letters:
            print("Je hebt deze letter al geraden.")
            self.ask_letter()
        else:
            print("Fout geraden!")
            self.tries += 1
            self.check_lose()

    def check_win(self):
        if all(letter in self.guessed_letters for letter in self.word):
            self.save_score(True)
            print("Gefeliciteerd, je hebt het woord geraden! Het woord was: ", self.word)
            self.play_again()
        else:
            self.ask_letter()

    def check_lose(self):
        if self.tries >= self.max_tries:
            print("Je hebt het maximale aantal pogingen bereikt.")
            print(f"Het woord was: {self.word}")
            self.save_score(False)
            self.play_again()
        else:
            self.ask_letter()

    def play_again(self):
        choice = input("Wil je nog een keer spelen? (ja/nee): ")
        if choice.lower() == "ja":
            self.__init__()
        elif choice.lower() == "nee":
            print("Bedankt voor het spelen!")
        else:
            print("Ongeldige keuze. Kies ja of nee.")
            self.play_again()

    def save_score(self, guessed: bool):
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