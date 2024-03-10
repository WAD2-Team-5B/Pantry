import { initButtons } from "../utility/helpers.js";

// ------------------------------
// GLOBALS
// ------------------------------

let selectedSortBy = [];

// ------------------------------
// INIT
// ------------------------------

let sortByBtns = document.getElementsByClassName("btn-sort-by");

initButtons(sortByBtns, selectedSortBy, "btn-sort-by-active");

// delete data
let btnsRemove = document.getElementsByClassName("btn-remove");
for (let i = 0; i < btnsRemove.length; i++) {
  let btn = btnsRemove[i];
  btn.onclick = () => {
    // TODO - REQUEST TO REMOVE IT FROM DB
    // IF SUCCESSFULL
    btn.parentElement.remove();
  };
}
