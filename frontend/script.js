const apiUrl = 'http://localhost:8000'; // Adjust if your FastAPI server is running on a different port

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const name = document.getElementById('name').value;

    try {
        const response = await fetch(`${apiUrl}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({email, name}),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const user = await response.json();
        alert(`User created: ${JSON.stringify(user)}`);
    } catch (error) {
        alert(`Failed to create user: ${error.message}`);
    }
});

document.getElementById('getUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('getEmail').value;

    try {
        const response = await fetch(`${apiUrl}/users/${email}`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const user = await response.json();
        document.getElementById('userDetails').innerText = `User details: ${JSON.stringify(user)}`;
    } catch (error) {
        document.getElementById('userDetails').innerText = `Failed to fetch user: ${error.message}`;
    }
});

document.getElementById('listUsersButton').addEventListener('click', async () => {
    try {
        const response = await fetch(`${apiUrl}/users/`);
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const users = await response.json();
        const userList = document.getElementById('userList');
        userList.innerHTML = '';
        users.forEach(user => {
            const listItem = document.createElement('li');
            listItem.textContent = `${user.name} (${user.email})`;
            userList.appendChild(listItem);
        });
    } catch (error) {
        alert(`Failed to list users: ${error.message}`);
    }
});