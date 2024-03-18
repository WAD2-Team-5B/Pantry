import { initButtons } from "../utility/helpers.js";
import { PantryAPI } from "../utility/ajax.js";

// ------------------------------
// GLOBALS
// ------------------------------

let selectedSortBy = [];

// ------------------------------
// INIT
// ------------------------------

let sortByBtns = document.getElementsByClassName("btn-sort-by");

initButtons(sortByBtns, selectedSortBy, "btn-sort-by-active", false);

// delete data
let btnsRemove = document.getElementsByClassName("btn-remove");
for (let i = 0; i < btnsRemove.length; i++) {
  let btn = btnsRemove[i];
  let dataId = btn.value;

  const data = {
    dataId: dataId
  };

  btn.onclick = () => {
    PantryAPI.removeUserData(data, btn, csrfToken);
  };
}
