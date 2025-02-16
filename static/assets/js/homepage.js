document.addEventListener('DOMContentLoaded', () => {
  tokenchecker();
  fetchUserDetails();
});

///checks if token is present
async function tokenchecker() {
  const token = localStorage.getItem('access_token');
  if (!token) {
    window.location.href = loginpage; // Redirect to login if no token
  }
}

console.log('homepage.js loaded');

//fetch user details
async function fetchUserDetails() {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  try {
    const response = await fetch('/auth/users/me/', {
      headers: {
        'Authorization': `JWT ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) throw new Error('Failed to fetch user details');

    const user = await response.json();
    document.getElementById('username-display').innerText = user.username;
  } catch (error) {
    console.error('Error fetching user details:', error);
  }
}

