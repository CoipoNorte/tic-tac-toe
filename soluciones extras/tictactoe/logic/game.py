from random import randrange, choice

class TicTacToeGame:
    def __init__(self, app, score_manager):
        self.app = app
        self.score_manager = score_manager
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.player_symbol = 'O'
        self.ai_symbol = 'X'
        self.buttons = None
        self.status_label = None

    def set_buttons(self, buttons):
        self.buttons = buttons

    def set_status_label(self, label):
        self.status_label = label

    def create_score_card(self, parent, title, score, color, column):
        import customtkinter as ctk
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

    def select_symbol(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = 'O' if symbol == 'X' else 'X'
        self.status_label.configure(text=f"Tu turno ({self.player_symbol})" if self.player_symbol == 'X' else "Turno de la IA...")
        self.app.set_board_state("normal")
        self.app.x_button.configure(state="disabled")
        self.app.o_button.configure(state="disabled")
        self.app.select_label.configure(text=f"Juegas como: {self.player_symbol}")
        self.reset_game(first_time=True)

    def set_board_state(self, state):
        self.app.set_board_state(state)

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '' or self.current_player != self.player_symbol:
            return
        self.board[row][col] = self.player_symbol
        self.buttons[row][col].configure(text=self.player_symbol, text_color="#00ff00" if self.player_symbol == 'O' else "#ff0000")
        if self.check_winner(self.player_symbol):
            self.score_manager.player_wins += 1
            self.end_game("¡Has ganado! 🎉")
            return
        if self.is_board_full():
            self.score_manager.draws += 1
            self.end_game("¡Empate! 🤝")
            return
        self.current_player = self.ai_symbol
        self.status_label.configure(text="Turno de la IA...")
        self.app.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        if self.game_over:
            return
        move = self.get_ai_move()
        if move:
            row, col = move
            self.board[row][col] = self.ai_symbol
            self.buttons[row][col].configure(text=self.ai_symbol, text_color="#ff0000" if self.ai_symbol == 'X' else "#00ff00")
            if self.check_winner(self.ai_symbol):
                self.score_manager.ai_wins += 1
                self.end_game("La IA gana 🤖")
                return
            if self.is_board_full():
                self.score_manager.draws += 1
                self.end_game("¡Empate! 🤝")
                return
        self.current_player = self.player_symbol
        self.status_label.configure(text=f"Tu turno ({self.player_symbol})")

    def get_ai_move(self):
        free_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        if not free_cells:
            return None
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
        self.player_score_label.configure(text=str(self.score_manager.player_wins))
        self.ai_score_label.configure(text=str(self.score_manager.ai_wins))
        self.draws_score_label.configure(text=str(self.score_manager.draws))
        if "ganado" in self.status_label.cget("text"):
            self.animate_score_change(self.player_score_label)
        elif "IA gana" in self.status_label.cget("text"):
            self.animate_score_change(self.ai_score_label)
        elif "Empate" in self.status_label.cget("text"):
            self.animate_score_change(self.draws_score_label)
        self.score_manager.save_score()

    def animate_score_change(self, label):
        original_font = label.cget("font")
        label.configure(font=("Arial", 32, "bold"))
        self.app.root.after(300, lambda: label.configure(font=original_font))

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
            self.app.x_button.configure(state="normal")
            self.app.o_button.configure(state="normal")
            self.app.select_label.configure(text="Selecciona tu ficha:")
            self.status_label.configure(text="Selecciona tu ficha para comenzar")
            self.set_board_state("disabled")
        else:
            if self.player_symbol == 'X':
                self.current_player = 'X'
                self.status_label.configure(text=f"Tu turno ({self.player_symbol})")
            else:
                self.current_player = 'X'
                self.status_label.configure(text="Turno de la IA...")
                self.app.root.after(500, self.make_ai_move)

    def reset_score(self):
        self.score_manager.player_wins = 0
        self.score_manager.ai_wins = 0
        self.score_manager.draws = 0
        self.update_score()
        self.score_manager.save_score()