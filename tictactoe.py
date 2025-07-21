from random import randrange

def display_board(board):
    """Muestra el tablero en consola con el formato especificado."""
    hr = "+-------+-------+-------+"
    for row in board:
        print(hr)
        print("|       |       |       |")
        print(f"|   {row[0]}   |   {row[1]}   |   {row[2]}   |")
        print("|       |       |       |")
    print(hr)


def make_list_of_free_fields(board):
    """
    Devuelve una lista de tuplas (fila, columna) para cada casilla Libre.
    Una casilla es libre si no contiene 'X' ni 'O'.
    """
    free = []
    for i in range(3):
        for j in range(3):
            if board[i][j] not in ('X', 'O'):
                free.append((i, j))
    return free


def enter_move(board):
    """
    Pide al usuario un número de casilla, valida la entrada
    y marca con 'O' la posición elegida.
    """
    while True:
        try:
            move = int(input("Ingresa tu movimiento (1-9): "))
            if not 1 <= move <= 9:
                raise ValueError()
        except ValueError:
            print("Entrada inválida. Debe ser entero entre 1 y 9.")
            continue

        row, col = (move - 1) // 3, (move - 1) % 3
        if board[row][col] in ('X', 'O'):
            print("La casilla ya está ocupada. Elige otra.")
        else:
            board[row][col] = 'O'
            break


def victory_for(board, sign):
    """
    Comprueba si el jugador con símbolo `sign` ('X' o 'O')
    ha ganado el juego.
    """
    # Filas y columnas
    for i in range(3):
        if all(board[i][j] == sign for j in range(3)):  # filas
            return True
        if all(board[j][i] == sign for j in range(3)):  # columnas
            return True

    # Diagonales
    if all(board[i][i] == sign for i in range(3)):
        return True
    if all(board[i][2 - i] == sign for i in range(3)):
        return True

    return False


def draw_move(board):
    """
    Elige aleatoriamente una casilla libre y marca con 'X'.
    """
    free = make_list_of_free_fields(board)
    if not free:
        return
    i, j = free[randrange(len(free))]
    board[i][j] = 'X'


def main():
    # Inicializar tablero con números 1-9 (como strings para facilitar el display)
    board = [[str(3 * i + j + 1) for j in range(3)] for i in range(3)]

    # Primer movimiento de la máquina: siempre en el centro
    board[1][1] = 'X'

    while True:
        display_board(board)

        # Turno del usuario
        enter_move(board)
        if victory_for(board, 'O'):
            display_board(board)
            print("¡Has ganado!")
            break
        if not make_list_of_free_fields(board):
            display_board(board)
            print("Empate.")
            break

        # Turno de la máquina
        draw_move(board)
        if victory_for(board, 'X'):
            display_board(board)
            print("La máquina gana.")
            break
        if not make_list_of_free_fields(board):
            display_board(board)
            print("Empate.")
            break

    print("Fin del juego.")


if __name__ == "__main__":
    main()
