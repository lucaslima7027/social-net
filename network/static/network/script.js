document.querySelectorAll('#like').forEach(element => {
    element.addEventListener('click', ()=>{
        const postId = { id: element.dataset.id}
        const jsonData = JSON.stringify(postId)
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/api/like', {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken,
                      'Content-Type': 'application/json'},
            mode: 'same-origin',
            body: jsonData,
        })
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
      }
  });


fixTime()