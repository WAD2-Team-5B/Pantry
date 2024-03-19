import { PantryAPI } from "../utility/ajax.js";

// ------------------------------
// GLOBALS
// ------------------------------

let searchQuery = "";

// ------------------------------
// INIT
// ------------------------------

function jqueryusers() {
    const data = {
        request: true,
        search_query: searchQuery,
    };

    PantryAPI.searchDatabase(data);
}


let searchBar = document.getElementById("search");
searchBar.oninput = () => {
    searchQuery = searchBar.value;

    jqueryusers();
};