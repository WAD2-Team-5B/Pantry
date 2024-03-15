import { imagePreview } from "../utility/helpers.js";
import { Form } from "../utility/form.js";

// ------------------------------
// GLOBALS
// ------------------------------

const PASSWORD_MIN_LENGTH = 6;

const WARNING =
  "WARNING\n\nAre you sure?\nDeleting an account is permanent and cannot be undone!";
let form = document.getElementById("edit-profile-form");

// ------------------------------
// INIT
// ------------------------------

imagePreview(
  document.getElementById("profile-image"),
  document.getElementById("profile-image-preview")
);

let deleteAccountBtn = document.getElementById("btn-delete-account");
deleteAccountBtn.onclick = () => {
  if (confirm(WARNING)) {
    deleteAccountBtn.value = "true";
    form.submit();
  }
};

// ------------------------------
// FORM
// ------------------------------

form.addEventListener("submit", (e) => {
  let password = document.getElementById("password");

  // validation
  let errorConditions = [
    {
      condition:
        document.getElementById("username").value === "" &&
        password.value === "" &&
        document.getElementById("profile-image").value === "" &&
        document.getElementById("profile-bio").value === "",
      message: "Please have atleast one change!",
    },
    {
      condition: document.getElementById("profile-image").files.length > 1,
      message: "Please select a single image!",
    },
    // if user is changing their password, do the length check
    {
      condition:
        password.value !== "" && password.value.length < PASSWORD_MIN_LENGTH,
      message:
        "Password must be at least " +
        PASSWORD_MIN_LENGTH +
        " characters long!",
    },
  ];
  Form.validate(e, errorConditions, document.getElementById("error-message"));
});
