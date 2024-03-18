// ------------------------------
// GLOBALS
// ------------------------------

import { PantryAPI } from "../utility/ajax.js";

// ------------------------------
// HELPERS
// ------------------------------

function updateReviewLike(likeButtons, index) {
  let likeTexts = document.getElementsByClassName("review-likes");
  let url = document.getElementById("review-url").getAttribute("data-url");
  let prevLikeStatus = likeButtons[index].getAttribute("data-liked");
  let reviewId = likeButtons[index].value;
  const data = {
    reviewId: reviewId,
  };
  // user deselecting like
  if (prevLikeStatus === "true") {
    likeButtons[index].style.backgroundImage =
      "url(../../../static/images/heart-empty.svg)";
    likeButtons[index].setAttribute("data-liked", "false");
    data["like"] = false;
    likeTexts[index].innerText = parseInt(likeTexts[index].innerText) - 1;
  } else if (prevLikeStatus === "false") {
    // user is selecting like
    likeButtons[index].style.backgroundImage =
      "url(../../../static/images/heart.svg)";
    likeButtons[index].setAttribute("data-liked", "true");
    data["like"] = true;
    likeTexts[index].innerText = parseInt(likeTexts[index].innerText) + 1;
  }

  PantryAPI.likeReview(data, url, csrfToken);
}

// ------------------------------
// INIT
// ------------------------------

// review likes
let likeButtons = document.getElementsByClassName("review-heart");
for (let i = 0; i < likeButtons.length; i++) {
  let liked = likeButtons[i].getAttribute("data-liked");

  if (liked === "true") {
    likeButtons[i].style.backgroundImage =
      "url(../../../static/images/heart.svg)";
  } else if (liked === "false") {
    likeButtons[i].style.backgroundImage =
      "url(../../../static/images/heart-empty.svg)";
  }

  likeButtons[i].onclick = () => {
    updateReviewLike(likeButtons, i);
  };
}

let starBtns = document.getElementsByClassName("star");
let starValue = document.getElementById("star-value");
for (let i = 0; i < starBtns.length; i++) {
  starBtns[i].onclick = () => {
    starValue.value = starBtns[i].value;
  };
}
