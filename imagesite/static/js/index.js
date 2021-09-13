let counter = 1;

const quantity = 9;

document.addEventListener('DOMContentLoaded', load);

var load_more = true;

$(window).scroll(function() {
   if($(window).scrollTop() + $(window).height() == $(document).height()) {
       console.log('loaded')
       load()     
   }
});


function like_image(image_id){
    image_id = parseInt(image_id)
    var current_class_name = document.querySelector(`#like_id_${image_id}`).className;
    if(current_class_name == "bx bxs-heart red"){
        document.querySelector(`#like_id_${image_id}`).className = "bx bx-heart";
    }
    else{
        document.querySelector(`#like_id_${image_id}`).className = "bx bxs-heart red";
    }
    fetch(`/like_image/${image_id}`)
    return false;
}
function load(bool){
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;
    fetch(`/posted_image/all?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts)
        if(posts.length == 6){
            load_more = true;
        }
        else{
            load_more = false;
        }
        if(bool == true){
            remove_skeleton()
        }
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
                    var like_button = `<i id="like_id_${posts[counter + j].id}" onclick="like_image(${posts[counter + j].id})" class='bx bx-heart' title="Like"></i>`;
                    var second_new_content = document.createElement("div");
                    second_new_content.className = "tile";
                    var image_location = `/static/images/profile_images/${posts[counter + j].image_location}`;
                    if(!posts[counter + j].image_location){
                        image_location = "https://st4.depositphotos.com/14953852/24787/v/600/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg";
                    } 
                    second_new_content.innerHTML = `
                        <img src="/static/images/uploads/compressed_images/${posts[counter + j].main_image_name}"/>
                        <a class="user-profile-link" href="user_profile/${posts[counter + j].uploader_id}">
                        <div class="user-profile">
                          <img src="${image_location}"/>
                          <h1>${posts[counter + j].upload_by}</h1>
                        </div>
                        </a>
                        <div class="text">
                          <h2 class="animate-text">${posts[counter + j].image_name}</h2>
                          <p class="animate-text">${posts[counter + j].image_description}</p>
                          <a href="/view_image/${posts[counter + j].id}"><button class="animate-text view-button">View</button></a>
                          
                        </div>
                        <div class="dots">
                            ${like_button}
                        </div>`;
                    new_content.appendChild(second_new_content);
                }
            }
            counter = counter + 3;
            main_content.appendChild(new_content)
        }
        for(var k=0; k < posts.length; k++){
            fetch(`/check_like/${posts[k].id}`)
            .then(response => response.json())
            .then(post => {
                if(post.image_liked >= 0){
                    document.querySelector(`#like_id_${post.image_liked}`).className = "bx bxs-heart red";
                }
            })
        }
    })
}

function skeleton(){
    var main_content = document.getElementById("main-content");
    var new_content = document.createElement('div');
    new_content.className = "wrap";
    new_content.setAttribute("id", 'skeleton')
    new_content.innerHTML = `
    <div class="skeleton-position">
    <div id="u_0_v">
      <div class="darkui1">
        <div class="darkui1-shimmer">
          <div class="_2iwr"></div>
          <div class="_2iws"></div>
          <div class="_2iwt"></div>
          <div class="_2iwu"></div>
          <div class="_2iwv"></div>
          <div class="_2iww"></div>
          <div class="_2iwx"></div>
          <div class="_2iwy"></div>
          <div class="_2iwz"></div>
          <div class="_2iw_"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="skeleton-position">
    <div id="u_0_v">
      <div class="darkui1">
        <div class="darkui1-shimmer">
          <div class="_2iwr"></div>
          <div class="_2iws"></div>
          <div class="_2iwt"></div>
          <div class="_2iwu"></div>
          <div class="_2iwv"></div>
          <div class="_2iww"></div>
          <div class="_2iwx"></div>
          <div class="_2iwy"></div>
          <div class="_2iwz"></div>
          <div class="_2iw_"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="skeleton-position">
    <div id="u_0_v">
      <div class="darkui1">
        <div class="darkui1-shimmer">
          <div class="_2iwr"></div>
          <div class="_2iws"></div>
          <div class="_2iwt"></div>
          <div class="_2iwu"></div>
          <div class="_2iwv"></div>
          <div class="_2iww"></div>
          <div class="_2iwx"></div>
          <div class="_2iwy"></div>
          <div class="_2iwz"></div>
          <div class="_2iw_"></div>
        </div>
      </div>
    </div>
  </div> `
  main_content.appendChild(new_content)
  load_more = false;

}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}