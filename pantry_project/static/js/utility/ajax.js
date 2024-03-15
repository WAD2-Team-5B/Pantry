export class PantryAPI {
  static searchDatabase(data) {
    $.get("", data, function (response) {
      // response is the html of the search results
      $("#search-results").html(response);
    });
  }

  static removeUserData(data, btn) {
    $.get("", data, function (response) {
      if (response === "success") {
        btn.parentElement.remove();
        return true;
      }
      alert("error deleting please try again");
      return false;
    });
  }

  static likeReview() {}

  static starRecipe() {}
}
