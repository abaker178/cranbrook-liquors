// Get the month from the hidden span element whose value is the month in the url
var monthInput = document.getElementById("month-in").attributes.value.value
var monthEle = document.getElementById("month")
monthEle.value = monthInput

// Adds the selected month to the URL as a parameter
// The app will handle the routing and DB query
function updateSpecials(month) {
    window.location = `../preview?month=${month}`;
};

function confirmDelete(id, month, name) {
    if(window.confirm(`Are you sure you would like to delete special: ${name}`)) {
        window.location = `/delete-special?id=${id}&month=${month}`;
    } else {
        return false;
    }
};