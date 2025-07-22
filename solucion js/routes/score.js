const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();

const scorePath = path.join(__dirname, '..', 'data', 'score.json');

// Leer puntaje
router.get('/', (req, res) => {
  if (fs.existsSync(scorePath)) {
    const data = fs.readFileSync(scorePath, 'utf8');
    res.json(JSON.parse(data));
  } else {
    res.json({ player: 0, ai: 0, draw: 0 });
  }
});

// Guardar puntaje
router.post('/', (req, res) => {
  fs.writeFileSync(scorePath, JSON.stringify(req.body));
  res.json({ status: 'ok' });
});

module.exports = router;