import { Form } from "../misc/form.js";

// GLOBALS

let username = document.getElementById("username");
let password = document.getElementById("password");

// EVENT HANDLERS

// 'submit' event listen for the login form to validate before submission
document.getElementById("login-form").addEventListener("submit", (e) => {
  // conditions:
  // 1. no field is empty
  let errorConditions = [username.value === "" || password.value === ""];

  let errorElement = document.getElementById("error-message");

  let errorMessages = ["Please fill out all fields!"];

  Form.validate(e, errorConditions, errorElement, errorMessages);
});
