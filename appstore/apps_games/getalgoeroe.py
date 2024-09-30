""" This is the Getalgoeroe module. It contains the Getalgoeroe class that implements the game logic and UI methods. """
import dataclasses
import random
import customtkinter

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


# https://www.youtube.com/watch?v=NI9LXzo0UY0 (video used making the gui)
class Getalgoeroe:
    """This is the Getalgoeroe class. It is a dataclass that contains the game logic and UI methods."""
    app: customtkinter.CTk = customtkinter.CTk()
    number: int
    difficulty: str
    max_attempts: int
    attempts: int = 0

    def __init__(self):
        """This is the constructor method for the Getalgoeroe class. It initializes the game."""
        self.app.geometry("720x480")
        self.app.title("Getalgoeroe")
        customtkinter.CTkLabel(self.app, text="Getalgoeroe", font=("Arial", 24)).pack(pady=10)
        self.app.protocol("WM_DELETE_WINDOW", self.close)
        self.show_welcome_screen()
        self.app.mainloop()

    # Game Logic Methods
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

    def check_guess(self, guess: str) -> None:
        """
        This method checks if the player's guess is correct and shows the appropriate message.

        :param guess: The player's guess as a string
        :return: None
        """
        if not guess.isdigit():
            self.remove_error_message()
            self.show_error("Ongeldige invoer. Voer een getal in.")
            return
        guess = int(guess)
        self.attempts += 1

        if guess == self.number:
            self.show_win()
        elif self.attempts == self.max_attempts:
            self.show_game_over()
        else:
            self.start_game()

    # UI Methods
    def show_welcome_screen(self) -> None:
        """
        This method shows the welcome screen for the game.

        :return: None
        """
        self.remove_old_elements()

        welcome_message = customtkinter.CTkLabel(self.app, text="Welkom bij Getalgoeroe!", font=("Arial", 18))
        welcome_message.pack(pady=10)

        button_frame = customtkinter.CTkFrame(self.app)
        button_frame.pack()

        start_button = customtkinter.CTkButton(button_frame, text="Start", font=("Arial", 18), command=self.ask_difficulty)
        start_button.grid(row=0, column=0, padx=1)

        quit_button = customtkinter.CTkButton(button_frame, text="Afsluiten", font=("Arial", 18), command=self.app.quit)
        quit_button.grid(row=0, column=1, padx=1)

        self.app.update()

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

        self.app.update()

    def set_difficulty(self, difficulty: str) -> None:
        """
        This method sets the difficulty attribute based on the user's choice.

        :param difficulty: The difficulty level chosen by the user
        :return: None
        """
        self.difficulty = difficulty
        self.max_attempts = self.get_max_attempts()
        self.number = self.get_random_number()
        self.attempts = 0
        self.start_game()

    def start_game(self) -> None:
        """
        This method starts the game and allows the player to guess the number. In the gui

        :return: None
        """
        self.remove_old_elements()
        self.show_attempts_left()

        guess_entry = customtkinter.CTkEntry(self.app, font=("Arial", 18))
        guess_entry.pack(pady=10)

        guess_button = customtkinter.CTkButton(self.app, text="Raad", font=("Arial", 18),
                                                command=lambda: self.check_guess(guess_entry.get()))
        guess_button.pack()

        self.app.update()

    def show_attempts_left(self) -> None:
        """
        This method shows the number of attempts left.

        :return: None
        """
        difficulty_text = f"Moeilijkheidsgraad: {self.difficulty}"
        difficulty_message = customtkinter.CTkLabel(self.app, text=difficulty_text, font=("Arial", 15))
        difficulty_message.pack()

        attempts_text = f"Je hebt nog {self.max_attempts - self.attempts} pogingen over."
        attempts_message = customtkinter.CTkLabel(self.app, text=attempts_text, font=("Arial", 18))
        attempts_message.pack(pady=5)

    def show_game_over(self) -> None:
        """
        This method shows a game over message when the player runs out of attempts.

        :return: None
        """
        self.remove_old_elements()

        lose_message = customtkinter.CTkLabel(self.app, text="Helaas! Je hebt geen pogingen meer over.", font=("Arial", 18), text_color="red")
        lose_message.pack(pady=5)

        number_message = customtkinter.CTkLabel(self.app, text=f"Het getal was: {self.number}", font=("Arial", 18))
        number_message.pack(pady=5)

        button_frame = customtkinter.CTkFrame(self.app)
        button_frame.pack()

        play_again_button = customtkinter.CTkButton(button_frame, text="Speel opnieuw", font=("Arial", 18), command=self.ask_difficulty)
        play_again_button.grid(row=0, column=0, padx=1)

        go_back_button = customtkinter.CTkButton(button_frame, text="Terug", font=("Arial", 18),
                                                 command=self.show_welcome_screen)
        go_back_button.grid(row=0, column=1, padx=1)

        self.app.update()

    def show_win(self) -> None:
        """
        This method shows a win message when the player guesses the number correctly.

        :return: None
        """
        self.remove_old_elements()
        win_message = customtkinter.CTkLabel(self.app, text="Gefeliciteerd! Je hebt het getal geraden.", font=("Arial", 18), text_color="green")
        win_message.pack(pady=5)

        button_frame = customtkinter.CTkFrame(self.app)
        button_frame.pack()

        play_again_button = customtkinter.CTkButton(button_frame, text="Speel opnieuw", font=("Arial", 18),
                                                    command=self.ask_difficulty)
        play_again_button.grid(row=0, column=0, padx=1)

        go_back_button = customtkinter.CTkButton(button_frame, text="Terug", font=("Arial", 18),
                                                 command=self.show_welcome_screen)
        go_back_button.grid(row=0, column=1, padx=1)

        self.app.update()

    def show_error(self, message: str) -> None:
        """
        This method shows an error message to the player.

        :param message: The error message to display
        :return: None
        """
        error_message = customtkinter.CTkLabel(self.app, text=message, font=("Arial", 18), text_color="red")
        error_message.pack()

    # Utility Methods
    def remove_old_elements(self) -> None:
        """
        This method removes old UI elements from the screen except the title.

        :return: None
        """
        for widget in self.app.winfo_children():
            if widget != self.app.winfo_children()[0]:
                widget.destroy()

    def remove_error_message(self) -> None:
        """
        This method removes the error message from the screen.

        :return: None
        """
        for widget in self.app.winfo_children():
            if isinstance(widget, customtkinter.CTkLabel) and widget._text_color == "red":
                widget.destroy()

    def close(self):
        """Close the app."""
        self.app.quit()
        exit()


if __name__ == "__main__":
    app = Getalgoeroe()
