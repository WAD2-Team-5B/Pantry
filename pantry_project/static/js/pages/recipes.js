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
        selected = selected.filter((c) => c !== type);
        return false;
      }

      btn.classList.add("btn-" + typeName + "-active");
      selected.push(type);

      return false;
    };

    document.getElementById(typeName + "-list").appendChild(btn);
  }
}

function init() {
  generateBtns("cuisine", CUISINE_TYPES, selectedCuisines);
  generateBtns("category", CATEGORY_TYPES, selectedCategories);
}

init();
