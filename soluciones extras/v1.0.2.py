# tictactoe_game.py
import customtkinter as ctk
from random import randrange, choice
import sys

class TicTacToeGame:
    def __init__(self):
        # Configuración de la ventana principal
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("500x675")
        self.root.resizable(False, False)
        
        # Variables del juego
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # La máquina empieza
        self.game_over = False
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0
        
        self.setup_ui()
        self.make_ai_move()  # Primer movimiento de la IA
        
    def setup_ui(self):
        # Marcador mejorado
        self.score_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.score_container.pack(pady=(20, 10))
        
        self.score_frame = ctk.CTkFrame(self.score_container, fg_color="transparent")
        self.score_frame.pack()
        
        # Configurar grid para que las columnas tengan el mismo tamaño
        self.score_frame.grid_columnconfigure(0, weight=1, minsize=140)
        self.score_frame.grid_columnconfigure(1, weight=1, minsize=140)
        self.score_frame.grid_columnconfigure(2, weight=1, minsize=140)
        
        # Frame para cada estadística
        self.create_score_card(self.score_frame, "Jugador (O)", self.player_wins, "#00ff00", 0)
        self.create_score_card(self.score_frame, "Empates", self.draws, "#FFD700", 1)
        self.create_score_card(self.score_frame, "IA (X)", self.ai_wins, "#ff0000", 2)
        
        # Frame del tablero
        self.board_frame = ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20)
        
        # Botones del tablero
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
        
        # Label de estado
        self.status_label = ctk.CTkLabel(
            self.root,
            text="Tu turno (O)",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)
        
        # Botón de reinicio
        self.reset_button = ctk.CTkButton(
            self.root,
            text="Nuevo Juego",
            command=self.reset_game,
            width=200,
            height=40
        )
        self.reset_button.pack(pady=20)
    
    def create_score_card(self, parent, title, score, color, column):
        """Crea una tarjeta de puntuación individual"""
        card_frame = ctk.CTkFrame(parent, width=130, height=90)
        card_frame.grid(row=0, column=column, padx=5, sticky="nsew")
        card_frame.grid_propagate(False)  # Mantener tamaño fijo
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Título de la tarjeta
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=("Arial", 14),
            text_color=color
        )
        title_label.pack(pady=(15, 5))
        
        # Puntuación
        score_label = ctk.CTkLabel(
            card_frame,
            text=str(score),
            font=("Arial", 28, "bold"),
            text_color=color
        )
        score_label.pack(pady=(0, 15))
        
        # Guardar referencia para actualizar después
        if "Jugador" in title:
            self.player_score_label = score_label
        elif "Empates" in title:
            self.draws_score_label = score_label
        else:
            self.ai_score_label = score_label
        
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '' or self.current_player != 'O':
            return
        
        # Movimiento del jugador
        self.board[row][col] = 'O'
        self.buttons[row][col].configure(text='O', text_color="#00ff00")
        
        if self.check_winner('O'):
            self.end_game("¡Has ganado! 🎉")
            self.player_wins += 1
            return
        
        if self.is_board_full():
            self.end_game("¡Empate! 🤝")
            self.draws += 1
            return
        
        # Cambiar turno a la IA
        self.current_player = 'X'
        self.status_label.configure(text="Turno de la IA...")
        self.root.after(500, self.make_ai_move)  # Pequeña pausa para simular pensamiento
        
    def make_ai_move(self):
        if self.game_over:
            return
        
        # IA con comportamiento más humano
        move = self.get_ai_move()
        if move:
            row, col = move
            self.board[row][col] = 'X'
            self.buttons[row][col].configure(text='X', text_color="#ff0000")
            
            if self.check_winner('X'):
                self.end_game("La IA gana 🤖")
                self.ai_wins += 1
                return
            
            if self.is_board_full():
                self.end_game("¡Empate! 🤝")
                self.draws += 1
                return
        
        self.current_player = 'O'
        self.status_label.configure(text="Tu turno (O)")
        
    def get_ai_move(self):
        """IA que simula comportamiento humano con diferentes niveles de habilidad"""
        free_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        
        if not free_cells:
            return None
        
        # Primer movimiento: preferir centro o esquinas (comportamiento humano común)
        if len(free_cells) == 8:  # Segundo movimiento del juego
            if self.board[1][1] == '':
                return (1, 1)
            else:
                corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                available_corners = [c for c in corners if c in free_cells]
                if available_corners:
                    return choice(available_corners)
        
        # Simular diferentes niveles de habilidad
        skill_roll = randrange(100)
        
        if skill_roll < 70:  # 70% de las veces juega bien
            # Intentar ganar
            winning_move = self.find_winning_move('X')
            if winning_move:
                return winning_move
            
            # Bloquear al oponente
            blocking_move = self.find_winning_move('O')
            if blocking_move:
                return blocking_move
            
            # Tomar el centro si está disponible
            if self.board[1][1] == '':
                return (1, 1)
            
            # Tomar una esquina
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            available_corners = [c for c in corners if c in free_cells]
            if available_corners:
                return choice(available_corners)
        
        elif skill_roll < 90:  # 20% de las veces comete errores pequeños
            # A veces no ve movimientos ganadores obvios
            if randrange(2) == 0:  # 50% de probabilidad de no ver el movimiento ganador
                blocking_move = self.find_winning_move('O')
                if blocking_move and randrange(3) > 0:  # 66% de probabilidad de bloquear
                    return blocking_move
        
        # 10% de las veces hace movimientos aleatorios (errores torpes)
        return choice(free_cells)
    
    def find_winning_move(self, player):
        """Encuentra un movimiento ganador para el jugador especificado"""
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
        # Verificar filas
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        
        # Verificar columnas
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        
        # Verificar diagonales
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
        
        # Resaltar línea ganadora si hay ganador
        if "gana" in message:
            self.highlight_winning_line()
    
    def highlight_winning_line(self):
        """Resalta la línea ganadora"""
        # Verificar filas
        for i in range(3):
            if all(self.board[i][j] == self.board[i][0] != '' for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].configure(fg_color="#FFD700")
                return
        
        # Verificar columnas
        for j in range(3):
            if all(self.board[i][j] == self.board[0][j] != '' for i in range(3)):
                for i in range(3):
                    self.buttons[i][j].configure(fg_color="#FFD700")
                return
        
        # Verificar diagonal principal
        if all(self.board[i][i] == self.board[0][0] != '' for i in range(3)):
            for i in range(3):
                self.buttons[i][i].configure(fg_color="#FFD700")
            return
        
        # Verificar diagonal secundaria
        if all(self.board[i][2-i] == self.board[0][2] != '' for i in range(3)):
            for i in range(3):
                self.buttons[i][2-i].configure(fg_color="#FFD700")
    
    def update_score(self):
        """Actualiza las etiquetas de puntuación con animación"""
        self.player_score_label.configure(text=str(self.player_wins))
        self.ai_score_label.configure(text=str(self.ai_wins))
        self.draws_score_label.configure(text=str(self.draws))
        
        # Efecto de resaltado en la puntuación que cambió
        if "ganado" in self.status_label.cget("text"):
            self.animate_score_change(self.player_score_label)
        elif "IA gana" in self.status_label.cget("text"):
            self.animate_score_change(self.ai_score_label)
        elif "Empate" in self.status_label.cget("text"):
            self.animate_score_change(self.draws_score_label)
    
    def animate_score_change(self, label):
        """Anima el cambio de puntuación"""
        original_font = label.cget("font")
        label.configure(font=("Arial", 32, "bold"))
        self.root.after(300, lambda: label.configure(font=original_font))
    
    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = 'X'
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(
                    text="", 
                    fg_color=["#3B8ED0", "#1F6AA5"],
                    text_color="white"
                )
        
        self.status_label.configure(text="Turno de la IA...")
        self.root.after(500, self.make_ai_move)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()