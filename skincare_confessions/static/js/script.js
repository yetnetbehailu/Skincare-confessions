/* Sidebar navigation */
$("#sidebarCollapse").click(function () {
    $("#sidebar").toggleClass("active");
});

/* Listens to change event on is_vegan boolean checkboxfield, marks true when checked */
$("#is_vegan").on("change", (e) => {
    this.checkbox = e.target.checked ? "true" : "false";
});

/* Star Rating radiofield*/

$("#rating-0").click(function() {
    $(".fa-star").css("color", "#ffd01f");
    $("#rating-1, #rating-2, #rating-3, #rating-4").css("color", "#cccccc");
});
$("#rating-1").click(function () {
    $(".fa-star").css("color", "#cccccc");
    $("#rating-0, #rating-1").css("color", "#ffd01f");
});
$("#rating-2").click(function () {
    $(".fa-star").css("color", "#cccccc");
    $("#rating-0, #rating-1, #rating-2").css("color", "#ffd01f");
});
$("#rating-3").click(function () {
    $(".fa-star").css("color", "#cccccc");
    $("#rating-0, #rating-1, #rating-2, #rating-3").css("color", "#ffd01f");
});
$("#rating-4").click(function () {
    $(".fa-star").css("color", "#cccccc");
    $("#rating-0, #rating-1, #rating-2, #rating-3, #rating-4").css("color", "#ffd01f");
});
