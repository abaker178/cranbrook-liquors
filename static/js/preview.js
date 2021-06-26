// Adds the selected month to the URL as a parameter
// The app will handle the routing and DB query
function updateSpecials(month) {
    window.location = `../preview?month=${month}`;
};