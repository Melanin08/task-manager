// Toggle Dark Mode
function toggleTheme() {
    let body = document.body;

    if (body.style.backgroundColor === "black") {
        body.style.backgroundColor = "white";
        body.style.color = "black";
    } else {
        body.style.backgroundColor = "black";
        body.style.color = "white";
    }
}

/* Form Validation */
let form = document.querySelector("form");

form.addEventListener("submit", function(event) {
event.preventDefault();

let name = document.querySelector('input[type="text"]').value;
let email = document.querySelector('input[type="email"]').value;

if (name === "" || email === "") {
    alert("Please fill in all fields!");
} else {
    alert("Thank you, " + name + "! Message sent.");
    form.reset();
}

});


// Click Counter
let counter = 0;

function countClicks() {
    counter++;
    document.getElementById("clickCount").textContent = "Clicks: " + counter;
}
