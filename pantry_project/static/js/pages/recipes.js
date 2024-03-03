import { Init } from "../misc/init.js";

// GLOBALS

let selectedCuisines = [];
let selectedCategories = [];
// arrays for passing by reference
let selectedDifficulty = [];
let selectedSortBy = [];

//  INIT CUISINE / CATEGORY / DIFFICULTY / SORTBY BUTTONS

let cuisineBtns = Array.from(document.getElementsByClassName("btn-cuisine"));
let categoryBtns = Array.from(document.getElementsByClassName("btn-category"));
let difficultyBtns = Array.from(
  document.getElementsByClassName("btn-difficulty")
);
let sortByBtns = Array.from(document.getElementsByClassName("btn-sort-by"));

Init.buttons(cuisineBtns, selectedCuisines, "btn-cuisine-active", true);
Init.buttons(categoryBtns, selectedCategories, "btn-category-active", true);
Init.buttons(difficultyBtns, selectedDifficulty, "btn-difficulty-active");
Init.buttons(sortByBtns, selectedSortBy, "btn-sort-by-active");
