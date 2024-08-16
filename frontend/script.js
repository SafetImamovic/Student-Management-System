function createUserType() {
    const formData = {
        name: document.getElementById('user-type-name').value
    };

    fetch('http://localhost:8000/user_types/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.detail || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
        showToast('User Type created successfully.');
        document.getElementById('user-type-form').reset(); // Clear the form
    })
    .catch(error => {
        showToast(`Error creating user type: ${error.message}`);
    });
}

// Function to populate user type dropdown
function populateUserTypes() {
    fetch('http://localhost:8000/user_types/') // Adjust URL as necessary
        .then(response => response.json())
        .then(data => {
            const userTypeSelect = document.getElementById('user-type-id');
            userTypeSelect.innerHTML = ''; // Clear existing options
            data.forEach(userType => {
                const option = document.createElement('option');
                option.value = userType.user_type_id; // Assuming the user type object has 'id'
                option.textContent = 'ID: ' + userType.user_type_id + ", Name: " + userType.name; // Assuming the user type object has 'name'
                userTypeSelect.appendChild(option);
            });
        })
        .catch(error => {
            showToast(`Error fetching user types: ${error.message}`);
        });
}

// Call populateUserTypes on page load
window.onload = function() {
    populateUserTypes();
};


let coll = document.getElementsByClassName("collapsible");
let i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    let content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
function fetchUserInfoById() {
    const userId = document.getElementById('user-id').value;
    const userInfoDiv = document.getElementById('user-info');

    if (!userId) {
        userInfoDiv.innerHTML = '<div class="alert alert-danger">Please enter a valid User ID.</div>';
        return;
    }

    fetch(`http://localhost:8000/users/${userId}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            userInfoDiv.innerHTML = generateUserHTML(data) + generateActionsHTML(data);
        })
        .catch(error => {
            userInfoDiv.innerHTML = `<div class="alert alert-danger">Error fetching user information: ${error.message}</div>`;
        });
}

function fetchUserInfoByEmail() {
    const userEmail = document.getElementById('user-email').value;
    const userInfoDiv = document.getElementById('user-info');

    if (!userEmail) {
        userInfoDiv.innerHTML = '<div class="alert alert-danger">Please enter a valid User Email.</div>';
        return;
    }

    fetch(`http://localhost:8000/users/email/${encodeURIComponent(userEmail)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            userInfoDiv.innerHTML = generateUserHTML(data) + generateActionsHTML(data);
        })
        .catch(error => {
            userInfoDiv.innerHTML = `<div class="alert alert-danger">Error fetching user information: ${error.message}</div>`;
        });
}

function fetchUserList() {
    const skip = document.getElementById('skip').value || 0;
    const limit = document.getElementById('limit').value || 10;
    const userListDiv = document.getElementById('user-list');

    fetch(`http://localhost:8000/users/?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                userListDiv.innerHTML = '<div class="alert alert-info">No users found.</div>';
                return;
            }

            userListDiv.innerHTML = data.map(user => generateUserSummaryHTML(user)).join('');
        })
        .catch(error => {
            userListDiv.innerHTML = `<div class="alert alert-danger">Error fetching user list: ${error.message}</div>`;
        });
}

function fetchUserTypesList()
{
    const skip = document.getElementById('skip_types').value || 0;
    const limit = document.getElementById('limit_types').value || 10;
    const userListDiv = document.getElementById('user-types-list');

    fetch(`http://localhost:8000/user_types/?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                userListDiv.innerHTML = '<div class="alert alert-info">No user types found.</div>';
                return;
            }

            userListDiv.innerHTML = data.map(type => generateUserTypesHTML(type)).join('');
        })
        .catch(error => {
            userListDiv.innerHTML = `<div class="alert alert-danger">Error fetching user types list: ${error.message}</div>`;
        });
}


function generateUserHTML(user) {
    return `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">${user.first_name} ${user.last_name}</h5>
                <p class="card-text"><strong>User ID:</strong> ${user.user_id} <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${user.user_id}')">Copy</button></p>
                <p class="card-text"><strong>Username:</strong> ${user.username}</p>
                <p class="card-text"><strong>Email:</strong> ${user.email} <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${user.email}')">Copy</button></p>
                <p class="card-text"><strong>Age:</strong> ${user.age}</p>
                <p class="card-text"><strong>Active:</strong> ${user.is_active}</p>
                <p class="card-text"><strong>User Type ID:</strong> ${user.user_type_id}</p>
                <p class="card-text"><strong>Created At:</strong> ${new Date(user.created_at).toLocaleString()}</p>
                <p class="card-text"><strong>Updated At:</strong> ${new Date(user.updated_at).toLocaleString()}</p>
                <p class="card-text"><strong>Last Login:</strong> ${new Date(user.last_login).toLocaleString()}</p>
            </div>
        </div>`;
}

