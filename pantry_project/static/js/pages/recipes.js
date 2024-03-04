import { initButtons } from "../utility/helpers.js";
import { Form } from "../utility/form.js";

// GLOBALS

let selectedCuisines = [];
let selectedCategories = [];
// arrays for passing by reference
let selectedDifficulty = [];
let selectedSortBy = [];

//  INIT

let cuisineBtns = Array.from(document.getElementsByClassName("btn-cuisine"));
let categoryBtns = Array.from(document.getElementsByClassName("btn-category"));
let difficultyBtns = Array.from(
  document.getElementsByClassName("btn-difficulty")
);
let sortByBtns = Array.from(document.getElementsByClassName("btn-sort-by"));

initButtons(cuisineBtns, selectedCuisines, "btn-cuisine-active", true);
initButtons(categoryBtns, selectedCategories, "btn-category-active", true);
initButtons(difficultyBtns, selectedDifficulty, "btn-difficulty-active");
initButtons(sortByBtns, selectedSortBy, "btn-sort-by-active");

// FORM

document.getElementById("search-form").addEventListener("submit", (e) => {
  let hiddenInputs = [
    document.getElementById("difficulty"),
    document.getElementById("cuisines"),
    document.getElementById("categories"),
    document.getElementById("sort"),
  ];

  let values = [
    selectedDifficulty,
    selectedCuisines,
    selectedCategories,
    selectedSortBy,
  ];

  Form.assignHiddenInputs(hiddenInputs, values);
});
