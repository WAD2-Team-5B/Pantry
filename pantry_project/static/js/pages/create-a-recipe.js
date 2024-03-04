import { initButtons } from "../utility/helpers.js";
import { Form } from "../utility/form.js";

// ------------------------------
// GLOBALS
// ------------------------------

let ingredients = [];
let categories = [];
// arrays for passing by reference
let cuisine = [];
let difficulty = [];

let numSteps = 0;

// ------------------------------
// HELPERS
// ------------------------------

function createIngredient(ingredient) {
  let div = document.createElement("div");
  div.className = "ingredient";
  let deleteBtn = document.createElement("button");
  let text = document.createTextNode(ingredient);

  // unicode for 'x' symbol
  deleteBtn.innerHTML = "&#10006";

  div.appendChild(deleteBtn);
  div.appendChild(text);
  document.getElementById("ingredients-list").appendChild(div);

  deleteBtn.onclick = () => {
    div.remove();
    ingredients.splice(ingredients.indexOf(ingredient), 1);
  };
}

function createStep() {
  numSteps++;

  let stepList = document.getElementById("container-steps");
  let nextItem = document.createElement("li");
  let nextStep = document.createElement("textarea");

  // unicode arrow symbol
  nextItem.style.listStyleImage = "&#8614;";

  nextStep.id = "step-" + numSteps;
  nextStep.className = "step";
  nextStep.placeholder = "step " + numSteps;
  nextStep.rows = 1;

  nextItem.appendChild(nextStep);
  stepList.appendChild(nextItem);

  nextStep.oninput = () => {
    let step = nextStep.id.split("-")[1];

    // resize textarea
    nextStep.style.height = "auto";
    nextStep.style.height = nextStep.scrollHeight + 4 + "px";

    // step was deleted
    if (nextStep.value === "") {
      nextItem.remove();

      // reset steps
      let stepList = document.getElementById("container-steps");
      let steps = stepList.getElementsByTagName("textarea");

      for (let i = 0; i < steps.length; i++) {
        steps[i].id = "step-" + (i + 1);
        steps[i].placeholder = "step " + (i + 1);
      }

      numSteps = steps.length;

      return false;
    }

    // next step already exists
    if (numSteps > step) {
      return false;
    }

    createStep();
  };
}

// ------------------------------
//  INIT
// ------------------------------

let difficultyBtns = Array.from(
  document.getElementsByClassName("btn-difficulty")
);
let cuisineBtns = Array.from(document.getElementsByClassName("btn-cuisine"));
let categoryBtns = Array.from(document.getElementsByClassName("btn-category"));

initButtons(difficultyBtns, difficulty, "btn-difficulty-active");
initButtons(cuisineBtns, cuisine, "btn-cuisine-active");
initButtons(categoryBtns, categories, "btn-category-active", true);

let addIngredientBtn = document.getElementById("btn-add-ingredient");
addIngredientBtn.onclick = () => {
  let ingredientInput = document.getElementById("ingredient");
  let ingredient = ingredientInput.value;
  ingredientInput.value = "";

  // empty or already exists
  if (ingredient === "" || ingredients.includes(ingredient)) {
    return false;
  }

  ingredients.push(ingredient);
  createIngredient(ingredient);

  return false;
};

let fileInput = document.getElementById("recipe-image");
// user selects file
fileInput.onchange = () => {
  let image = fileInput.files[0];
  document.getElementById("recipe-image-preview").src =
    URL.createObjectURL(image);
};

createStep();

// ------------------------------
// FORM
// ------------------------------

let form = document.getElementById("create-a-recipe-form");
form.addEventListener("submit", (e) => {
  // validation
  let errorConditions = [
    ingredients.length === 0,
    cuisine.length === 0,
    difficulty.length === 0,
    // since always defaults to one step
    numSteps <= 1,
    fileInput.files.length === 0 || fileInput.files.length > 1,
    document.getElementById("recipe-name").value === "",
    document.getElementById("recipe-description").value === "",
    document.getElementById("recipe-prep").value === "",
    document.getElementById("recipe-cook").value === "",
  ];
  let errorElement = document.getElementById("error-message");
  let errorMessages = [
    "Please have atleast one ingredient!",
    "Please select a cuisine!",
    "Please select a difficulty!",
    "Please have atleast one step!",
    "Please select a single image!",
    "Please enter a recipe name!",
    "Please enter a recipe description!",
    "Please enter a recipe prep time!",
    "Please enter a recipe cook time!",
    // TODO - validate prep and cook time string format
  ];

  Form.validate(e, errorConditions, errorElement, errorMessages);

  let hiddenInputs = [
    document.getElementById("ingredients"),
    document.getElementById("difficulty"),
    document.getElementById("steps"),
    document.getElementById("cuisines"),
    document.getElementById("categories"),
  ];
  let steps = [];
  Array.from(document.getElementsByClassName("step")).forEach((step) => {
    steps.push(step.value);
  });
  let values = [ingredients, difficulty, steps, cuisine, categories];

  Form.assignHiddenInputs(hiddenInputs, values);
});
