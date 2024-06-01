document.addEventListener('DOMContentLoaded', () => {
    console.log('Website is loaded and ready.');

    document.getElementById('submitBtn').addEventListener('click', () => {
        const username = document.getElementById('username').value;
        const tag = document.getElementById('tag').value;

        if (username && tag) {
            // Navigate to a new page with the analytics message
            window.location.href = `analytics.html?username=${username}&tag=${tag}`;
        } else {
            alert('Please enter both username and tag.');
        }
    });
});