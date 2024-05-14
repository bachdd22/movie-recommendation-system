const arrows2 = document.querySelectorAll(".left-arrow")
const arrows = document.querySelectorAll(".arrow");
const movieLists = document.querySelectorAll(".movie-list");

arrows.forEach((arrow, i) => {
  const itemNumber = movieLists[i].querySelectorAll("img").length;
  let clickCounter = 0;
  arrow.addEventListener("click", () => {
    const ratio = Math.floor(window.innerWidth / 200);
    clickCounter++;
    if (itemNumber - (10 + clickCounter) + (10 - ratio) >= 0) {
      movieLists[i].style.transform = `translateX(${
        movieLists[i].computedStyleMap().get("transform")[0].x.value - 300
      }px)`;
    } else {
      movieLists[i].style.transform = "translateX(0)";
      clickCounter = 0;
    }
  });

  console.log(Math.floor(window.innerWidth / 200));
});

arrows2.forEach((arrow, i) => {
  const itemNumber = movieLists[i].querySelectorAll("img").length;
  let clickCounter = 0;
  arrow.addEventListener("click", () => {
    const ratio = Math.floor(window.innerWidth / 200);
    clickCounter++;
    if (itemNumber - (4 + clickCounter) + (4 - ratio) >= 0) {
      movieLists[i].style.transform = `translateX(${
        movieLists[i].computedStyleMap().get("transform")[0].x.value + 300
      }px)`;
    } else {
      movieLists[i].style.transform = "translateX(0)";
      clickCounter = 0;
    }
  });

  console.log(Math.floor(window.innerWidth / 200));
});

//TOGGLE

const ball = document.querySelector(".toggle-ball");
const items = document.querySelectorAll(
  ".container,.movie-list-title,.navbar-container,.sidebar,.left-menu-icon,.toggle"
);

ball.addEventListener("click", () => {
  items.forEach((item) => {
    item.classList.toggle("active");
  });
  ball.classList.toggle("active");
});


$(document).ready(function() {
  $("#newListBtn").click(function() {
      $("#newListForm").show();
  });

  $("#closeBtn").click(function() {
      $("#newListForm").hide();
  });

  $("#createForm").submit(function(event) {
      event.preventDefault();
      var listName = $("#listName").val();
      $.ajax({
          type: "POST",
          url: "/create_list",
          data: JSON.stringify({ name: listName }),
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          success: function(response) {
              // Handle success response
              console.log("List created successfully");
              // Optionally, you can redirect the user to another page or update the UI
          },
          error: function(xhr, status, error) {
              // Handle error
              console.error("Error creating list:", error);
          }
      });
  });

});
