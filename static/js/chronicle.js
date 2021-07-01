// Get the month from the hidden span element whose value is the month in the url
var monthInput = document.getElementById("month-in").attributes.value.value
var monthEle = document.getElementById("month")
monthEle.value = monthInput

var apiURL = "api?category=";

// Adds the selected month to the URL as a parameter
// The app will handle the routing and DB query
function updateSpecials(month) {
    window.location = `../chronicle?month=${month}`;
};

// Get the correct order of the specials for the Chronicle Ad
function getChronicleOrder(beer, wine, spirit) {
    var spec_order = [];
    spec_order.push(
        wine[0],
        spirit.slice(0,3),
        wine.slice(1,4),
        spirit.slice(3,6),
        wine.slice(4,7),
        spirit.slice(6,9),
        beer.slice(0,4),
        wine.slice(7,),
        spirit.slice(9,),
        beer.slice(4,)
    );
    return spec_order
}


// Drag & Drop Functionality
function allowDrop(ev) {
    ev.preventDefault();
}
  
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}
  
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}

async function getSpecials(month) {
    const beer = await fetch(`/api?category=beer&month=${month}`);
    const wine = await fetch(`/api?category=wine&month=${month}`);
    const spirit = await fetch(`/api?category=spirit&month=${month}`);
    const myJson = await beer.json();
    // do something with myJson
  }

function screenshot() {
    html2canvas(document.getElementById("ad-editor")).then(canvas => document.body.appendChild(canvas));
}