// TESTING
const NUMBER_OF_RECIPES = 10;

function createRecipeCard(name, picture) {
  let card = document.createElement("div");
  let heading = document.createElement("h4");
  let img = document.createElement("img");

  heading.innerHTML = name;
  img.src = picture;

  card.appendChild(heading);
  card.appendChild(img);

  card.className = "recipe-card";

  return card;
}

function loadRecipes(containerName) {
  div = document.getElementById(containerName);
  for (let i = 0; i < NUMBER_OF_RECIPES; i++) {
    div.appendChild(createRecipeCard("Test", ""));
  }
}

loadRecipes("highest-rated-recipes");
loadRecipes("newest-recipes");
