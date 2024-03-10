import { initButtons } from "../utility/helpers.js";
import { Form } from "../utility/form.js";

// ------------------------------
// GLOBALS
// ------------------------------

let selectedCuisines = [];
let selectedCategories = [];
// arrays for passing by reference
let selectedDifficulty = [];
let selectedSortBy = [];

// ------------------------------
// INIT
// ------------------------------

let cuisineBtns = document.getElementsByClassName("btn-cuisine");
let categoryBtns = document.getElementsByClassName("btn-category");
let difficultyBtns = document.getElementsByClassName("btn-difficulty");
let sortByBtns = document.getElementsByClassName("btn-sort-by");

initButtons(cuisineBtns, selectedCuisines, "btn-cuisine-active", true);
initButtons(categoryBtns, selectedCategories, "btn-category-active", true);
initButtons(difficultyBtns, selectedDifficulty, "btn-difficulty-active");
initButtons(sortByBtns, selectedSortBy, "btn-sort-by-active");

// ------------------------------
// FORM
// ------------------------------

document.getElementById("search-form").addEventListener("submit", (e) => {
  let hiddenInputs = [
    { input: document.getElementById("difficulty"), value: selectedDifficulty },
    { input: document.getElementById("cuisines"), value: selectedCuisines },
    { input: document.getElementById("categories"), value: selectedCategories },
    { input: document.getElementById("sort"), value: selectedSortBy },
  ];
  Form.assignHiddenInputs(hiddenInputs, values);
});
