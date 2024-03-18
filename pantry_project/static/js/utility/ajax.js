export class PantryAPI {
  static searchDatabase(data) {
    $.get("", data, function (response) {
      // response is the html of the search results
      $("#search-results").html(response);
    });
  }

  static removeUserData(data, btn, csrfToken) {
    $.post("", {data:data, csrfmiddlewaretoken: csrfToken}, function (response) {
      if (response == "success") {
        btn.parentElement.remove();
        return true;
      } else if (response == "fail"){
        alert("error deleting please try again");
        return false;
      }
    });
  }

  static likeReview(data, url, csrfToken) {
    $.post(url, {data:data, csrfmiddlewaretoken: csrfToken})
  }
  
  static starRecipe() {}
}
