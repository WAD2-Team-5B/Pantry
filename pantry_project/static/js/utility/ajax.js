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
        console.log("remove user data success")
      } else if (response == "fail"){
        console.log("remove user data fail")
      }
    });
  }

  static likeReview(data, url, csrfToken) {
    $.post(url, {data:data, csrfmiddlewaretoken: csrfToken}, function (response) {
      if (response == "success") {
        console.log("like review success")
      } else if (response == "fail"){
        console.log("like review fail")
      }
    });
  }

  static bookmark(data, csrfToken){
    $.post("", {data:data, csrfmiddlewaretoken: csrfToken}, function (response) {
      if (response == "success") {
        console.log("bookmark success")
      } else if (response == "fail"){
        console.log("bookmark fail")
      }
    });

  }
  
  static starRecipe() {}
}
