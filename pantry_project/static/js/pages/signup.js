// simple form validation
// if passwords dont match then show error message
let username = document.getElementById("username");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm-password");

document.getElementById("signup-form").addEventListener("submit", (e) => {
  if (
    username.value === "" ||
    password.value === "" ||
    confirmPassword.value === ""
  ) {
    document.getElementById("error-message").innerHTML =
      "Please fill out all fields!";
    document.getElementById("error-message").className = "error-message-active";
    e.preventDefault();
    return false;
  }

  if (password.value !== confirmPassword.value) {
    document.getElementById("error-message").innerHTML =
      "Please ensure both passwords match!";
    document.getElementById("error-message").className = "error-message-active";
    e.preventDefault();
    return false;
  }
});
