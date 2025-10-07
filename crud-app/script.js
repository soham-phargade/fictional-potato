document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const input = form.querySelector('input[name="name"]');
    const messagesDiv = document.createElement('div');
    document.body.appendChild(messagesDiv);

    // Fetch and display messages
    function loadMessages() {
        fetch('/messages')
            .then(res => res.json())
            .then(messages => {
                messagesDiv.innerHTML = '';
                messages.forEach(msg => {
                    const msgEl = document.createElement('div');
                    msgEl.textContent = msg.name;
                    // Edit button
                    const editBtn = document.createElement('button');
                    editBtn.textContent = 'Edit';
                    editBtn.onclick = () => {
                        const newName = prompt('Edit message:', msg.name);
                        if (newName) updateMessage(msg.id, newName);
                    };
                    // Delete button
                    const delBtn = document.createElement('button');
                    delBtn.textContent = 'Delete';
                    delBtn.onclick = () => deleteMessage(msg.id);
                    msgEl.appendChild(editBtn);
                    msgEl.appendChild(delBtn);
                    messagesDiv.appendChild(msgEl);
                });
            });
    }

    // Create
    form.onsubmit = (e) => {
        e.preventDefault();
        fetch('/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: input.value })
        })
        .then(res => res.json())
        .then(() => {
            input.value = '';
            loadMessages();
        });
    };

    // Update
    function updateMessage(id, name) {
        fetch(`/update/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        })
        .then(res => res.json())
        .then(loadMessages);
    }

    // Delete
    function deleteMessage(id) {
        fetch(`/delete/${id}`, { method: 'DELETE' })
            .then(res => res.json())
            .then(loadMessages);
    }

    loadMessages();
});