import customtkinter as ctk
from random import randrange, choice
import sys
import json
import os

class TicTacToeGame:
    def __init__(self):
        self.score_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puntaje.json")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x800")  # Cambiado tamaño de ventana
        self.root.resizable(False, False)
        
        # Variables del juego
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Siempre empieza X
        self.game_over = False

        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

        self.player_symbol = 'O'  # Por defecto, jugador es O
        self.ai_symbol = 'X'

        self.load_score()
        self.setup_ui()
        # No hacer el primer movimiento hasta que el usuario elija ficha

    def save_score(self):
        data = {
            "player_wins": self.player_wins,
            "ai_wins": self.ai_wins,
            "draws": self.draws
        }
        with open(self.score_path, "w") as f:
            json.dump(data, f)

    def load_score(self):
        if os.path.exists(self.score_path):
            try:
                with open(self.score_path, "r") as f:
                    data = json.load(f)
                    self.player_wins = data.get("player_wins", 0)
                    self.ai_wins = data.get("ai_wins", 0)
                    self.draws = data.get("draws", 0)
            except Exception:
                self.player_wins = 0
                self.ai_wins = 0
                self.draws = 0
        else:
            self.player_wins = 0
            self.ai_wins = 0
            self.draws = 0

    def setup_ui(self):
        # Frame de selección de ficha
        self.select_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.select_frame.pack(pady=(20, 5))
        self.select_label = ctk.CTkLabel(
            self.select_frame,
            text="Selecciona tu ficha:",
            font=("Arial", 16)
        )
        self.select_label.pack(side="left", padx=10)
        self.x_button = ctk.CTkButton(
            self.select_frame,
            text="X",
            width=60,
            command=lambda: self.select_symbol('X'),
            fg_color="#ff0000"
        )
        self.x_button.pack(side="left", padx=10)
        self.o_button = ctk.CTkButton(
            self.select_frame,
            text="O",
            width=60,
            command=lambda: self.select_symbol('O'),
            fg_color="#00ff00"
        )
        self.o_button.pack(side="left", padx=10)

        # Marcador mejorado
        self.score_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.score_container.pack(pady=(10, 10))
        
        self.score_frame = ctk.CTkFrame(self.score_container, fg_color="transparent")
        self.score_frame.pack()
        
        self.score_frame.grid_columnconfigure(0, weight=1, minsize=140)
        self.score_frame.grid_columnconfigure(1, weight=1, minsize=140)
        self.score_frame.grid_columnconfigure(2, weight=1, minsize=140)
        
        self.create_score_card(self.score_frame, "Jugador", self.player_wins, "#00ff00", 0)
        self.create_score_card(self.score_frame, "Empates", self.draws, "#FFD700", 1)
        self.create_score_card(self.score_frame, "IA", self.ai_wins, "#ff0000", 2)
        
        self.board_frame = ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = ctk.CTkButton(
                    self.board_frame,
                    text="",
                    width=120,
                    height=120,
                    font=("Arial", 36, "bold"),
                    command=lambda r=i, c=j: self.make_move(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Selecciona tu ficha para comenzar",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)
        
        self.reset_button = ctk.CTkButton(
            self.root,
            text="Nuevo Juego",
            command=self.reset_game,
            width=200,
            height=40,
            fg_color="#00cc44"  # Verde
        )
        self.reset_button.pack(pady=20)

        self.reset_score_button = ctk.CTkButton(
            self.root,
            text="Resetear Puntaje",
            command=self.reset_score,
            width=200,
            height=40
        )
        self.reset_score_button.pack(pady=5)

        # Deshabilitar tablero hasta que elija ficha
        self.set_board_state("disabled")

    def select_symbol(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = 'O' if symbol == 'X' else 'X'
        self.status_label.configure(text=f"Tu turno ({self.player_symbol})" if self.player_symbol == 'X' else "Turno de la IA...")
        self.set_board_state("normal")
        self.x_button.configure(state="disabled")
        self.o_button.configure(state="disabled")
        self.select_label.configure(text=f"Juegas como: {self.player_symbol}")
        self.reset_game(first_time=True)

    def set_board_state(self, state):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(state=state)

    def create_score_card(self, parent, title, score, color, column):
        card_frame = ctk.CTkFrame(parent, width=130, height=90)
        card_frame.grid(row=0, column=column, padx=5, sticky="nsew")
        card_frame.grid_propagate(False)
        card_frame.grid_columnconfigure(0, weight=1)
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=("Arial", 14),
            text_color=color
        )
        title_label.pack(pady=(15, 5))
        score_label = ctk.CTkLabel(
            card_frame,
            text=str(score),
            font=("Arial", 28, "bold"),
            text_color=color
        )
        score_label.pack(pady=(0, 15))
        if "Jugador" in title:
            self.player_score_label = score_label
        elif "Empates" in title:
            self.draws_score_label = score_label
        else:
            self.ai_score_label = score_label
        
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '' or self.current_player != self.player_symbol:
            return
        self.board[row][col] = self.player_symbol
        self.buttons[row][col].configure(text=self.player_symbol, text_color="#00ff00" if self.player_symbol == 'O' else "#ff0000")
        if self.check_winner(self.player_symbol):
            self.player_wins += 1
            self.end_game("¡Has ganado! 🎉")
            return
        if self.is_board_full():
            self.draws += 1
            self.end_game("¡Empate! 🤝")
            return
        self.current_player = self.ai_symbol
        self.status_label.configure(text="Turno de la IA...")
        self.root.after(500, self.make_ai_move)
        
    def make_ai_move(self):
        if self.game_over:
            return
        move = self.get_ai_move()
        if move:
            row, col = move
            self.board[row][col] = self.ai_symbol
            self.buttons[row][col].configure(text=self.ai_symbol, text_color="#ff0000" if self.ai_symbol == 'X' else "#00ff00")
            if self.check_winner(self.ai_symbol):
                self.ai_wins += 1
                self.end_game("La IA gana 🤖")
                return
            if self.is_board_full():
                self.draws += 1
                self.end_game("¡Empate! 🤝")
                return
        self.current_player = self.player_symbol
        self.status_label.configure(text=f"Tu turno ({self.player_symbol})")
        
    def get_ai_move(self):
        free_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        if not free_cells:
            return None
        # Primer movimiento: preferir centro o esquinas
        if len(free_cells) == 9:
            if self.ai_symbol == 'X':
                if self.board[1][1] == '':
                    return (1, 1)
                else:
                    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                    available_corners = [c for c in corners if c in free_cells]
                    if available_corners:
                        return choice(available_corners)
        if len(free_cells) == 8:
            if self.board[1][1] == '':
                return (1, 1)
            else:
                corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                available_corners = [c for c in corners if c in free_cells]
                if available_corners:
                    return choice(available_corners)
        skill_roll = randrange(100)
        if skill_roll < 70:
            winning_move = self.find_winning_move(self.ai_symbol)
            if winning_move:
                return winning_move
            blocking_move = self.find_winning_move(self.player_symbol)
            if blocking_move:
                return blocking_move
            if self.board[1][1] == '':
                return (1, 1)
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            available_corners = [c for c in corners if c in free_cells]
            if available_corners:
                return choice(available_corners)
        elif skill_roll < 90:
            if randrange(2) == 0:
                blocking_move = self.find_winning_move(self.player_symbol)
                if blocking_move and randrange(3) > 0:
                    return blocking_move
        return choice(free_cells)
    
    def find_winning_move(self, player):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = player
                    if self.check_winner(player):
                        self.board[i][j] = ''
                        return (i, j)
                    self.board[i][j] = ''
        return None
    
    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False
    
    def is_board_full(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))
    
    def end_game(self, message):
        self.game_over = True
        self.status_label.configure(text=message)
        self.update_score()
        if "gana" in message:
            self.highlight_winning_line()
    
    def highlight_winning_line(self):
        for i in range(3):
            if all(self.board[i][j] == self.board[i][0] != '' for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].configure(fg_color="#FFD700")
                return
        for j in range(3):
            if all(self.board[i][j] == self.board[0][j] != '' for i in range(3)):
                for i in range(3):
                    self.buttons[i][j].configure(fg_color="#FFD700")
                return
        if all(self.board[i][i] == self.board[0][0] != '' for i in range(3)):
            for i in range(3):
                self.buttons[i][i].configure(fg_color="#FFD700")
            return
        if all(self.board[i][2-i] == self.board[0][2] != '' for i in range(3)):
            for i in range(3):
                self.buttons[i][2-i].configure(fg_color="#FFD700")
    
    def update_score(self):
        self.player_score_label.configure(text=str(self.player_wins))
        self.ai_score_label.configure(text=str(self.ai_wins))
        self.draws_score_label.configure(text=str(self.draws))
        if "ganado" in self.status_label.cget("text"):
            self.animate_score_change(self.player_score_label)
        elif "IA gana" in self.status_label.cget("text"):
            self.animate_score_change(self.ai_score_label)
        elif "Empate" in self.status_label.cget("text"):
            self.animate_score_change(self.draws_score_label)
        self.save_score()
    
    def animate_score_change(self, label):
        original_font = label.cget("font")
        label.configure(font=("Arial", 32, "bold"))
        self.root.after(300, lambda: label.configure(font=original_font))
    
    def reset_game(self, first_time=False):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = 'X'
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(
                    text="", 
                    fg_color=["#3B8ED0", "#1F6AA5"],
                    text_color="white",
                    state="normal"
                )
        if not first_time:
            self.x_button.configure(state="normal")
            self.o_button.configure(state="normal")
            self.select_label.configure(text="Selecciona tu ficha:")
            self.status_label.configure(text="Selecciona tu ficha para comenzar")
            self.set_board_state("disabled")
        else:
            if self.player_symbol == 'X':
                self.current_player = 'X'
                self.status_label.configure(text=f"Tu turno ({self.player_symbol})")
            else:
                self.current_player = 'X'
                self.status_label.configure(text="Turno de la IA...")
                self.root.after(500, self.make_ai_move)

    def reset_score(self):
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        self.update_score()
        self.save_score()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()