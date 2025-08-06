<script>
document.addEventListener("DOMContentLoaded", function () {
    // 1. Extract the last part of the URL as identifier
    const pathParts = window.location.pathname.split('/');
    const identifier = pathParts[pathParts.length - 1]; // e.g. "2" or "vincent"

    // 2. Call API using Axios
    axios.get(`/profile/${identifier}`, {
        headers: { "Accept": "application/json" }
    })
    .then(res => {
        const data = res.data;
        document.getElementById('username').textContent = data.name;
        document.getElementById('bio').textContent = data.bio;
        document.getElementById('profile-pic').src = data.image;
    })
    .catch(err => {
        document.getElementById('username').textContent = 'Error loading profile';
        document.getElementById('bio').textContent = err.response?.data?.message || err.message;
        document.getElementById('profile-pic').src = 'https://via.placeholder.com/100';
        
        // If unauthorized → redirect to login
        if (err.response && err.response.status === 403) {
            window.location.href = "/login";
        }
    });
});
</script>

