document.addEventListener('DOMContentLoaded', () => {
	var image_id = document.querySelector("#like").parentElement.id;
	console.log(image_id)
	fetch(`/check_like/${image_id}`)
    .then(response => response.json())
    .then(post => {
        if(post.image_liked >= 0){
            document.querySelector(`#like`).className = "bx bxs-heart red";
        }
    })

    var modal = document.getElementById("myModal");
    var span = document.getElementById("close");

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }
})

function like_image(image_id){
    image_id = parseInt(image_id)
    var current_class_name = document.querySelector(`#like`).className;
    if(current_class_name == "bx bxs-heart red"){
        document.querySelector(`#like`).className = "bx bx-heart";
        var likes = document.querySelector(`#like_no`).innerHTML;
        var newlikes = parseInt(likes) - 1;
        document.querySelector("#like_no").innerHTML = newlikes;
    }
    else{
        document.querySelector(`#like`).className = "bx bxs-heart red";
        var likes = document.querySelector(`#like_no`).innerHTML;
        var newlikes = parseInt(likes) + 1;
        document.querySelector("#like_no").innerHTML = newlikes;
    }
    fetch(`/like_image/${image_id}`)
    return false;
}

function add_comment(imageid){
    event.preventDefault()
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        `/comment_image`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        data: '{{csrf_token}}',
        body: JSON.stringify({
            comment: document.querySelector("#new-comment").value,
            image_id: imageid,
        })
    })
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    var comments = document.getElementById("posted_comments");
    var comment = document.getElementById("new-comment").value;
    var username = document.getElementById("username").innerHTML;
    var newcomment = document.createElement('div');
    newcomment.className = "comment-container";
    newcomment.innerHTML = `<div class='user-details'><a>${username}</a> <p class="comment-time" >${today}</p></div><div class='user-comment' >${comment}</div>`
    comments.insertBefore(newcomment, comments.childNodes[0]);
    document.getElementById("new-comment").value = '';
    
}

function load_comments(image_id) {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
    modal.style.animationName = "showcomment";
    fetch(`/get_comment/${image_id}`)
    .then(response => response.json())
    .then(comments => {
        document.getElementById("posted_comments").innerHTML = '';
        for(var i=0; i < comments.length; i++){
            var cTime = comments[i].comment_time.substring(0, 10)
            var comment = document.createElement('div')
            comment.className = "comment-container";
            comment.innerHTML = `<div class='user-details'><a href="/user_profile/${comments[i].commented_by_id}" >${comments[i].commented_by}  </a> <p class="comment-time" >${cTime}</p></div><div class='user-comment' >${comments[i].comment}</div>`
            document.getElementById("posted_comments").appendChild(comment);
        }
    })
}