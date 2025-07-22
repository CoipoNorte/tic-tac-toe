let game;
let playerSymbol = null;
let score = { player: 0, ai: 0, draw: 0 };

function updateUI(winner) {
  // Actualiza tablero
  for (let i = 0; i < 3; i++)
    for (let j = 0; j < 3; j++) {
      const btn = document.getElementById(`cell-${i}-${j}`);
      btn.textContent = game ? game.board[i][j] : '';
      btn.disabled = !playerSymbol || (game && (game.board[i][j] !== '' || game.gameOver || game.currentPlayer !== playerSymbol));
      btn.className = 'btn tic-btn btn-outline-light';
    }

  // Estado
  const status = document.getElementById('status');
  if (winner === 'player') status.textContent = '¡Has ganado! 🎉';
  else if (winner === 'ai') status.textContent = 'La IA gana 🤖';
  else if (winner === 'draw') status.textContent = '¡Empate! 🤝';
  else if (!playerSymbol) status.textContent = 'Selecciona tu ficha para comenzar';
  else if (game.currentPlayer === playerSymbol) status.textContent = `Tu turno (${playerSymbol})`;
  else status.textContent = 'Turno de la IA...';

  // Actualiza puntaje si corresponde
  if (winner === 'ai') {
    score.ai++;
    saveScore();
  } else if (winner === 'draw') {
    score.draw++;
    saveScore();
  }

  // Puntaje
  document.getElementById('score-player').textContent = score.player;
  document.getElementById('score-ai').textContent = score.ai;
  document.getElementById('score-draw').textContent = score.draw;

  document.getElementById('board').style.opacity = playerSymbol ? '1' : '0.5';
}

function buildBoard() {
  const boardDiv = document.getElementById('board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < 3; i++) {
    const row = document.createElement('div');
    row.className = 'd-flex';
    for (let j = 0; j < 3; j++) {
      const btn = document.createElement('button');
      btn.id = `cell-${i}-${j}`;
      btn.className = 'btn tic-btn btn-outline-light';
      btn.onclick = () => {
        if (!playerSymbol) return;
        const result = game.makeMove(i, j);
        if (result === 'player') {
          score.player++;
          saveScore();
          updateUI('player');
        } else if (result === 'draw') {
          updateUI('draw');
        }
      };
      row.appendChild(btn);
    }
    boardDiv.appendChild(row);
  }
}

function saveScore() {
  fetch('/api/score', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(score)
  });
}

function loadScore() {
  fetch('/api/score')
    .then(res => res.json())
    .then(data => {
      score = data;
      updateUI();
    });
}

// Selección de ficha
document.getElementById('btn-x').onclick = () => {
  playerSymbol = 'X';
  startGame();
};
document.getElementById('btn-o').onclick = () => {
  playerSymbol = 'O';
  startGame();
};

// Nuevo juego: permite volver a elegir ficha
document.getElementById('btn-new').onclick = () => {
  playerSymbol = null;
  game = null;
  buildBoard();
  updateUI();
  document.getElementById('btn-x').disabled = false;
  document.getElementById('btn-o').disabled = false;
};

// Resetear puntaje
document.getElementById('btn-reset-score').onclick = () => {
  score = { player: 0, ai: 0, draw: 0 };
  saveScore();
  updateUI();
};

function startGame() {
  game = new TicTacToeGame(updateUI, aiMove);
  game.setSymbols(playerSymbol);
  buildBoard();
  updateUI();
  document.getElementById('btn-x').disabled = true;
  document.getElementById('btn-o').disabled = true;
  if (playerSymbol === 'O') setTimeout(() => game.aiTurn(), 500);
}

window.onload = () => {
  buildBoard();
  loadScore();
  updateUI();
};