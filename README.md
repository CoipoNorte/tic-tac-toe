# Tic-Tac-Toe

Este proyecto implementa un juego de Tic-Tac-Toe (ta-te-ti) en consola, donde la máquina juega con ‘X’ y el usuario con ‘O’. La máquina siempre empieza colocando una ‘X’ en el centro y luego realiza movimientos aleatorios.

---

## Requisitos

- Python 3.6 o superior  
- Módulo estándar `random`  

---

## Instalación

1. Clona o descarga el repositorio.  
2. Asegúrate de tener Python 3 instalado en tu sistema.  

---

## Uso

```bash
python tic_tac_toe.py
```

Sigue las instrucciones en pantalla para ingresar un número de casilla (1–9) y jugar.

---

## Estructura del tablero

El tablero se almacena como una lista de tres filas, cada una con tres celdas.  
Cada celda contiene:  
- ‘X’ si la máquina ocupa ese espacio  
- ‘O’ si el usuario ocupa ese espacio  
- Un dígito (‘1’–‘9’) si la casilla está libre  

Acceso a una celda:  
```python
board[row][column]
```

---

## Funciones implementadas

| Función                     | Parámetros    | Descripción                                                                          |
|-----------------------------|---------------|--------------------------------------------------------------------------------------|
| display_board(board)        | board (list)  | Muestra el tablero en consola con líneas y separadores siguiendo el formato dado.    |
| make_list_of_free_fields(board) | board (list)  | Devuelve lista de tuplas `(fila, columna)` de todas las celdas libres.               |
| enter_move(board)           | board (list)  | Solicita al usuario un número válido, valida y coloca una ‘O’ en la casilla elegida. |
| victory_for(board, sign)    | board (list), sign (str) | Comprueba si el jugador con símbolo `sign` ha logrado tres en línea.           |
| draw_move(board)            | board (list)  | Selecciona aleatoriamente una casilla libre y coloca una ‘X’.                        |

---

## Flujo de juego

1. Inicialización del tablero numerado del 1 al 9.  
2. La máquina coloca su primera ‘X’ en la posición central.  
3. Bucle principal:
   - Se muestra el tablero.
   - El usuario ingresa su movimiento (`enter_move`).
   - Se comprueba victoria o empate (`victory_for`, `make_list_of_free_fields`).
   - La máquina dibuja su movimiento aleatorio (`draw_move`).
   - Se vuelve a comprobar el estado del juego.  
4. El juego termina cuando hay victoria de ‘X’, victoria de ‘O’ o empate.  

---

## Ejemplo de ejecución

```
+-------+-------+-------+
|       |       |       |
|   1   |   2   |   3   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   4   |   X   |   6   |
|       |       |       |
+-------+-------+-------+
|       |       |       |
|   7   |   8   |   9   |
|       |       |       |
+-------+-------+-------+
Ingresa tu movimiento (1-9): 1
...
¡Has ganado!
```

---

## Fundamentos de Python 1

Fundamentos de Python 1 (PE1) Examen Final de Curso

Proyecto final