
//on click to a listen button, check if the track is in the playlist
//if it's in the playlist, just get the index and then pass it to play
//if it's not in the playlist, add it to the playlist, get the index, and then play it

//player.play(i) can be used to immediately play the file and everthing updates correctly

//eventually this just pulls from the database

var player = new Player([]);

//this and the playlist data api calls are going to merge, the data handlers that call it are identical
//with the single exception that they need to call a different endpoint
//the ids are unique, so I should be able to pass the configuration as an object
function get_track_data(track_id, callback){
    apiUrl = "/api/track/" + track_id;

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(track_data => {  //this is the callback function
        // Handle the JSON data (the track) here

        //build the playlist object

        const track_obj = {
            tr_id : track_data["id"],
            title: track_data["title"],
            file: track_data["audio_file_url"],
            howl: null
        };

        console.log("track data in AJAX function: ", track_data)
        callback(track_obj)
      })
      .catch(error => {
        console.error('Fetch error:', error);
      });

}

function get_playlist_data(track_id, callback){
    apiUrl = "/api/playlist/" + track_id;

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(track_data => {  //this is the callback function
        // Handle the JSON data (the track) here

        //build the playlist object

//        const track_obj = {
//            tr_id : track_data["id"],
//            title: track_data["title"],
//            file: track_data["audio_file_url"],
//            howl: null
//        };

        console.log("track data in AJAX function: ", track_data)
        callback(track_data)
      })
      .catch(error => {
        console.error('Fetch error:', error);
      });

}


//this whole bit of code might need to be scrapped
function init_player(playlist){
    //playlist must be an array
    if(!Array.isArray(playlist)){
        playlist = [playlist]
    }
    stop_player() //stop any track that may or may not be playing from continuing
    player.playlist = playlist
    console.log("init player: ", player.playlist)

    //the player dom elements are loaded into memory when player.js loads
    track.innerHTML = '1. ' + playlist[0]["title"];
    rebuild_playlist_html()
    player.skipTo(0) //unloads the currently playing track if there's one and starts playing the new one
}


function add_track_to_playlist(track_obj){
    const track_index = player.playlist.push(track_obj) - 1;
    rebuild_playlist_html();
    return track_index;

}

function stop_player(){
//there's a pause function built in, which needs to have a track loaded.
//This function should probably be folded into that prototype, but for now
//we are just going to do it this way.
    console.log("stop_player called")
    if(player.isAnyTrackPlaying()){
        console.log("A Track is loaded")
        player.unloadAllTracks()
    }
}



function rebuild_playlist_html(){
    //get the current playlist from the player
    var curr_playlist = player.playlist
    //console.log("rebuilding playlist HTML: ", curr_playlist)
    clear_playlist_html()

    //take the existing playlist and then build the html for it
    for (var i = 0; i < curr_playlist.length; i++){
        (function (index) {
              //console.log("iterating thru playlist : ", curr_playlist[index])
              update_playlist_html(curr_playlist[index], index);
        })(i);
    }
}


function update_playlist_html(track_obj, index){
    var playlist_track = document.createElement("div");
    playlist_track.className = "list-song";
    playlist_track.innerHTML = track_obj["title"]

    playlist_track.onclick = function(){
        player.skipTo(index);
    };
    list.append(playlist_track)
}


function clear_playlist_html(){
   //remove clear the HTML list
    while (list.firstChild){
        console.log("child left to be removed");
        list.removeChild(list.firstChild);
    }
}


function load_track(track_obj){
        console.log("load_track called with :", track_obj)
        var track_id = track_obj["tr_id"]
        var index = player.playlist.findIndex(audio_track => audio_track.tr_id === track_id)

        if(index == -1){
            //track is not in here.
            //check and see if the playlist is empty
            if (player.playlist.length == 0){
                //playlist is empty. initialize the player with our single track
                init_player(track_obj);
                player.skipTo(0);
            } // playlist isn't empty but our track isn't here. Add it and play it
            else{
                //player.pause()
                const appended_track = add_track_to_playlist(track_obj);
                player.skipTo(appended_track);
            }
        }
        else if (index !== -1){
            //track is already in the playlist. just play it.
            //check and see if it's currently loaded.
            current_track = player.getCurrentTrack();
            if(current_track.tr_id == track_id){
                //if it is just play it
                player.pause();
                player.play(index); // Plays the track object at the index
            }
            else{
                 //else skip to it
                 player.skipTo(index);
            }

        }

}


function track_button_handler(){
        trackButton = document.querySelector("button.track-button");
        if(trackButton){
            trackButton.addEventListener("click", function(){
            var track_id = this.getAttribute("data-track-id");
            console.log("track button handler fired: ", track_id);
            get_track_data(track_id, function(track_obj){
                console.log("track object from ajax: ", track_obj);
                //init_player(track_obj)
                load_track(track_obj);
            })
        });
   }
}

function playlist_button_handler() {
    playlistButton = document.querySelector("button.playlist-button");
    if (playlistButton) {
        playlistButton.addEventListener("click", function () {
            var playlistID = this.getAttribute("data-playlist-id");
            get_playlist_data(playlistID, function (playlist_obj) {
                console.log("playlist_object from ajax: ", playlist_obj);
                console.log(playlist_obj["track_details"]);
                track_playlist_obj = [];
                playlist_obj["track_details"].forEach((detail) => {
                    aj_trk = {
                        tr_id: detail["id"],
                        title: detail["title"],
                        file: detail["audio_file_url"],
                        howl: null,
                    };
                    track_playlist_obj.push(aj_trk);
                });

                //tracks (for now) auto clear the playlist and load in their place
                init_player(track_playlist_obj);
            });
        });
    }
}




document.addEventListener("DOMContentLoaded", track_button_handler)
document.addEventListener("DOMContentLoaded", playlist_button_handler)


//data_from_button = document.querySelector(".track-button")
//track_info_tag = document.querySelector("#track-info").attributes
//get_track_data(track_info_tag["data-track-id"].value)









