url_address = "http://localhost:8000/"

// -------------------------------------------------------------------------------------------------
// Different Routes
// -------------------------------------------------------------------------------------------------
routes = {
    "user_types/": "user_types/",
    "users/": "users/",
    "users/email/": "users/email/",
    "delete_users/": "delete_users/",
    "delete_user_types/": "delete_user_types/",
    "truncate_db/": "truncate_db/",
    "re_seed_db/": "re_seed_db/",
    "users_count/": "users_count/",
    "user_types_count/": "user_types_count/",
    "courses_count/": "courses_count/",
    "enrollments_count/": "enrollments_count/",
    "enrollments/": "enrollments/",
    "courses/": "courses/",
    "delete_enrollment/": "delete_enrollment/",
}


// -------------------------------------------------------------------------------------------------
// TRUNCATES every table in the database
// -------------------------------------------------------------------------------------------------
function truncate() {
    if (confirm('Are you sure you want to TRUNCATE every table in the database?')) {
        fetch(url_address + routes["truncate_db/"], {method: 'DELETE'})
            .then(response => {
                if (response.ok) {
                    showToast('Tables TRUNCATED successfully.');
                    fetchUserTypesList();
                } else {
                    return response.json().then(errorData => {
                        throw new Error(errorData.detail || 'Unknown error');
                    });
                }
            })
            .catch(error => {
                showToast(`Error TRUNCATING tables: ${error.message}`);
            });
    }

    updateCounts();
}


// -------------------------------------------------------------------------------------------------
// RE-SEEDS some tables in the database
// -------------------------------------------------------------------------------------------------
function re_seed() {
    fetch(url_address + routes["re_seed_db/"], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
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
            showToast('Database table re-seeded successfully.');
            document.getElementById('user-type-form').reset(); // Clear the form
        })
        .catch(error => {
            showToast(`Error reseeding database tables: ${error.message}`);
        });

    updateCounts();
}


// -------------------------------------------------------------------------------------------------
// Update table counts
// -------------------------------------------------------------------------------------------------
function updateCounts() {
    // <p id="user_types_count"></p>
    // <p id="users_count"></p>
    // <p id="courses_count"></p>
    // <p id="enrollments_count"></p>
    const user_types_count = document.getElementById('user_types_count');
    const users_count = document.getElementById('users_count');
    const courses_count = document.getElementById('courses_count');
    const enrollments_count = document.getElementById('enrollments_count');

    fetch(url_address + routes["user_types_count/"])
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
                user_types_count.innerText = `ERROR`;
                return;
            }

            user_types_count.innerText = `User Types Count: ${data}`;
        })
        .catch(error => {

        });


    fetch(url_address + routes["users_count/"])
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
                users_count.innerText = `ERROR`;
                return;
            }

            users_count.innerText = `Users Count: ${data}`;
        })
        .catch(error => {

        });


    fetch(url_address + routes["courses_count/"])
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
                courses_count.innerText = `ERROR`;
                return;
            }

            courses_count.innerText = `Courses Count: ${data}`;
        })
        .catch(error => {

        });


    fetch(url_address + routes["enrollments_count/"])
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
                enrollments_count.innerText = `ERROR`;
                return;
            }

            enrollments_count.innerText = `Enrollments Count: ${data}`;
        })
        .catch(error => {

        });
}


