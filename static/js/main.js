function onCategoryChange() {
    var selectElement = document.getElementById('cat-select');
    var selectedCategory = selectElement.options[selectElement.selectedIndex].value;
    if (selectedCategory) {
        window.location.href = '/galery/' + selectedCategory;
    }
}

window.onload = function() {
    var selectElement = document.getElementById('cat-select');
    selectElement.addEventListener('change', onCategoryChange);
}