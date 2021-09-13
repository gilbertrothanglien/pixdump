const quantity = 6;
var load_more = true;
let counter = 1;


document.addEventListener('DOMContentLoaded', () => {
	var user_role = document.querySelector("#user_role").innerHTML;
	if(user_role == "Admin Owner Developer"){
		console.log("Found")
		document.querySelector("#user_role").style.color = "#FFFFFF";
		document.querySelector("#user_role").style.textShadow = "0 -1px 4px #FFF, 0 -2px 10px #ff0, 0 -10px 20px #ff8000, 0 -18px 40px #F00";
	}
	else if(user_role.indexOf("Admin") > -1){
		document.querySelector("#user_role").style.color = "#e0072b";
	}
	else if(user_role.indexOf("Member") > -1){
		document.querySelector("#user_role").style.color = "#3b82f5";
	}
	else if(user_role.indexOf("Elite") > -1){
		document.querySelector("#user_role").style.color = "#edd924";
	}

    $("#profile-user-posted").scroll(function() {
        if($(this).scrollTop() + $(this).height() >= $(this)[0].scrollHeight) {
            console.log('scrolled')
            load()
        }
     });
     load()
} )

function follow_user(user_id){
    fetch(`/follow_user/${user_id}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts)
    })
    var follow_status = document.querySelector("#follow_button").innerHTML;
    if(follow_status == "Follow"){
        document.querySelector("#follow_button").innerHTML = "Unfollow";
        var follow_amount = document.getElementById("followers").innerHTML;
        follow_amount = parseInt(follow_amount) + 1
        document.getElementById("followers").innerHTML = follow_amount;
    }
    else{
        document.querySelector("#follow_button").innerHTML = "Follow";
        var follow_amount = document.getElementById("followers").innerHTML;
        follow_amount = parseInt(follow_amount) - 1
        document.getElementById("followers").innerHTML = follow_amount;
    }
}

function load(){
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;
    var user_id = document.querySelector("#profile_id").value;
    console.log(`/posted_image/${user_id}?start=${start}&end=${end}`)
	fetch(`/posted_image/${user_id}?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(posts => {
    	console.log(posts)
        var main_content = document.getElementById("main-content");
        var content_loop = 0;
        var counter = 0;
        var second_loop = 3;
        if((posts.length % 3) != 0){
           var count = parseInt(posts.length / 3);
           content_loop = count + 1;
           second_loop = parseInt(posts.length / 3)
        }
        else{
            content_loop = parseInt(posts.length / 3);
        }
        for(var i = 0; i < content_loop; i++){
            var new_content = document.createElement("div");
            new_content.className = "wrap";
            
            for(var j = 0; j < 3; j++){
                if(counter+j < parseInt(posts.length)){
                    var second_new_content = document.createElement("div");
                    second_new_content.className = "tile";
                    second_new_content.innerHTML = `
                        <img src="/static/images/uploads/compressed_images/${posts[counter + j].main_image_name}"/>
                        <div class="text">
                          <h2 class="animate-text">${posts[counter + j].image_name}</h2>
                          <p class="animate-text">${posts[counter + j].image_description}</p>
                          <a href="/view_image/${posts[counter + j].id}"><button class="animate-text view-button">View</button></a>
                        </div>
                        `;
                    new_content.appendChild(second_new_content);
                }
            }
            counter = counter + 3;
            main_content.appendChild(new_content)
        }
    })
}