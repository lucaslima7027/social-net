document.querySelectorAll(".date").forEach(element => {
    const utcDate = element.innerHTML
    const date = new Date(utcDate);
    element.innerHTML = date.toLocaleString('default');
});


var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0]
  });