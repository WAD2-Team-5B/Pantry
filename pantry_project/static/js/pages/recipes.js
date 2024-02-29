// TESTING

const CUISINE_TYPES = [
  "American",
  "Chinese",
  "French",
  "Indian",
  "Italian",
  "Japanese",
  "Mediterranean",
  "Mexican",
  "Thai",
  "Vietnamese",
];

const CATEGORY_TYPES = [
  "Vegan",
  "Vegetarian",
  "Pescatarian",
  "Gluten-Free",
  "Dairy-Free",
  "Nut-Free",
  "Soy-Free",
  "Egg-Free",
];

let selectedCuisines = [];
let selectedCategories = [];
// these two arrays will only contain one element
// but need to be arrays for pass by reference
let selectedDifficulty = [];
let selectedSortBy = [];

function generateBtns(typeName, types, selected) {
  for (let i = 0; i < types.length; i++) {
    let type = types[i];

    let btn = document.createElement("button");
    btn.innerHTML = type;
    btn.id = "btn-" + typeName + "-" + type;
    btn.classList.add("btn-" + typeName);

    btn.onclick = () => {
      if (selected.includes(type)) {
        // user is deselecting
        btn.classList.remove("btn-" + typeName + "-active");
        selected.splice(selected.indexOf(type), 1);
        return false;
      }

      btn.classList.add("btn-" + typeName + "-active");
      selected.push(type);

      return false;
    };

    document.getElementById(typeName + "-list").appendChild(btn);
  }
}

// maybe not the best function name?
function initActiveBtns(name, btns, selected) {
  for (let i = 0; i < btns.length; i++) {
    let btn = btns[i];
    btn.onclick = () => {
      // check if button is already active
      if (btn.classList.contains("btn-" + name + "-active")) {
        btn.classList.remove("btn-" + name + "-active");
        selected.splice(selected.indexOf(btn.value), 1);
        return false;
      }

      // remove active class from all other buttons
      for (let j = 0; j < btns.length; j++) {
        btns[j].classList.remove("btn-" + name + "-active");
        selected.splice(selected.indexOf(btn.value), 1);
      }

      btn.classList.add("btn-" + name + "-active");
      selected.push(btn.value);
      return false;
    };
  }
}

function init() {
  generateBtns("cuisine", CUISINE_TYPES, selectedCuisines);
  generateBtns("category", CATEGORY_TYPES, selectedCategories);

  let difficultyBtns = document.getElementsByClassName("btn-difficulty");
  let sortByBtns = document.getElementsByClassName("btn-sort-by");

  initActiveBtns("difficulty", difficultyBtns, selectedDifficulty);
  initActiveBtns("sort-by", sortByBtns, selectedSortBy);
}

init();
