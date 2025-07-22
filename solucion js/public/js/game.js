class TicTacToeGame {
  constructor(updateUI, aiMove) {
    this.updateUI = updateUI;
    this.aiMove = aiMove;
    this.reset();
  }

  reset() {
    this.board = Array.from({ length: 3 }, () => Array(3).fill(''));
    this.gameOver = false;
    this.currentPlayer = 'X';
  }

  setSymbols(playerSymbol) {
    this.playerSymbol = playerSymbol;
    this.aiSymbol = playerSymbol === 'X' ? 'O' : 'X';
    this.currentPlayer = 'X';
  }

  makeMove(row, col) {
    if (this.gameOver || this.board[row][col] !== '' || this.currentPlayer !== this.playerSymbol) return false;
    this.board[row][col] = this.playerSymbol;
    this.updateUI();
    if (this.checkWinner(this.playerSymbol)) {
      this.gameOver = true;
      return 'player';
    }
    if (this.isBoardFull()) {
      this.gameOver = true;
      return 'draw';
    }
    this.currentPlayer = this.aiSymbol;
    setTimeout(() => this.aiTurn(), 400);
    return true;
  }

  aiTurn() {
    if (this.gameOver) return;
    const move = this.aiMove(this.board, this.aiSymbol, this.playerSymbol);
    if (move) {
      this.board[move[0]][move[1]] = this.aiSymbol;
      this.updateUI();
      if (this.checkWinner(this.aiSymbol)) {
        this.gameOver = true;
        this.updateUI('ai');
        return;
      }
      if (this.isBoardFull()) {
        this.gameOver = true;
        this.updateUI('draw');
        return;
      }
    }
    this.currentPlayer = this.playerSymbol;
    this.updateUI();
  }

  checkWinner(player) {
    for (let i = 0; i < 3; i++)
      if (this.board[i].every(cell => cell === player)) return true;
    for (let j = 0; j < 3; j++)
      if ([0,1,2].every(i => this.board[i][j] === player)) return true;
    if ([0,1,2].every(i => this.board[i][i] === player)) return true;
    if ([0,1,2].every(i => this.board[i][2-i] === player)) return true;
    return false;
  }

  isBoardFull() {
    return this.board.flat().every(cell => cell !== '');
  }
}