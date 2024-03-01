// simple form validation
// if passwords dont match then show error message
let username = document.getElementById("username");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm-password");

let form = document.getElementById("login-form");
form.addEventListener("submit", (e) => {
  if (username.value === "" || password.value === "") {
    document.getElementById("error-message").innerHTML =
      "Please fill out all fields!";
    document.getElementById("error-message").className = "error-message-active";
    e.preventDefault();
    return false;
  }
});
