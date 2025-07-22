function aiMove(board, aiSymbol, playerSymbol) {
  // IA simple: primero intenta ganar, luego bloquear, luego centro, luego esquinas, luego random
  function findWinningMove(symbol) {
    for (let i = 0; i < 3; i++)
      for (let j = 0; j < 3; j++)
        if (board[i][j] === '') {
          board[i][j] = symbol;
          if (new TicTacToeGame(()=>{},()=>{}).checkWinner.call({board}, symbol)) {
            board[i][j] = '';
            return [i, j];
          }
          board[i][j] = '';
        }
    return null;
  }
  let move = findWinningMove(aiSymbol) || findWinningMove(playerSymbol);
  if (move) return move;
  if (board[1][1] === '') return [1, 1];
  const corners = [[0,0],[0,2],[2,0],[2,2]].filter(([i,j]) => board[i][j] === '');
  if (corners.length) return corners[Math.floor(Math.random()*corners.length)];
  const free = [];
  for (let i=0;i<3;i++) for (let j=0;j<3;j++) if (board[i][j]==='') free.push([i,j]);
  return free.length ? free[Math.floor(Math.random()*free.length)] : null;
}