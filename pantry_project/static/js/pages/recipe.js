// GLOBALS

const STARS_AMOUNT = 5;

let rating = 0;
let bookmarked = false;

// STAR RATING

function updateStars(index) {
  let stars = document.getElementsByClassName("star");

  rating = index;

  for (let i = 0; i < STARS_AMOUNT; i++) {
    if (i < index) {
      stars[i].style.backgroundImage = "url(../../static/images/star.svg)";
    } else {
      stars[i].style.backgroundImage =
        "url(../../static/images/star-empty.svg)";
    }
  }
}

function initStars() {
  let container = document.getElementById("stars");

  for (let i = 0; i < STARS_AMOUNT; i++) {
    let star = document.createElement("button");

    star.id = "star-" + (i + 1);
    star.style.backgroundImage = "url(../../static/images/star-empty.svg)";
    star.className = "star";

    star.onclick = () => {
      updateStars(i + 1);
    };

    container.appendChild(star);
  }
}

// BOOKMARK

function updateBookmark() {
  let bookmark = document.getElementById("bookmark");

  // user deselecting bookmark
  if (bookmarked) {
    bookmarked = false;
    bookmark.style.backgroundImage =
      "url(../../static/images/bookmark-empty.svg)";
    return;
  }

  // user selecting bookmark
  bookmarked = true;
  bookmark.style.backgroundImage = "url(../../static/images/bookmark.svg)";
}

function initBookmark() {
  let bookmark = document.getElementById("bookmark");

  bookmark.style.backgroundImage =
    "url(../../static/images/bookmark-empty.svg)";

  bookmark.onclick = () => {
    updateBookmark();
  };
}

initStars();
initBookmark();
