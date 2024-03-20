import { initButtons, imagePreview } from "../utility/helpers.js";
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

let difficultyBtns = document.getElementsByClassName("btn-difficulty");
let cuisineBtns = document.getElementsByClassName("btn-cuisine");
let categoryBtns = document.getElementsByClassName("btn-category");

initButtons(difficultyBtns, difficulty, "btn-difficulty-active", false);
initButtons(cuisineBtns, cuisine, "btn-cuisine-active", false);
initButtons(categoryBtns, categories, "btn-category-active", true);

let addIngredientBtn = document.getElementById("btn-add-ingredient");
addIngredientBtn.onclick = () => {
  let ingredientInput = document.getElementById("ingredient");
  let ingredient = ingredientInput.value.trim();
  ingredientInput.value = "";

  // empty or already exists
  if (ingredient === "" || ingredients.includes(ingredient)) {
    return false;
  }

  ingredients.push(ingredient);
  createIngredient(ingredient);

  return false;
};

imagePreview(
  document.getElementById("recipe-image"),
  document.getElementById("recipe-image-preview")
);

createStep();

// ------------------------------
// FORM
// ------------------------------

let form = document.getElementById("create-a-recipe-form");
form.addEventListener("submit", (e) => {
  // validation
  let errorConditions = [
    {
      condition: ingredients.length === 0,
      message: "Please have atleast one ingredient!",
    },
    { condition: cuisine.length === 0, message: "Please select a cuisine!" },
    {
      condition: difficulty.length === 0,
      message: "Please select a difficulty!",
    },
    { condition: numSteps <= 1, message: "Please have atleast one step!" },
    {
      condition:
        document.getElementById("recipe-image").value === "" ||
        document.getElementById("recipe-image").files.length > 1,
      message: "Please select a single image!",
    },
    {
      condition: document.getElementById("recipe-name").value === "",
      message: "Please enter a recipe name!",
    },
    {
      condition: document.getElementById("recipe-description").value === "",
      message: "Please enter a recipe description!",
    },
    {
      condition: document.getElementById("recipe-prep").value === "",
      message: "Please enter a recipe prep time!",
    },
    {
      condition: document.getElementById("recipe-cook").value === "",
      message: "Please enter a recipe cook time!",
    },
  ];
  Form.validate(e, errorConditions, document.getElementById("error-message"));

  // assign hidden inputs
  let stepElements = document.getElementsByClassName("step");
  let steps = [];
  for (let i = 0; i < stepElements.length - 1; i++) {
    steps.push(stepElements[i].value);
  }

  let hiddenInputs = [
    { input: document.getElementById("ingredients"), value: ingredients },
    { input: document.getElementById("difficulty"), value: difficulty },
    { input: document.getElementById("steps"), value: steps },
    { input: document.getElementById("cuisine"), value: cuisine },
    { input: document.getElementById("categories"), value: categories },
  ];
  Form.assignHiddenInputs(hiddenInputs);
});