// -------------------------------------------------------------------------------------------------
// Fetch All User Types
// -------------------------------------------------------------------------------------------------
function fetchUserTypesList() {
    const skip = document.getElementById('skip_types').value || 0;
    const limit = document.getElementById('limit_types').value || 10;
    const userListDiv = document.getElementById('user-types-list');

    fetch(url_address + routes["user_types/"] + `?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`)
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


// -------------------------------------------------------------------------------------------------
// Add New User Type
// -------------------------------------------------------------------------------------------------
function createUserType() {
    const formData = {
        name: document.getElementById('user-type-name').value
    };

    console.log(JSON.stringify(formData))

    fetch(url_address + routes["user_types/"], {
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


// -------------------------------------------------------------------------------------------------
// Fetch Specific User
// -------------------------------------------------------------------------------------------------
function fetchUserInfoById() {
    const userId = document.getElementById('user-id').value;
    const userInfoDiv = document.getElementById('user-info');

    if (!userId) {
        userInfoDiv.innerHTML = '<div class="alert alert-danger">Please enter a valid User ID.</div>';
        return;
    }

    fetch(url_address + routes["users/"] + `${userId}`)
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

    fetch(url_address + routes["users/email/"] + `${encodeURIComponent(userEmail)}`)
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


// -------------------------------------------------------------------------------------------------
// Fetch All Users
// -------------------------------------------------------------------------------------------------
function fetchUserList() {
    const skip = document.getElementById('skip').value || 0;
    const limit = document.getElementById('limit').value || 10;
    const userListDiv = document.getElementById('user-list');

    fetch(url_address + routes["users/"] + `?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`)
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


// -------------------------------------------------------------------------------------------------
// Add New User
// -------------------------------------------------------------------------------------------------
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

    fetch(url_address + routes["users/"], {
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


// -------------------------------------------------------------------------------------------------
// Fetch All Courses
// -------------------------------------------------------------------------------------------------
function fetchCourseList() {
    const skip = document.getElementById('skip_course').value || 0;
    const limit = document.getElementById('limit_course').value || 10;
    const userListDiv = document.getElementById('course-list');

    fetch(url_address + routes["courses/"] + `?skip=${encodeURIComponent(skip)}&limit=${encodeURIComponent(limit)}`)
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
                userListDiv.innerHTML = '<div class="alert alert-info">No courses found.</div>';
                return;
            }

            userListDiv.innerHTML = data.map(course => generateCourseSummaryHTML(course)).join('');
        })
        .catch(error => {
            userListDiv.innerHTML = `<div class="alert alert-danger">Error fetching course list: ${error.message}</div>`;
        });
}


// -------------------------------------------------------------------------------------------------
// Enrollment Management
// -------------------------------------------------------------------------------------------------
const enrollmentForm = document.getElementById('enrollmentForm');
const enrollmentTableBody = document.querySelector('#enrollmentTable tbody');

// Fetch, display and POST enrollments
function fetchEnrollments() {
    fetch(url_address + routes["enrollments/"])
        .then(response => response.json())
        .then(data => {
            enrollmentTableBody.innerHTML = '';
            data.forEach(enrollment => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${enrollment.enrolled_date}</td>
                    <td>${enrollment.end_date}</td>
                    <td>${enrollment.associative_data}</td>
                    <td>${enrollment.user_id}</td>
                    <td>${enrollment.course_id}</td>
                `;
                enrollmentTableBody.appendChild(row);
                // row.innerHTML += `<button className="btn btn-danger" onClick="deleteEnrollment(${enrollment.enrollment_id})">Delete</button>`
            });
        });
}

function deleteEnrollment(id) {
    if (confirm('Are you sure you want to delete this enrollment?')) {
        fetch(url_address + routes["delete_enrollment/"] + `${id}`, {method: 'DELETE'})
            .then(response => {
                if (response.ok) {
                    showToast('Enrollment deleted successfully.');
                    fetchEnrollments();
                } else {
                    return response.json().then(errorData => {
                        throw new Error(errorData.detail || 'Unknown error');
                    });
                }
            })
            .catch(error => {
                showToast(`Error deleting enrollment: ${error.message}`);
            });
    }
}


enrollmentForm.addEventListener('submit', event => {
    event.preventDefault();
    const formData = new FormData(enrollmentForm);
    const jsonData = JSON.stringify(Object.fromEntries(formData.entries()));

    fetch(url_address + routes["enrollments/"], {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData
    }).then(response => {
        if (response.ok) {
            showToast('Enrollment added successfully.');
            fetchEnrollments();
        } else {
            return response.json().then(errorData => {
                throw new Error(errorData.detail || 'Unknown error');
            });
        }
    }).catch(error => {
        showToast(`Error creating enrollment: ${error.message}`);
    });
});

const userIdSelect = document.getElementById('userIdEnrollment');
const courseIdSelect = document.getElementById('courseIdEnrollment');

// Fetch and populate user options
function fetchUsers() {
    fetch(url_address + routes["users/"])
        .then(response => response.json())
        .then(users => {
            userIdSelect.innerHTML = '<option value="" disabled selected>Select a user</option>';
            users.forEach(user => {
                const option = document.createElement('option');
                option.value = user.user_id;
                option.textContent = `${user.first_name} ${user.last_name} (${user.username})`;
                userIdSelect.appendChild(option);
            });
        });
}

// Fetch and populate course options
function fetchCourses() {
    fetch(url_address + routes["courses/"])
        .then(response => response.json())
        .then(courses => {
            courseIdSelect.innerHTML = '<option value="" disabled selected>Select a course</option>';
            courses.forEach(course => {
                const option = document.createElement('option');
                option.value = course.course_id;
                option.textContent = course.name;
                courseIdSelect.appendChild(option);
            });
        });
}


// -------------------------------------------------------------------------------------------------
// Generates the HTML for User info
// -------------------------------------------------------------------------------------------------
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


// -------------------------------------------------------------------------------------------------
// Generates the HTML for User Type info
// -------------------------------------------------------------------------------------------------
function generateUserTypesHTML(type) {
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


// -------------------------------------------------------------------------------------------------
// Generates the HTML for Course info
// -------------------------------------------------------------------------------------------------
function generateCourseSummaryHTML(course) {
    return `
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">${course.name}</h5>
                <p class="card-text"><strong>Course ID:</strong> ${course.course_id} <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${course.course_id}')">Copy</button></p>
                <p class="card-text"><strong>Description:</strong> ${course.description} </p>
                <p class="card-text"><strong>Start Date:</strong> ${new Date(course.start_date).toLocaleString()}</p>
                <p class="card-text"><strong>End Date:</strong> ${new Date(course.end_date).toLocaleString()}</p>
                <p class="card-text"><strong>Created At:</strong> ${new Date(course.created_at).toLocaleString()}</p>
                <p class="card-text"><strong>Updated At:</strong> ${new Date(course.updated_at).toLocaleString()}</p>
                <div class="mt-3">
                    <button class="btn btn-danger" onclick="deleteUserType('${course.course_id}')">Delete</button>
                </div>
            </div>
        </div>`;
}


// -------------------------------------------------------------------------------------------------
// Deletes the User
// -------------------------------------------------------------------------------------------------
function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(url_address + routes["delete_users/"] + `${userId}`, {method: 'DELETE'})
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


// -------------------------------------------------------------------------------------------------
// Deletes the User Type
// -------------------------------------------------------------------------------------------------
function deleteUserType(user_type_id) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(url_address + routes["delete_user_types/"] + `${user_type_id}`, {method: 'DELETE'})
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


// -------------------------------------------------------------------------------------------------
// Other Functions
// -------------------------------------------------------------------------------------------------
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


// -------------------------------------------------------------------------------------------------
// Code that manages the collapsible elements
// -------------------------------------------------------------------------------------------------
let coll = document.getElementsByClassName("collapsible");
let i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        let content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}


// -------------------------------------------------------------------------------------------------
// Function to populate user type dropdown
// -------------------------------------------------------------------------------------------------
function populateUserTypes() {
    fetch(url_address + routes["user_types/"]) // Adjust URL as necessary
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
window.onload = function () {
    populateUserTypes();
};

fetchEnrollments();
fetchUsers();
fetchCourses();
