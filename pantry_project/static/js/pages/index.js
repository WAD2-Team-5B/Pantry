// TESTING
const NUMBER_OF_RECIPES = 10;

function createRecipeCard(name, picture, href) {
  let card = document.createElement("a");
  let heading = document.createElement("h4");
  let img = document.createElement("img");

  heading.innerHTML = name;
  img.src = picture;

  card.appendChild(heading);
  card.appendChild(img);

  card.href = href;
  card.className = "recipe-card";

  return card;
}

function loadRecipes(containerName) {
  div = document.getElementById(containerName);
  for (let i = 0; i < NUMBER_OF_RECIPES; i++) {
    div.appendChild(createRecipeCard("Test", "", ""));
  }
}

console.log("loading highest-rated-recipes");
loadRecipes("highest-rated-recipes");

console.log("loading newest-recipes");
loadRecipes("newest-recipes");

// headings
document.getElementById("heading-highest-rated-recipes").innerHTML =
  NUMBER_OF_RECIPES + " Highest Rated Recipes";
document.getElementById("heading-newest-recipes").innerHTML =
  NUMBER_OF_RECIPES + " Newest Recipes";
