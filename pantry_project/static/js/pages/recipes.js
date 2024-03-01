// GLOBALS

let selectedCuisines = [];
let selectedCategories = [];
let selectedDifficulty = "";
let selectedSortBy = "";

//  INIT CUISINE AND CATEGORY BUTTONS

function initCuisineBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-cuisine"));
  btns.forEach((btn) => {
    let cuisine = btn.value;

    btn.onclick = () => {
      // user is deselecting
      if (selectedCuisines.includes(cuisine)) {
        btn.classList.remove("btn-cuisine-active");
        selectedCuisines.splice(selectedCuisines.indexOf(cuisine), 1);

        // dont submit form
        return false;
      }

      // user is selecting
      btn.classList.add("btn-cuisine-active");
      selectedCuisines.push(cuisine);

      // dont submit form
      return false;
    };
  });
}

function initCategoryBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-category"));
  btns.forEach((btn) => {
    let category = btn.value;

    btn.onclick = () => {
      // user is deselecting
      if (selectedCategories.includes(category)) {
        btn.classList.remove("btn-category-active");
        selectedCategories.splice(selectedCategories.indexOf(category), 1);

        // dont submit form
        return false;
      }

      // user is selecting
      btn.classList.add("btn-category-active");
      selectedCategories.push(category);

      // dont submit form
      return false;
    };
  });
}

// INIT DIFFICULTY AND SORT BY BUTTONS

function initDifficultyBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-difficulty"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      // user is deselecting
      if (selectedDifficulty === btn.value) {
        btn.classList.remove("btn-difficulty-active");
        selectedDifficulty = "";

        // dont submit form
        return false;
      }

      // user is selecting another difficulty
      btns.forEach((btn) => {
        btn.classList.remove("btn-difficulty-active");
      });
      btn.classList.add("btn-difficulty-active");
      selectedDifficulty = btn.value;

      // dont submit form
      return false;
    };
  });
}

function initSortByBtns() {
  let btns = Array.from(document.getElementsByClassName("btn-sort-by"));
  btns.forEach((btn) => {
    btn.onclick = () => {
      // user is deselecting
      if (selectedSortBy === btn.value) {
        btn.classList.remove("btn-sort-by-active");
        selectedSortBy = "";

        // dont submit form
        return false;
      }

      // user is selecting another sort by
      btns.forEach((btn) => {
        btn.classList.remove("btn-sort-by-active");
      });
      btn.classList.add("btn-sort-by-active");
      selectedSortBy = btn.value;

      // dont submit form
      return false;
    };
  });
}

// STARTUP

initCuisineBtns();
initCategoryBtns();
initDifficultyBtns();
initSortByBtns();
