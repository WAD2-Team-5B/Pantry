import { initButtons } from "../utility/helpers.js";
import { PantryAPI } from "../utility/ajax.js";

// ------------------------------
// GLOBALS
// ------------------------------

let selectedSortBy = [];

// ------------------------------
// INIT
// ------------------------------

// sorting
let dataList = document.getElementById("data-list");
let sortNewest = document.getElementById("btn-newest");
let sortOldest = document.getElementById("btn-oldest")

sortNewest.onclick = () => {
  sortDataList('newest');
};

sortOldest.onclick = () => {
  sortDataList('oldest');
};

function sortDataList(order) {
  let items = Array.from(dataList.children);
  items.sort((a, b) => {
    let dateA = new Date(a.dataset.date);
    let dateB = new Date(b.dataset.date);
    if (order === 'newest') {
      return dateB - dateA; // Sort in descending order (newest first)
    } else {
      return dateA - dateB; // Sort in ascending order (oldest first)
    }
  });
  // Clear the current list
  dataList.innerHTML = '';
  // Append sorted items back to the list
  items.forEach(item => dataList.appendChild(item));
}

initButtons(
  [sortNewest, sortOldest],
  selectedSortBy, // Initially no button selected
  "btn-sort-by-active", 
  false, // Allow only single selection
  () => { // Callback function to handle sorting
    // Sort only when a button is selected, not deselected
    if (selectedSortBy.length > 0) {
      if (selectedSortBy[0] === "newest") {
        sortDataList('newest');
      } else if (selectedSortBy[0] === "oldest") {
        sortDataList('oldest');
      }
    }
  }
);


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
