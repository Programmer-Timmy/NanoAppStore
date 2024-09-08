import random

from appstore.apps_games.getalgoeroe import Difficulty
import json


class HangMan:
    difficulty: str
    word: str
    user_name: str

    max_tries: int
    tries: int = 0

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
        print("Raad het woord:")
        print("_ " * len(self.word))
        print(f"Je hebt {self.max_tries} pogingen.")
        self.ask_letter()

    def ask_letter(self):
        letter = input("Raad een letter: ")
        self.check_letter(letter)

    def check_letter(self, letter):
        if letter in self.word:
            print("Goed geraden!")
            self.check_win()
        else:
            print("Fout geraden!")
            self.tries += 1
            self.check_lose()

    def check_win(self):
        if "_" not in self.word:
            print("Gefeliciteerd! Je hebt het woord geraden.")
            self.play_again()
        else:
            self.ask_letter()

    def check_lose(self):
        if self.tries >= self.max_tries:
            print("Je hebt het maximale aantal pogingen bereikt.")
            print(f"Het woord was: {self.word}")
            self.play_again()
        else:
            self.ask_letter()

    def play_again(self):
        choice = input("Wil je nog een keer spelen? (ja/nee): ")
        if choice.lower() == "ja":
            self.__init__()
            self.start_game()
        elif choice.lower() == "nee":
            print("Bedankt voor het spelen!")
        else:
            print("Ongeldige keuze. Kies ja of nee.")
            self.play_again()


if __name__ == "__main__":
    hang_man = HangMan()
    print(hang_man.difficulty)
