"""This is the rock, paper, scissors game logic."""
import random

import customtkinter


class RockPeperScissors:
    """This is the rock, paper, scissors class. It is a dataclass that contains the game logic and UI methods."""
    app: customtkinter.CTk = customtkinter.CTk()
    player_choice: str
    computer_choice: str
    player_score: int = 0
    computer_score: int = 0
    max_rounds: int
    rounds_played: int = 0
    rounds_entry = None

    def __init__(self):
        """This is the constructor method for the rock, paper, scissors class. It initializes the game."""
        self.app.geometry("720x480")
        self.app.title("Rock, Paper, Scissors")
        customtkinter.CTkLabel(self.app, text="Rock, Paper, Scissors", font=("Arial", 24)).pack(pady=10)
        self.app.protocol("WM_DELETE_WINDOW", self.close)
        self.show_welcome_screen()
        self.run()

    def get_winner(self) -> str:
        """
        This method determines the winner of the round based on the player and computer choices.

        :return: The winner of the round
        """
        if self.player_choice == self.computer_choice:
            return "Tie"
        elif self.player_choice == "Rock" and self.computer_choice == "Scissors":
            return "Player"
        elif self.player_choice == "Paper" and self.computer_choice == "Rock":
            return "Player"
        elif self.player_choice == "Scissors" and self.computer_choice == "Paper":
            return "Player"
        else:
            return "Computer"

    def get_computer_choice(self) -> str:
        """
        This method returns a random choice for the computer.

        :return: A random choice for the computer
        """
        return random.choice(["Rock", "Paper", "Scissors"])

    def update_scores(self, winner: str):
        """
        This method updates the scores based on the winner of the round.

        :param winner: The winner of the round
        """
        if winner == "Player":
            self.player_score += 1
        elif winner == "Computer":
            self.computer_score += 1

    def is_game_over(self) -> bool:
        """
        This method checks if the game is over based on the number of rounds played.

        :return: True if the game is over, False otherwise
        """
        return self.rounds_played >= self.max_rounds

    def show_welcome_screen(self):
        """Show the welcome screen."""
        self.remove_old_elements()
        customtkinter.CTkLabel(self.app, text="Hoeveel rondes wil je spelen?", font=("arial", 15)).pack()
        self.rounds_entry = customtkinter.CTkEntry(self.app, font=("Arial", 18), width=350)
        self.rounds_entry.pack(pady=5)
        self.buttnonGroup = customtkinter.CTkFrame(self.app)
        start_button = customtkinter.CTkButton(self.buttnonGroup, text="Start", command=self.save_rounds)
        stop_button = customtkinter.CTkButton(self.buttnonGroup, text="Stop", command=self.close)

        start_button.pack(pady=5)
        stop_button.pack(pady=5)
        self.buttnonGroup.pack()

    def save_rounds(self):
        """Save the number of rounds entered by the player."""
        self.rounds_played = 0
        self.max_rounds = int(self.rounds_entry.get())
        self.show_choices()

    def show_choices(self):
        """Show the choices for the player."""
        self.remove_old_elements()
        customtkinter.CTkLabel(self.app, text="Kies Rock, Paper of Scissors", font=("arial", 15)).pack()
        rock_button = customtkinter.CTkButton(self.app, text="Rock", command=lambda: self.save_choice("Rock"))
        rock_button.pack(pady=5)
        paper_button = customtkinter.CTkButton(self.app, text="Paper", command=lambda: self.save_choice("Paper"))
        paper_button.pack(pady=5)
        scissors_button = customtkinter.CTkButton(self.app, text="Scissors", command=lambda: self.save_choice("Scissors"))
        scissors_button.pack(pady=5)

    def save_choice(self, choice: str):
        """Save the choice made by the player and start the round."""
        self.player_choice = choice
        self.computer_choice = self.get_computer_choice()
        self.show_result()

    def show_result(self):
        """Show the result of the round."""
        self.remove_old_elements()
        customtkinter.CTkLabel(self.app, text=f"Player: {self.player_choice}", font=("arial", 15)).pack()
        customtkinter.CTkLabel(self.app, text=f"Computer: {self.computer_choice}", font=("arial", 15)).pack()
        winner = self.get_winner()
        self.update_scores(winner)
        customtkinter.CTkLabel(self.app, text=f"Winner: {winner}", font=("arial", 15)).pack()
        self.rounds_played += 1
        if self.is_game_over():
            self.show_game_over()
        else:
            customtkinter.CTkButton(self.app, text="Volgende ronde", command=self.show_choices).pack()

    def show_game_over(self):
        """Show the game over screen."""
        self.remove_old_elements()
        customtkinter.CTkLabel(self.app, text="Game Over", font=("arial", 20)).pack()
        customtkinter.CTkLabel(self.app, text=f"Player Score: {self.player_score}", font=("arial", 15)).pack()
        customtkinter.CTkLabel(self.app, text=f"Computer Score: {self.computer_score}", font=("arial", 15)).pack()
        customtkinter.CTkButton(self.app, text="Opnieuw spelen", command=self.show_welcome_screen).pack()

    def remove_old_elements(self):
        """Remove old elements from the screen."""
        for widget in self.app.winfo_children():
            widget.destroy()

    def run(self):
        """Run the rock, paper, scissors game."""
        self.app.mainloop()

    def close(self):
        """Close the app."""
        self.app.destroy()
        exit()


if __name__ == "__main__":
    game = RockPeperScissors()


