document.addEventListener('DOMContentLoaded', () => {
    console.log('Website is loaded and ready.');

    document.getElementById('submitBtn').addEventListener('click', () => {
        const username = document.getElementById('username').value;
        const tag = document.getElementById('tag').value;

        if (username && tag) {
            // Update content dynamically instead of navigating
            document.getElementById('analyticsMessage').textContent = `Here are the analytics for ${username} ${tag}`;
            document.getElementById('content').style.display = 'block'; // Show the analytics content
        } else {
            alert('Please enter both username and tag.');
        }
    });
});