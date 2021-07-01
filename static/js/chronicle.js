// Get the month from the hidden span element whose value is the month in the url
var monthInput = document.getElementById("month-in").attributes.value.value
var monthEle = document.getElementById("month")
monthEle.value = monthInput

// Adds the selected month to the URL as a parameter
// The app will handle the routing and DB query
function updateSpecials(month) {
    window.location = `../chronicle?month=${month}`;
};

// D3 for drag-n-drop editor
var apiURL = "api?category=";

var svg = d3.select("svg");
svg.append("use")
    .attr("href", "#pointer")
    .attr("x", 50)
    .attr("y", 50)
    .attr("fill", "#039BE5")
    .attr("stroke", "#039BE5")
    .attr("stroke-width", "1px");

var dragHandler = d3.drag()
    .on("drag", function () {
        d3.select(this)
            .attr("x", d3.event.x)
            .attr("y", d3.event.y);
    });
 
dragHandler(svg.selectAll("use"));

  