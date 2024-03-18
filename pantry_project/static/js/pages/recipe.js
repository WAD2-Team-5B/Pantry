// ------------------------------
// GLOBALS
// ------------------------------

import { PantryAPI } from "../utility/ajax.js";

const STARS_AMOUNT = 5;

let rating = 0;

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
  let bookmarked = bookmark.value;
  const data = {"bookmarked": bookmarked};
  PantryAPI.bookmark(data,csrfToken);
  // user deselecting bookmark
  if (bookmarked === "true") {
    bookmark.setAttribute("value", "false");
    bookmark.style.backgroundImage = "url(../../../static/images/bookmark-empty.svg)"; 
    updateSaves(false);
  } else if (bookmarked === "false") {
  // user selecting bookmark
    bookmark.setAttribute("value", "true");
    bookmark.style.backgroundImage = "url(../../../static/images/bookmark.svg)";
    updateSaves(true);
  }
}

function updateSaves(increment) {
  let saves = document.getElementById("saves");
  let value = parseInt(saves.getAttribute("data-save"));

  if (increment) {
    value += 1;
  } else {
    value -= 1;
  }

  saves.setAttribute("data-save", value);

  let ending = (value === 1) ? "" : "s";
  saves.innerHTML = value + " save" + ending;
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
  let bookmarked = bookmark.value
  // set up background image
  if (bookmarked === "true"){
    bookmark.style.backgroundImage = "url(../../../static/images/bookmark.svg)";
  } else if (bookmarked === "false") {
    bookmark.style.backgroundImage = "url(../../../static/images/bookmark-empty.svg)";
  }
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
