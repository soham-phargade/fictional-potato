const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname)); // Serves index.html and script.js

let messages = []; // In-memory storage

// Create
app.post('/create', (req, res) => {
    const { name } = req.body;
    const id = Date.now();
    messages.push({ id, name });
    res.json({ success: true, messages });
});

// Read
app.get('/messages', (req, res) => {
    res.json(messages);
});

// Update
app.put('/update/:id', (req, res) => {
    const { id } = req.params;
    const { name } = req.body;
    messages = messages.map(msg => msg.id == id ? { ...msg, name } : msg);
    res.json({ success: true, messages });
});

// Delete
app.delete('/delete/:id', (req, res) => {
    const { id } = req.params;
    messages = messages.filter(msg => msg.id != id);
    res.json({ success: true, messages });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});