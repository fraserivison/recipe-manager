document.addEventListener("DOMContentLoaded", function() {
    const descriptionField = document.querySelector("textarea[name='description']");
    const messageDiv = document.getElementById("message");

    const maxChars = 45;

    descriptionField.addEventListener("input", function() {
        const currentLength = descriptionField.value.length;

        if (currentLength > maxChars) {
            messageDiv.style.display = "block";
            descriptionField.value = descriptionField.value.substring(0, maxChars);
        } else {
            messageDiv.style.display = "none";
        }
    });
});

