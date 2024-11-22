import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.move_history = []
        
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.single_player = False
        self.difficulty = "Easy"
        
        self.turn_label = tk.Label(self.root, text=f"Player {self.player}'s turn")
        self.turn_label.grid(row=3, column=0, columnspan=3, sticky="nsew")
        
        self.score_label = tk.Label(self.root, text=self.get_score_text())
        self.score_label.grid(row=6, column=0, columnspan=3, sticky="nsew")
        
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            for j in range(3):
                self.root.grid_columnconfigure(j, weight=1)
                self.buttons[i][j] = tk.Button(self.root, text="", width=10, height=3,
                                               command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j, sticky="nsew")
        
        self.reset_button = tk.Button(self.root, text="Reset game", command=self.reset_board)
        self.reset_button.grid(row=4, column=0, columnspan=3, sticky="nsew")
        
        self.undo_button = tk.Button(self.root, text="Undo turn", command=self.undo_turn)
        self.undo_button.grid(row=5, column=0, columnspan=3, sticky="nsew")

        self.mode_button = tk.Button(self.root, text="Switch to Single Player", command=self.switch_mode)
        self.mode_button.grid(row=7, column=0, columnspan=3, sticky="nsew")

        self.difficulty_button = tk.Button(self.root, text="Switch to Regular", command=self.switch_difficulty)
        self.difficulty_button.grid(row=8, column=0, columnspan=3, sticky="nsew")

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_rowconfigure(7, weight=1)
        self.root.grid_rowconfigure(8, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def on_button_click(self, i, j):
        if self.buttons[i][j]["text"] == "" and not self.check_winner():
            self.buttons[i][j]["text"] = self.player
            self.move_history.append((i, j, self.player))
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
                if self.player == "X":
                    self.x_wins += 1
                else:
                    self.o_wins += 1
                self.update_score()
                self.reset_board()
            elif self.is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.draws += 1
                self.update_score()
                self.reset_board()
            else:
                self.player = "O" if self.player == "X" else "X"
                self.turn_label.config(text=f"Player {self.player}'s turn")
                if self.single_player and self.player == "O":
                    self.root.after(500, self.computer_move)

    def computer_move(self):
        if self.difficulty == "Easy":
            self.computer_move_easy()
        else:
            self.computer_move_regular()

    def computer_move_easy(self):
        available_moves = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if available_moves:
            i, j = random.choice(available_moves)
            self.on_button_click(i, j)

    def computer_move_regular(self):
        # Check for blocking move
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = "X"
                    if self.check_winner():
                        self.buttons[i][j]["text"] = ""
                        self.on_button_click(i, j)
                        return
                    self.buttons[i][j]["text"] = ""

        # If no blocking move, make a random move
        self.computer_move_easy()

    def undo_turn(self):
        if self.move_history:
            i, j, player = self.move_history.pop()
            self.buttons[i][j]["text"] = ""
            self.player = player
            self.turn_label.config(text=f"Player {self.player}'s turn")

    def check_winner(self):
        for i in range(3):
            if self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "":
                return True
            if self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != "":
                return True
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return True
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return True
        return False

    def is_draw(self):
        for row in self.buttons:
            for button in row:
                if button["text"] == "":
                    return False
        return True

    def reset_board(self):
        for row in self.buttons:
            for button in row:
                button["text"] = ""
        self.player = "X"
        self.move_history.clear()
        self.turn_label.config(text=f"Player {self.player}'s turn")

    def update_score(self):
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        return f"X Wins: {self.x_wins} | O Wins: {self.o_wins} | Draws: {self.draws}"

    def switch_mode(self):
        self.single_player = not self.single_player
        mode_text = "Switch to Two Player" if self.single_player else "Switch to Single Player"
        self.mode_button.config(text=mode_text)
        self.reset_board()

    def switch_difficulty(self):
        self.difficulty = "Regular" if self.difficulty == "Easy" else "Easy"
        difficulty_text = "Switch to Easy" if self.difficulty == "Regular" else "Switch to Regular"
        self.difficulty_button.config(text=difficulty_text)
        self.reset_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()