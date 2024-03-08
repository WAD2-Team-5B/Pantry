import { imagePreview } from "../utility/helpers.js";
import { Form } from "../utility/form.js";

// ------------------------------
// INIT
// ------------------------------

imagePreview(
  document.getElementById("profile-image"),
  document.getElementById("profile-image-preview")
);

// ------------------------------
// FORM
// ------------------------------

let form = document.getElementById("edit-profile-form");
form.addEventListener("submit", (e) => {
  // validation
  let errorConditions = [
    {
      condition:
        document.getElementById("username").value === "" &&
        document.getElementById("password").value === "" &&
        document.getElementById("profile-image").value === "" &&
        document.getElementById("profile-bio").value === "",
      message: "Please have atleast one change!",
    },
    {
      condition: document.getElementById("profile-image").files.length > 1,
      message: "Please select a single image!",
    },
  ];
  Form.validate(e, errorConditions, document.getElementById("error-message"));
});
