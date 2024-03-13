export class PantryAPI {
  static searchRecipes(data) {
    $.get("", data, function (response) {
      // response is the html of the search results
      $("#search-results").html(response);
    });
  }

  static bookmark() {}

  static like() {}
}

// $(document).ready(function () {
//   $("#bookmark").click(function () {
//     var recipeIdVar;
//     recipeIdVar = $(this).attr("data-recipeid");

//     $.get("/rango/save_recipe/", { recipe_id: recipeIdVar });
//   });
// });

// $(document).ready(function () {
//   $("#review-heart").click(function () {
//     var reviewIdVar;
//     reviewIdVar = $(this).attr("data-reviewid");

//     $.get("/rango/like_review/", { review_id: reviewIdVar });
//   });
// });
