import { Form } from "../utility/form.js";

// ------------------------------
// GLOBALS
// ------------------------------

const PASSWORD_MIN_LENGTH = 6;

let username = document.getElementById("username");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm-password");

// ------------------------------
// FORM
// ------------------------------

document.getElementById("signup-form").addEventListener("submit", (e) => {
  // validation
  let errorConditions = [
    {
      condition:
        username.value === "" ||
        password.value === "" ||
        confirmPassword.value === "",
      message: "Please fill out all fields!",
    },
    {
      condition: password.value !== confirmPassword.value,
      message: "Please ensure both passwords match!",
    },
    {
      condition: password.value.length < PASSWORD_MIN_LENGTH,
      message:
        "Password must be at least " +
        PASSWORD_MIN_LENGTH +
        " characters long!",
    },
  ];
  Form.validate(e, errorConditions, document.getElementById("error-message"));
});
