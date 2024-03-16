// ------------------------------
// GLOBALS
// ------------------------------

import { PantryAPI } from "../utility/ajax.js";

const STARS_AMOUNT = 5;

let rating = 0;
let bookmarked = false;

// ------------------------------
// HELPERS
// ------------------------------

function updateStars(index) {
  let stars = document.getElementsByClassName("star");

  rating = index;

  for (let i = 0; i < STARS_AMOUNT; i++) {
    if (i < index) {
      stars[i].style.backgroundImage = "url(../../../static/images/star.svg)";
    } else {
      stars[i].style.backgroundImage =
        "url(../../../static/images/star-empty.svg)";
    }
  }
}

function updateBookmark() {
  let bookmark = document.getElementById("bookmark");

  // user deselecting bookmark
  if (bookmarked) {
    bookmarked = false;
    bookmark.style.backgroundImage =
      "url(../../../static/images/bookmark-empty.svg)";
    return;
  }

  // user selecting bookmark
  bookmarked = true;
  bookmark.style.backgroundImage = "url(../../../static/images/bookmark.svg)";
}

function updateReviewLike(likeButtons, index, like) {
  let likeTexts = document.getElementsByClassName("review-likes");
  let url = document.getElementById("review-url").getAttribute("data-url");
  let prevLikeStatus = likeButtons[index].getAttribute("data-liked");
  let reviewId = likeButtons[index].value;
  const data = {
    reviewId: reviewId
  }
  // user deselecting like
  if (prevLikeStatus === "true") {
    likeButtons[index].style.backgroundImage = "url(../../../static/images/heart-empty.svg)";
    likeButtons[index].setAttribute("data-liked","false")
    data["like"] = false
    likeTexts[index].innerText = parseInt(likeTexts[index].innerText) - 1;
  } else if (prevLikeStatus === "false"){
    // user is selecting like
    likeButtons[index].style.backgroundImage = "url(../../../static/images/heart.svg)";
    likeButtons[index].setAttribute("data-liked","true")
    data["like"] = true
    likeTexts[index].innerText = parseInt(likeTexts[index].innerText) + 1;
  } 

  PantryAPI.likeReview(data, url, csrfToken);

 
}

// ------------------------------
// INIT
// ------------------------------

// stars
let stars = document.getElementById("stars");
// if null then user not logged in
if (stars) {
  for (let i = 0; i < STARS_AMOUNT; i++) {
    let star = document.createElement("button");

    star.id = "star-" + (i + 1);
    star.style.backgroundImage = "url(../../../static/images/star-empty.svg)";
    star.className = "star";

    star.onclick = () => {
      updateStars(i + 1);
    };

    stars.appendChild(star);
  }
}

// bookmark
let bookmark = document.getElementById("bookmark");
// if null then user not logged in
if (bookmark) {
  bookmark.style.backgroundImage =
    "url(../../../static/images/bookmark-empty.svg)";
  bookmark.onclick = () => {
    updateBookmark();
  };
}

// review likes
let likeButtons = document.getElementsByClassName("review-heart");
for (let i = 0; i < likeButtons.length; i++) {
  let liked = likeButtons[i].getAttribute("data-liked");

  if (liked === "true"){
    likeButtons[i].style.backgroundImage = "url(../../../static/images/heart.svg)";
  } else if (liked === "false"){
    likeButtons[i].style.backgroundImage ="url(../../../static/images/heart-empty.svg)";
  } 
 
  likeButtons[i].onclick = () => {
    updateReviewLike(likeButtons, i);
  };
}
