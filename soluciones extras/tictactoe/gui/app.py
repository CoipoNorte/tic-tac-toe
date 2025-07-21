import customtkinter as ctk
from logic.game import TicTacToeGame
from data.score_manager import ScoreManager

class TicTacToeApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x800")
        self.root.resizable(False, False)

        self.score_manager = ScoreManager()
        self.game = TicTacToeGame(self, self.score_manager)

        self.setup_ui()
        self.set_board_state("disabled")

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
            command=lambda: self.game.select_symbol('X'),
            fg_color="#ff0000"
        )
        self.x_button.pack(side="left", padx=10)
        self.o_button = ctk.CTkButton(
            self.select_frame,
            text="O",
            width=60,
            command=lambda: self.game.select_symbol('O'),
            fg_color="#00ff00"
        )
        self.o_button.pack(side="left", padx=10)

        # Marcador
        self.score_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.score_container.pack(pady=(10, 10))
        self.score_frame = ctk.CTkFrame(self.score_container, fg_color="transparent")
        self.score_frame.pack()
        self.score_frame.grid_columnconfigure(0, weight=1, minsize=140)
        self.score_frame.grid_columnconfigure(1, weight=1, minsize=140)
        self.score_frame.grid_columnconfigure(2, weight=1, minsize=140)
        self.game.create_score_card(self.score_frame, "Jugador", self.score_manager.player_wins, "#00ff00", 0)
        self.game.create_score_card(self.score_frame, "Empates", self.score_manager.draws, "#FFD700", 1)
        self.game.create_score_card(self.score_frame, "IA", self.score_manager.ai_wins, "#ff0000", 2)

        # Tablero
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
                    command=lambda r=i, c=j: self.game.make_move(r, c)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        self.game.set_buttons(self.buttons)

        # Estado
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Selecciona tu ficha para comenzar",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)
        self.game.set_status_label(self.status_label)

        # Botón nuevo juego
        self.reset_button = ctk.CTkButton(
            self.root,
            text="Nuevo Juego",
            command=self.game.reset_game,
            width=200,
            height=40,
            fg_color="#00cc44"
        )
        self.reset_button.pack(pady=20)

        # Botón resetear puntaje
        self.reset_score_button = ctk.CTkButton(
            self.root,
            text="Resetear Puntaje",
            command=self.game.reset_score,
            width=200,
            height=40
        )
        self.reset_score_button.pack(pady=5)

    def set_board_state(self, state):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(state=state)

    def run(self):
        self.root.mainloop()