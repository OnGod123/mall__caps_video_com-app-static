document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.form');
  const usernameInput = form.querySelector('input[name="username"]');
  const passwordInput = form.querySelector('input[name="password"]');

  form.addEventListener('submit', async function (event) {
    event.preventDefault(); // stop normal navigation

    const formData = new FormData();
    formData.append('username', usernameInput.value.trim());
    formData.append('password', passwordInput.value);

    try {
      const response = await fetch('/login', {
        method: 'POST',
        body: formData, // multipart/form-data automatically
        credentials: 'include', // send cookies
        redirect: 'follow' // default, but explicit for clarity
      });

      // If backend redirected (302 -> final URL), fetch follows it but doesn't change window location.
      if (response.redirected) {
        window.location.href = response.url;
        return;
      }

      // Otherwise, assume an error or JSON payload
      const contentType = response.headers.get('Content-Type') || '';
      if (contentType.includes('application/json')) {
        const data = await response.json();
        if (response.ok) {
          // in case backend ever returns success JSON
          if (data.redirectUrl) {
            window.location.href = data.redirectUrl;
          } else {
            alert('Login succeeded but no redirect provided.');
          }
        } else {
          alert(data.message || 'Login failed');
        }
      } else {
        // fallback: if HTML returned (e.g., login page with error), replace current document
        const text = await response.text();
        document.open();
        document.write(text);
        document.close();
      }
    } catch (err) {
      console.error('Login error:', err);
      alert('An error occurred. Please try again.');
    }
  });
});


