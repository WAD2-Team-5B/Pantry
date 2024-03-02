// GLOBALS

let rating = 0;

// STAR RATING

function initStars() {
  let container = document.getElementById("stars");

  // 5 stars
  for (let i = 0; i < 5; i++) {
    let star = document.createElement("button");

    star.id = "star-" + (i + 1);
    star.style.backgroundImage = "url(../../static/images/star-empty.svg)";
    star.className = "star";

    container.appendChild(star);
  }
}

// BOOKMARK

function initBookmark() {
  let bookmark = document.getElementById("bookmark");
  bookmark.style.backgroundImage =
    "url(../../static/images/bookmark-empty.svg)";
}

initStars();
initBookmark();
