// GLOBALS

let selectedDifficulty = "";
let selectedIngredients = [];
let selectedCuisine = "";
let selectedCategories = [];
let steps = [];

let numSteps = 0;

// INIT DIFFICULTY

// TODO - REUSE SAME FUNCTION FROM 'recipes'
function initDifficultyBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-difficulty"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      let difficulty = btn.value;
      // user is deselecting
      if (selectedDifficulty === difficulty) {
        btn.classList.remove("btn-difficulty-active");
        selectedDifficulty = "";

        // TESTING - this stops form from submitting
        return false;
      }

      // user is selecting another difficulty
      btns.forEach((btn) => {
        btn.classList.remove("btn-difficulty-active");
      });
      btn.classList.add("btn-difficulty-active");
      selectedDifficulty = difficulty;

      // TESTING - this stops form from submitting
      return false;
    };
  });
}

// INIT INGREDIENTS

function initIngredients() {
  let addIngredientBtn = document.getElementById("btn-add-ingredient");
  let ingredientInput = document.getElementById("ingredient");

  addIngredientBtn.onclick = () => {
    let ingredient = ingredientInput.value;
    ingredientInput.value = "";

    // empty or already exists
    if (ingredient === "" || selectedIngredients.includes(ingredient)) {
      return false;
    }

    selectedIngredients.push(ingredient);

    let div = document.createElement("div");
    div.className = "ingredient";
    let deleteBtn = document.createElement("button");
    let text = document.createTextNode(ingredient);

    //   unicode for 'x' symbol
    deleteBtn.innerHTML = "&#10006";

    div.appendChild(deleteBtn);
    div.appendChild(text);
    document.getElementById("ingredients-list").appendChild(div);

    deleteBtn.onclick = () => {
      div.remove();
      selectedIngredients.splice(selectedIngredients.indexOf(ingredient), 1);
    };

    return false;
  };
}

// INIT CUISINES / CATEGORIES

// TODO - REUSE SAME FUNCTION FROM 'recipes'
function initCuisineBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-cuisine"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      let cuisine = btn.value;
      // user is deselecting
      if (selectedCuisine === cuisine) {
        btn.classList.remove("btn-cuisine-active");
        selectedCuisine = "";

        // TESTING - this stops form from submitting
        return false;
      }

      // user is selecting
      btns.forEach((btn) => {
        btn.classList.remove("btn-cuisine-active");
      });
      btn.classList.add("btn-cuisine-active");
      selectedCuisine = cuisine;

      // TESTING - this stops form from submitting
      return false;
    };
  });
}

// TODO - REUSE SAME FUNCTION FROM 'recipes'
function initCategoryBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-category"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      let category = btn.value;
      // user is deselecting
      if (selectedCategories.includes(category)) {
        btn.classList.remove("btn-category-active");
        selectedCategories.splice(selectedCategories.indexOf(category), 1);

        // TESTING - this stops form from submitting
        return false;
      }

      // user is selecting
      btn.classList.add("btn-category-active");
      selectedCategories.push(category);

      // TESTING - this stops form from submitting
      return false;
    };
  });
}

// HANDLE IMAGE UPLOAD

// TODO
function validateImage() {}

function initImageUpload() {
  let fileInput = document.getElementById("recipe-image");

  // user selects file
  fileInput.onchange = () => {
    validateImage();

    let image = fileInput.files[0];
    document.getElementById("recipe-image-preview").src =
      URL.createObjectURL(image);
  };
}

// HANDLE STEPS

function resetIDs() {
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
      resetIDs();
      return false;
    }

    // next step already exists
    if (numSteps > step) {
      return false;
    }

    createTextArea();
  };
}

initDifficultyBtns();
initIngredients();
initCuisineBtns();
initCategoryBtns();
initImageUpload();
createTextArea();
