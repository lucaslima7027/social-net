// Check if edit button is clicked
function editPost() {
    document.querySelectorAll('#edit').forEach(element => {
        element.addEventListener('click', ()=>{
            element.style.display = 'none'
            const postId = element.dataset.id
            const post = document.querySelector(`#content${postId}`).innerHTML
            document.querySelector(`#content${postId}`).innerHTML = `
                                                            <textarea id="newContent" rows="5">${post}</textarea>
                                                            <button id="editPost">Submit</button>
                                                            `
            document.querySelector("#editPost").addEventListener('click', () => {
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const newContent = document.querySelector("#newContent").value
                var data = {id: postId,
                            content: newContent,
                        }
                data = JSON.stringify(data)
    
                fetch('/api/edit_post', {
                    method: 'PUT',
                    headers: {'X-CSRFToken': csrftoken,
                              'Content-Type': 'application/json'},
                    mode: 'same-origin',
                    body: data,
                })
                .then(response => {
                    fetch(`/api/post/${postId}`, {
                        method: 'GET',
                    })
                    .then(response => response.json())
                    .then(response => {
                        var data = response
                        document.querySelector(`#content${postId}`).innerHTML = data.post_content
                        document.querySelector(`#date${postId}`).innerHTML = data.post_date
                        element.style.display = 'inline'
                        fixTime()
                    })
                })
            })
        })
    })    
}


// Check if like button is clicked
document.querySelectorAll('#like').forEach(element => {
    element.addEventListener('click', ()=>{
        const postId = { id: element.dataset.id}
        const jsonData = JSON.stringify(postId)
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        //Send a HTTP PUT to update like number
        fetch('/api/like', {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken,
                      'Content-Type': 'application/json'},
            mode: 'same-origin',
            body: jsonData,
        })
        //Update the like number 
        .then(response => {
                    fetch(`/api/likes/${postId.id}`, {
                        method: 'GET',
                    })
                    .then(response => response.json())
                    .then(response => {
                        const postLikes = JSON.stringify(response)
                        selector = String(`#post${postId.id}`)
                        document.querySelector(selector).innerHTML = postLikes
                    })
        })
    })
})

// get date of the post and convert to local time
function fixTime() {
    document.querySelectorAll(".date").forEach(element => {
        const utcDate = element.innerHTML
        const date = new Date(utcDate);
        element.innerHTML = date.toLocaleString('default');
    });    
}

// Waypoint to load more posts
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onAfterPageLoad: function () {
        fixTime()
        editPost()
      }
  });


fixTime()
editPost()