"""Controller for the Getalgoeroe game"""
import dataclasses
import time
import random


@dataclasses.dataclass
class Difficulty:
    """
    This is the difficulty class. It is a dataclass that contains the difficulty levels of the game.

    Attributes
    ----------
    easy : str
        The easy difficulty level
    medium : str
        The medium difficulty level
    hard : str
        The hard difficulty level
    """
    easy: str = "Makkelijk"
    medium: str = "Gemiddeld"
    hard: str = "Moeilijk"


class Getalgoeroe:
    """This is the Getalgoeroe class. It is a dataclass that contains the game logic and UI methods."""

    getal: int
    difficulty: str
    max_attempts: int
    attempts: int = 0

    def __init__(self):
        """This is the constructor method for the Getalgoeroe class. It initializes the game."""
        self.show_welcome_message()
        self.ask_difficulty()
        self.max_attempts = self.get_max_attempts()
        self.getal = self.get_random_number()
        self.start_game()

    def get_max_attempts(self) -> int:
        """
        This method returns the maximum number of attempts based on the difficulty level.

        :return: The maximum number of attempts based on the difficulty level
        """
        match self.difficulty:
            case Difficulty.easy:
                return 5
            case Difficulty.medium:
                return 10
            case Difficulty.hard:
                return 15

    def get_random_number(self) -> int:
        """
        This method returns a random number between 1 and the maximum number based on the difficulty level.

        :return: A random number between 1 and the maximum number
        """
        return random.randint(1, self.get_max_number())

    def get_max_number(self) -> int:
        """
        This method returns the maximum number based on the difficulty level.

        :return: The maximum number based on the difficulty level
        """
        match self.difficulty:
            case Difficulty.easy:
                return 10
            case Difficulty.medium:
                return 25
            case Difficulty.hard:
                return 50

    def ask_difficulty(self) -> None:
        """
        This method asks the user to choose a difficulty level and sets the difficulty attribute.

        :return: None
        """
        possible_difficulties = [Difficulty.easy, Difficulty.medium, Difficulty.hard]

        print("Kies een moeilijkheidsgraad:")
        for i, difficulty in enumerate(possible_difficulties):
            print(f"{i + 1}. {difficulty}")

        try:
            difficulty = int(input("Kies een moeilijkheidsgraad: "))
        except ValueError:
            self.show_difficulty_error()
            self.ask_difficulty()
            return

        if difficulty not in range(1, 4):
            self.show_difficulty_error()
            self.ask_difficulty()
            return
        else:
            self.difficulty = possible_difficulties[difficulty - 1]
            print(f"Je hebt gekozen voor de moeilijkheidsgraad {self.difficulty}")

        self.difficulty = possible_difficulties[difficulty - 1]

    def start_game(self) -> None:
        """
        This method starts the game and allows the player to guess the number.

        :return: None
        """
        while self.attempts < self.max_attempts:
            self.show_attempts_left()
            print("---------------------------------------------------------")
            try:
                guess = int(input(f"Raad het getal tussen 1 en {self.get_max_number()}: "))
            except ValueError:
                print("Ongeldige invoer. Probeer opnieuw.")
                continue

            if guess == self.getal:
                self.show_win()
                break
            else:
                print("Fout! Probeer opnieuw.")
                self.attempts += 1
        else:
            self.show_game_over()

    def show_difficulty_error(self) -> None:
        """
        This method shows an error message when the user chooses an invalid difficulty level.

        :return: None
        """
        print("---------------------------------------------------------")
        print("| Ongeldige keuze. Het getal moet tussen 1 en 3 liggen. |")
        print("---------------------------------------------------------")

    def show_welcome_message(self) -> None:
        """
        This method shows the welcome message when the game starts.

        :return: None
        """
        print('-------------------------------------------------------------------------')
        print('| Welkom bij het spel "GetalGoeroe"                                     |')
        print("| Het spel kiest een getal en jij moet raden welk getal het is.         |")
        print("| Je krijgt een aantal pogingen, afhankelijk van de moeilijkheidsgraad. |")
        print('-------------------------------------------------------------------------')
        time.sleep(3)

    def show_attempts_left(self) -> None:
        """
        This method shows the number of attempts left.

        :return: None
        """
        print(f"Je hebt nog {self.max_attempts - self.attempts} pogingen over.")

    def show_game_over(self) -> None:
        """
        This method shows a game over message when the player runs out of attempts.

        :return: None
        """
        print("---------------------------------------------------------")
        print(f"Je hebt geen pogingen meer over. Het getal was {self.getal}")

    def show_win(self) -> None:
        """
        This method shows a win message when the player guesses the number correctly.

        :return: None
        """
        print("---------------------------------------------------------")
        print(f"| Proficiat! Je hebt het getal geraden in {self.attempts} pogingen.")


