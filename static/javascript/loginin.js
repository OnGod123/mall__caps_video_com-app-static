document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.form');
  const usernameInput = form.querySelector('input[type="text"]');
  const passwordInput = form.querySelector('input[type="password"]');

  form.addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent traditional form submit

    const username = usernameInput.value;
    const password = passwordInput.value;

    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',  // <-- Added this line to send cookies
        body: JSON.stringify({ username, password })
      });

      if (response.ok) {
        // Assume server sends { success: true, redirectUrl: "/dashboard" }
        const data = await response.json();
        if (data.success) {
          window.location.href = data.redirectUrl || '/dashboard'; // fallback if no redirectUrl
        } else {
          alert(data.message || 'Login failed');
        }
      } else {
        const errorData = await response.json();
        alert(errorData.message || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      alert('An error occurred. Please try again.');
    }
  });
});

