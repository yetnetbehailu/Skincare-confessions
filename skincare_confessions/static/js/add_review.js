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

//Tagbtn click event
document.getElementById("tagbtn").addEventListener("click", (e) => {
    /*input value gets split with comma sign,tag created gets pushed into array var */
    if (e.target.id == "tagbtn") {
        e.preventDefault();
        input.value.split(",").forEach((tag) => {
         if (tag){
                tags.push(tag);
            }
        });

        addTags();
        input.value = "";
        let hiddenField = document.getElementById("hiddenInput");
        hiddenField.value = tags;
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

const reviewForm = document.getElementById("reviewForm");
reviewForm.addEventListener("submit", (e) => {
    //If a form control (e.g. submit button) has name or id of submit this method will mask the form's submit event, and instead submit given form.
    HTMLFormElement.prototype.submit.call(reviewForm);
});