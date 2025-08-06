document.getElementById("updateForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form); // automatically sets multipart/form-data

    try {
        const response = await fetch("/profile/update", {
            method: "POST",
            body: formData,
            credentials: "include" 
        });

        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        const data = await response.json().catch(() => ({}));

        if (response.ok) {
            alert("Profile updated successfully!");
        } else {
            alert(data.error || "Error updating profile");
        }
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Something went wrong. Please try again.");
    }
});

