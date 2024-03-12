// ------------------------------
// GLOBALS
// ------------------------------

const STARS_AMOUNT = 5;

let rating = 0;
let bookmarked = false;
let likedReviews = [];

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

function updateReviewLike(likeButtons, index) {
  let likeTexts = document.getElementsByClassName("review-likes");

  // user deselecting like
  if (likedReviews.includes(index)) {
    likeButtons[index].style.backgroundImage =
      "url(../../../static/images/heart-empty.svg)";
    likeTexts[index].innerText = parseInt(likeTexts[index].innerText) - 1;
    likedReviews.splice(likedReviews.indexOf(index), 1);
    return;
  }

  // user is selecting like
  likeButtons[index].style.backgroundImage =
    "url(../../../static/images/heart.svg)";
  likeTexts[index].innerText = parseInt(likeTexts[index].innerText) + 1;
  likedReviews.push(index);
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
  likeButtons[i].style.backgroundImage =
    "url(../../../static/images/heart-empty.svg)";

  likeButtons[i].onclick = () => {
    updateReviewLike(likeButtons, i);
  };
}
