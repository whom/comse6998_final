var favTopics = [];

function getRequestParameter(name) {
    if (name = (new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search)) {
        return decodeURIComponent(name[1]);
    }
}

function changeFavTopic(checkbox) {
    var index = favTopics.indexOf(checkbox.value);

    if (checkbox.checked) {
        //add to the list
        if (index === -1) {
            favTopics.push(checkbox.value);
        }
        backgroundlabel = checkbox.parentElement;
        backgroundlabel.className = "favtopic-checked";
        backgroundlabel.firstChild.className = "glyphicon glyphicon-star";
    } else {
        //remove from the list
        if (index > -1) {
            favTopics.splice(index, 1);
        }
        backgroundlabel = checkbox.parentElement;
        backgroundlabel.className = "favtopic-unchecked";
        backgroundlabel.firstChild.className = "glyphicon glyphicon-star-empty";
    }
}

function updateFavTopic() {
    if (favTopics.length === 0) {
        return;
    }

    var parameters = {"favtopics[]": favTopics, "id": getRequestParameter("id")};
    $.post("/LittUp/updatefavtopics/", parameters, function () {
        showSnackbar();
    });
}

function showSnackbar() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 3000);
}