function generateUserSummaryHTML(user) {
    return `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${user.first_name} ${user.last_name}</h5>
                <p class="card-text"><strong>User ID:</strong> ${user.user_id} <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${user.user_id}')">Copy</button></p>
                <p class="card-text"><strong>Username:</strong> ${user.username}</p>
                <p class="card-text"><strong>Email:</strong> ${user.email} <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${user.email}')">Copy</button></p>
                <button class="btn btn-secondary" onclick="fillForm('${user.user_id}', '${user.first_name}', '${user.last_name}', '${user.username}', '${user.email}', ${user.age}, ${user.is_active}, '${user.user_type_id}')">Fill Form</button>
                <button class="btn btn-danger" onclick="deleteUser('${user.user_id}')">Delete</button>
            </div>
        </div>`;
}

function generateUserTypesHTML(type)
{
    return `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${type.name}</h5>
                <p class="card-text"><strong>User Type ID:</strong> ${type.user_type_id} <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${type.user_type_id}')">Copy</button></p>
                <p class="card-text"><strong>Created At:</strong> ${new Date(type.created_at).toLocaleString()}</p>
                <p class="card-text"><strong>Updated At:</strong> ${new Date(type.updated_at).toLocaleString()}</p>
                <div class="mt-3">
                    <button class="btn btn-danger" onclick="deleteUserType('${type.user_type_id}')">Delete</button>
                </div>
            </div>
        </div>`;
}

function generateActionsHTML(user) {
    return `
        <div class="mt-3">
            <button class="btn btn-secondary" onclick="fillForm('${user.user_id}', '${user.first_name}', '${user.last_name}', '${user.username}', '${user.email}', ${user.age}, ${user.is_active}, '${user.user_type_id}')">Fill Form</button>
            <button class="btn btn-danger" onclick="deleteUser('${user.user_id}')">Delete</button>
        </div>`;
}

function fillForm(userId, firstName, lastName, username, email, age, isActive, userTypeId) {
    document.getElementById('first-name').value = firstName;
    document.getElementById('last-name').value = lastName;
    document.getElementById('username').value = username;
    document.getElementById('email').value = email;
    document.getElementById('age').value = age;
    document.getElementById('is-active').checked = isActive;
    document.getElementById('user-type-id').value = userTypeId;
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(`http://localhost:8000/delete_users/${userId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    showToast('User deleted successfully.');
                    fetchUserList(); // Refresh the user list
                } else {
                    return response.json().then(errorData => {
                        throw new Error(errorData.detail || 'Unknown error');
                    });
                }
            })
            .catch(error => {
                showToast(`Error deleting user: ${error.message}`);
            });
    }
}

function deleteUserType(user_type_id)
{
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(`http://localhost:8000/delete_user_types/${user_type_id}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    showToast('User deleted successfully.');
                    fetchUserTypesList(); // Refresh the user list
                } else {
                    return response.json().then(errorData => {
                        throw new Error(errorData.detail || 'Unknown error');
                    });
                }
            })
            .catch(error => {
                showToast(`Error deleting user: ${error.message}`);
            });
    }
}

function createUser() {
    const formData = {
        first_name: document.getElementById('first-name').value,
        last_name: document.getElementById('last-name').value,
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        age: parseInt(document.getElementById('age').value),
        is_active: document.getElementById('is-active').checked,
        user_type_id: parseInt(document.getElementById('user-type-id').value),
        password: document.getElementById('password').value
    };

    console.log(formData);

    fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            showToast('User created successfully.');
            document.getElementById('user-form').reset(); // Clear the form
        })
        .catch(error => {
            showToast(`Error creating user: ${error.message}`);
        });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard.');
    }).catch(err => {
        showToast('Failed to copy to clipboard.');
    });
}

function showToast(message) {
    const toastContainer = document.getElementById('toast-container');
    const toastHTML = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-body bg-dark text-light">
                ${message}
            </div>
        </div>`;
    toastContainer.innerHTML = toastHTML;
    const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
    toast.show();
}