function onCategoryChange() {
  var selectElement = document.getElementById("cat-select");
  var selectedCategory =
    selectElement.options[selectElement.selectedIndex].value;
  if (selectedCategory) {
    window.location.href = "/galery/" + selectedCategory;
  }
}

window.onload = function () {
  var selectElement = document.getElementById("cat-select");
  selectElement.addEventListener("change", onCategoryChange);
};

// on keyUp event
function searchPigeon() {
  if (event.keyCode === 13) {
    var searchElement = document.getElementById("search");
    var searchValue = searchElement.value.toLowerCase();
    if (searchValue && searchValue.length > 1) {
      window.location.href = "/galery/search-pigeon/" + searchValue;
    } else {
      document.getElementById("minCharMessage").style.display = "block";
    }
  }
}
