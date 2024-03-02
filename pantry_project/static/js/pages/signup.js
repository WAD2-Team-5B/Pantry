// simple form validation
// if passwords dont match then show error message
let username = document.getElementById("username");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm-password");

const PASSWORD_MIN_LENGTH = 6;

document.getElementById("signup-form").addEventListener("submit", (e) => {
  // empty field
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

  // password dont match
  if (password.value !== confirmPassword.value) {
    document.getElementById("error-message").innerHTML =
      "Please ensure both passwords match!";
    document.getElementById("error-message").className = "error-message-active";
    e.preventDefault();
    return false;
  }

  // password too short
  if (password.value.length < PASSWORD_MIN_LENGTH) {
    document.getElementById("error-message").innerHTML =
      "Password must be at least 6 characters long!";
    document.getElementById("error-message").className = "error-message-active";
    e.preventDefault();
    return false;
  }
});
