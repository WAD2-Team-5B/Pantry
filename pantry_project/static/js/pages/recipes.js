// GLOBALS

let selectedCuisines = [];
let selectedCategories = [];
let selectedDifficulty = "";
let selectedSortBy = "";

//  INIT CUISINE AND CATEGORY BUTTONS

function initCuisineBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-cuisine"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      let cuisine = btn.value;
      // user is deselecting
      if (selectedCuisines.includes(cuisine)) {
        btn.classList.remove("btn-cuisine-active");
        selectedCuisines.splice(selectedCuisines.indexOf(cuisine), 1);

        // TESTING - this stops form from submitting
        return false;
      }

      // user is selecting
      btn.classList.add("btn-cuisine-active");
      selectedCuisines.push(cuisine);

      // TESTING - this stops form from submitting
      return false;
    };
  });
}

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

// INIT DIFFICULTY AND SORT BY BUTTONS

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

function initSortByBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-sort-by"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      let sortBy = btn.value;
      // user is deselecting
      if (selectedSortBy === sortBy) {
        btn.classList.remove("btn-sort-by-active");
        selectedSortBy = "";

        // TESTING - this stops form from submitting
        return false;
      }

      // user is selecting another sort by
      btns.forEach((btn) => {
        btn.classList.remove("btn-sort-by-active");
      });
      btn.classList.add("btn-sort-by-active");
      selectedSortBy = sortBy;

      // TESTING - this stops form from submitting
      return false;
    };
  });
}

// STARTUP

initCuisineBtns();
initCategoryBtns();
initDifficultyBtns();
initSortByBtns();
