function AfficherVideo(){
    var contentDiv = document.getElementById("contentDiv");
    var video = document.getElementById("displayVideo");

    contentDiv.style.display = "none";
    video.style.display = "block";
    video.setAttribute("autoplay", "");
    video.setAttribute("controls", "");
    

}