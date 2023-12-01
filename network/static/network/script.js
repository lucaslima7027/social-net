document.querySelectorAll(".date").forEach(element => {
    const utcDate = element.innerHTML
    const date = new Date(utcDate);
    element.innerHTML = date.toLocaleString('default');
});