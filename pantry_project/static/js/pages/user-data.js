import { initButtons } from "../utility/helpers.js";
import { PantryAPI } from "../utility/ajax.js";

// ------------------------------
// GLOBALS
// ------------------------------
let dataList = document.getElementById("data-list");
let sortNewest = document.getElementById("btn-newest");
let sortOldest = document.getElementById("btn-oldest");
let currentSelected = sortNewest;

// ------------------------------
// INIT
// ------------------------------

function changeSortBtn(clickedBtn){
  currentSelected.classList.remove('btn-sort-by-active');
  currentSelected = clickedBtn;
  currentSelected.classList.add('btn-sort-by-active');
}

function sortClick (clickedBtn, sortBy){
  if (currentSelected !== clickedBtn) {
    sortDataList(sortBy);
    changeSortBtn(clickedBtn);
  }

}

sortNewest.onclick = function(){
  sortClick(this, "newest");
}

sortOldest.onclick = function() {
  sortClick(this, "oldest");
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
