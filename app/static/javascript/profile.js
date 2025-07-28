 fetch('/api/profile')
        .then(res => {
          if (!res.ok) throw new Error('Failed to fetch profile');
          return res.json();
        })
        .then(data => {
          document.getElementById('username').textContent = data.username;
          document.getElementById('bio').textContent = data.bio;
          document.getElementById('profile-pic').src = data.image;
        })
        .catch(error => {
          document.getElementById('username').textContent = 'Error loading profile';
          document.getElementById('bio').textContent = error.message;
          document.getElementById('profile-pic').src = 'https://via.placeholder.com/100';
        });
    };
