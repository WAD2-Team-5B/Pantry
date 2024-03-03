import { Init } from "../misc/init.js";
import { Form } from "../misc/form.js";

// GLOBALS

let ingredients = [];
let categories = [];
// arrays for passing by reference
let cuisine = [];
let difficulty = [];

let numSteps = 0;

//  INIT CUISINE / CATEGORY / DIFFICULTY BUTTONS

let difficultyBtns = Array.from(
  document.getElementsByClassName("btn-difficulty")
);
let cuisineBtns = Array.from(document.getElementsByClassName("btn-cuisine"));
let categoryBtns = Array.from(document.getElementsByClassName("btn-category"));

Init.buttons(difficultyBtns, difficulty, "btn-difficulty-active");
Init.buttons(cuisineBtns, cuisine, "btn-cuisine-active");
Init.buttons(categoryBtns, categories, "btn-category-active", true);

// HELPER FUNCTIONS

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
    selectedIngredients.splice(selectedIngredients.indexOf(ingredient), 1);
  };
}

// TODO - implement validation of image
function validateImage() {}

function resetStepIds() {
  let stepList = document.getElementById("container-steps");
  let steps = stepList.getElementsByTagName("textarea");

  for (let i = 0; i < steps.length; i++) {
    steps[i].id = "step-" + (i + 1);
    steps[i].placeholder = "step " + (i + 1);
  }

  numSteps = steps.length;
}

function createTextArea() {
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
      resetStepIds();
      return false;
    }

    // next step already exists
    if (numSteps > step) {
      return false;
    }

    createTextArea();
  };
}

// INIT

// ingredients
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

// image
let fileInput = document.getElementById("recipe-image");
// user selects file
fileInput.onchange = () => {
  validateImage();

  let image = fileInput.files[0];
  document.getElementById("recipe-image-preview").src =
    URL.createObjectURL(image);
};

// steps
createTextArea();
