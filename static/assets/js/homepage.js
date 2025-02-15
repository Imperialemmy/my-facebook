async function getUserProfile() {
  const token = localStorage.getItem('access_token');
  if (!token) {
    alert('You need to log in first.');
    window.location.href = loginpage;
    return;
  }

  try {
    const response = await fetch('/auth/users/me/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    const userData = await response.json();

    if (response.ok) {
      document.getElementById('welcome-msg').innerText = `Welcome, ${userData.first_name}!`;
    } else {
      alert('Failed to fetch user info.');
    }
  } catch (error) {
    alert('Network error. Please try again.');
  }
}














