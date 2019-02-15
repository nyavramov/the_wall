function test_javascript() {
    console.log("Javascript is running successfully!");
};

function send_post_request() {
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "http://localhost:5000/insert", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    var user_message = document.getElementById("submission_field").value;
    var the_wall     = document.getElementById("the_wall");
    var list_item    = document.createElement("li");
    var post_data    = JSON.stringify({ "user_message" : user_message });

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            list_item.innerHTML = user_message;
            the_wall.appendChild(list_item)
        }
    };
    
    xhttp.send(post_data);
}

window.onload = function () {
    var submit_button = document.getElementById("submit-button");
    
    submit_button.onclick = function() {
        send_post_request();
    };
};

test_javascript()