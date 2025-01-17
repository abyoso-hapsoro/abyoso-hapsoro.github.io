document.addEventListener("DOMContentLoaded", function() {
    // Ensure all hidden tab contents are indexed
    document.querySelectorAll('.tabcontent').forEach(tab => {
        tab.style.display = "block";
    });
});