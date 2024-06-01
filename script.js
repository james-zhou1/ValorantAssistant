document.addEventListener('DOMContentLoaded', () => {
    console.log('Website is loaded and ready.');

    // Example: Log input values on change
    document.getElementById('username').addEventListener('input', (event) => {
        console.log('Username:', event.target.value);
    });

    document.getElementById('tag').addEventListener('input', (event) => {
        console.log('Tag:', event.target.value);
    });
});