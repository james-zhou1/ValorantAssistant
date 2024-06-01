document.addEventListener('DOMContentLoaded', () => {
    console.log('Website is loaded and ready.');

    document.getElementById('submitBtn').addEventListener('click', () => {
        console.log('Submit button clicked'); // Debugging log

        const username = document.getElementById('username').value;
        const tag = document.getElementById('tag').value;

        console.log('Username:', username); // Debugging log
        console.log('Tag:', tag); // Debugging log

        if (username && tag) {
            // Debugging: Log the URL to be navigated to
            const url = `analytics.html?username=${username}&tag=${tag}`;
            console.log('Navigating to:', url);

            // Navigate to a new page with the analytics message
            window.location.href = url;
        } else {
            alert('Please enter both username and tag.');
        }
    });
});