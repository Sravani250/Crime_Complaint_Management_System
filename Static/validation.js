function validateForm() {
    let title = document.getElementById("title").value;
    let desc = document.getElementById("desc").value;

    if (title.length < 5) {
        alert("Title must be at least 5 characters");
        return false;
    }

    if (desc.length < 10) {
        alert("Description must be at least 10 characters");
        return false;
    }
    return true;
}
