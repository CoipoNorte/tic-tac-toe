const express = require('express');
const path = require('path');
const scoreRoutes = require('./routes/score');
const app = express();

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use('/api/score', scoreRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});