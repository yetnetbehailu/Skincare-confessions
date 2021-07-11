/* Sidebar navigation */
$("#sidebarCollapse").click(function () {
    $("#sidebar").toggleClass("active");
     // Display overlay
    $('.overlay').addClass('active');
});
 $('#dismiss-btn, .overlay').on('click', function () {
            // Hide sidebar
            $('#sidebar').removeClass('active');
            // Hide overlay
            $('.overlay').removeClass('active');
        });

/* Listens to change event on is_vegan boolean checkboxfield, marks true when checked */
$("#is_vegan").on("change", function (e) {
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

const tagContainer = document.querySelector(".tag-container");
const input = document.getElementById("tag-input");

var tags = [];

// Creates the div container of the tags,span labels & close icon
function createTag(label) {
    const div = document.createElement("div");
    div.setAttribute("class", "tag");
    const span = document.createElement("span");
    span.innerHTML = label;
    const closeIcon = document.createElement("i");
    closeIcon.setAttribute("class", "fas fa-times");
    closeIcon.setAttribute("data-item", label);
    div.appendChild(span);
    div.appendChild(closeIcon);
    return div;
}

//function to remove tags
function clearTags() {
    document.querySelectorAll(".tag").forEach((tag) => {
        tag.parentElement.removeChild(tag);
    });
}

//function to append the tags to the tag-container
function addTags() {
    clearTags();
    tags.slice().forEach((tag) => {
        newTag = createTag(tag);
        tagContainer.append(newTag);
    });
}

// Keydown event
input.addEventListener("keydown", (e) => {
    // keycode for 'enter' pressed
    if (e.keyCode == 13) {
        // prevent form submit
        e.preventDefault();
        //input value gets split with comma sign,tag created gets pushed into array var
        e.target.value.split(",").forEach((tag) => {
            tags.push(tag);
        });

        addTags();
        input.value = "";
    }
});
//click event listening for specified tagName being pressed
document.addEventListener("click", (e) => {
    if (e.target.tagName === "I") {
        const tagLabel = e.target.getAttribute("data-item");
        const index = tags.indexOf(tagLabel);
        /* removes indexed label using slice method & applying spread operator creating a new single array containing items remained */
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
        addTags();
    }
});
