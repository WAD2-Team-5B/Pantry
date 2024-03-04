import { Form } from "../utility/form.js";

// GLOBALS

const PASSWORD_MIN_LENGTH = 6;

let username = document.getElementById("username");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm-password");

// EVENT HANDLERS

// 'submit' event listen for the signup form to validate before submission
document.getElementById("signup-form").addEventListener("submit", (e) => {
  // conditions:
  // 1. no field is empty
  // 2. passwords match
  // 3. password is at least 'PASSWORD_MIN_LENGTH' characters long
  let errorConditions = [
    username.value === "" ||
      password.value === "" ||
      confirmPassword.value === "",
    password.value !== confirmPassword.value,
    password.value.length < PASSWORD_MIN_LENGTH,
  ];
  let errorElement = document.getElementById("error-message");
  let errorMessages = [
    "Please fill out all fields!",
    "Please ensure both passwords match!",
    "Password must be at least " + PASSWORD_MIN_LENGTH + " characters long!",
  ];

  Form.validate(e, errorConditions, errorElement, errorMessages);
});
