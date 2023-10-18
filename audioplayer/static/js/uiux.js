const appContent = document.getElementById("app-content")

function get_django_content(endpoint){
    var url = endpoint + '?use_template=SPA';


    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type" : "text/html",
        },
    })
    .then((response) =>{
        if(!response.ok){
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log(response)
        return response.text();
    })
    .then((htmlContent) =>{
      appContent.innerHTML = htmlContent;
      //console.log(htmlContent)

      //brand new content is loaded. Lets re-attach the event listeners

      //track-button
      track_button_handler();
      //playlist-button
      playlist_button_handler();
      //internal urls
      preventAnchorDefault();
    })
    .catch((error) =>{
        console.error("Fetch error:", error);
    })
}





function preventAnchorDefault() {
  var anchorElements = document.querySelectorAll('a.internal-url');

  anchorElements.forEach(function(element) {
    element.addEventListener('click', function(event) {
      event.preventDefault();
      var href = this.getAttribute("href");
      console.log(href);
      get_django_content(href);
    });
  });
}


// Call the function initially when the page loads
preventAnchorDefault();



const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))


