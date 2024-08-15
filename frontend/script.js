const apiUrl = 'http://localhost:8000'; // Adjust if your FastAPI server is running on a different port

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const user = {
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        username: formData.get('username'),
        email: formData.get('email'),
        age: parseInt(formData.get('age'), 10),
        is_active: formData.get('is_active') === 'on',
        password: formData.get('password'),
        user_type_id: parseInt(formData.get('user_type_id'), 10),
    };

    try {
        const response = await fetch(`${apiUrl}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(user),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const createdUser = await response.json();
        alert(`User created: ${JSON.stringify(createdUser)}`);
        document.getElementById('createUserForm').reset(); // Reset form after successful creation
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
        document.getElementById('userDetails').innerHTML = `
            <p><strong>First Name:</strong> ${user.first_name}</p>
            <p><strong>Last Name:</strong> ${user.last_name}</p>
            <p><strong>Username:</strong> ${user.username}</p>
            <p><strong>Email:</strong> ${user.email}</p>
            <p><strong>Age:</strong> ${user.age}</p>
            <p><strong>Active:</strong> ${user.is_active}</p>
            <p><strong>User ID:</strong> ${user.user_id}</p>
            <p><strong>Created At:</strong> ${new Date(user.created_at).toLocaleString()}</p>
            <p><strong>Updated At:</strong> ${new Date(user.updated_at).toLocaleString()}</p>
            <p><strong>Last Login:</strong> ${new Date(user.last_login).toLocaleString()}</p>
        `;
    } catch (error) {
        document.getElementById('userDetails').innerHTML = `Failed to fetch user: ${error.message}`;
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
            listItem.setAttribute('data-user-id', user.user_id); // Set user ID for deletion
            listItem.innerHTML = `
                <strong>Username:</strong> ${user.username}
                (<strong>Email:</strong> ${user.email},
                <strong>Active:</strong> ${user.is_active},
                <strong>Created At:</strong> ${new Date(user.created_at).toLocaleString()})
                <button class="delete-button">Delete</button>
            `;
            userList.appendChild(listItem);
        });

        // Attach event listeners to delete buttons
        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', handleDelete);
        });
    } catch (error) {
        alert(`Failed to list users: ${error.message}`);
    }
});

// Function to handle deletion of a user
async function handleDelete(event) {
    const userId = event.target.parentElement.getAttribute('data-user-id');

    if (confirm('Are you sure you want to delete this user?')) {
        try {
            const response = await fetch(`${apiUrl}/del_user/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete user');
            }

            // Remove the user from the list if the deletion was successful
            event.target.parentElement.remove();
            alert('User deleted successfully');
        } catch (error) {
            console.error('Error deleting user:', error);
            alert('There was an error deleting the user');
        }
    }
}