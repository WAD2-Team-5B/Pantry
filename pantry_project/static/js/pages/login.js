import { Form } from "../utility/form.js";

// ------------------------------
// GLOBALS
// ------------------------------

let username = document.getElementById("username");
let password = document.getElementById("password");

// ------------------------------
// FORM
// ------------------------------

document.getElementById("login-form").addEventListener("submit", (e) => {
  // validation
  let errorConditions = [
    {
      condition: username.value === "" || password.value === "",
      message: "Please fill out all fields!",
    },
  ];
  Form.validate(e, errorConditions, document.getElementById("error-message"));
});
