import { initButtons } from "../utility/helpers.js";
import { SPACER } from "../utility/form.js";
import { PantryAPI } from "../utility/ajax.js";

// ------------------------------
// GLOBALS
// ------------------------------

let selectedCuisines = [];
let selectedCategories = [];
// arrays for passing by reference
let selectedDifficulty = [];
let selectedSortBy = [];
let searchQuery = "";

// ------------------------------
// INIT
// ------------------------------

let cuisineBtns = document.getElementsByClassName("btn-cuisine");
let categoryBtns = document.getElementsByClassName("btn-category");
let difficultyBtns = document.getElementsByClassName("btn-difficulty");
let sortByBtns = document.getElementsByClassName("btn-sort-by");

function jquery() {
  const data = {
    request: true,
    search_query: searchQuery,
    selected_cuisines: selectedCuisines.join(SPACER),
    selected_categories: selectedCategories.join(SPACER),
    selected_difficulty: selectedDifficulty.join(SPACER),
    selected_sort: selectedSortBy.join(SPACER),
  };

  PantryAPI.searchRecipes(data);
}

initButtons(cuisineBtns, selectedCuisines, "btn-cuisine-active", true, jquery);
initButtons(categoryBtns, selectedCategories, "btn-category-active", true, jquery);
initButtons(difficultyBtns, selectedDifficulty, "btn-difficulty-active", false, jquery);
initButtons(sortByBtns, selectedSortBy, "btn-sort-by-active", false, jquery);
