
async function signupUser() {
  const firstName = document.getElementById('first-name').value;
  const lastName = document.getElementById('last-name').value;
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const gender = document.querySelector('input[name="one"]:checked')?.value;

  const userData = {
    first_name: firstName,
    last_name: lastName,
    username: username,
    email: email,
    password: password,
    gender: gender
  };

  try {
    const response = await fetch('/auth/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });

    if (response.ok) {
      alert('Signup successful! Redirecting...');
      window.location.href = signupRedirectUrl;  // ✅ Redirect URL here
    } else {
      const errorData = await response.json();
      alert('Signup failed: ' + JSON.stringify(errorData));
      console.error('Error:', errorData);
    }
  } catch (error) {
    console.error('Network error:', error);
    alert('An error occurred. Please try again later.');
  }
}

// Link this to a submit button:
// <button onclick="signupUser()">Sign Up</button>
