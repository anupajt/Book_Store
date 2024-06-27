// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}


    // Define a function to refresh the page
    function refreshPage() {
      location.reload(); // Reload the current page
    }

    // Set a timer to refresh the page every 30 seconds (adjust the time interval as needed)
    setTimeout(refreshPage, 30000); // 30,000 milliseconds = 30 seconds

