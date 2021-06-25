// Adds the selected month to the URL as a parameter
// The app will handle the routing and DB query
function updateSpecials(month) {
    window.location = `../preview?month=${month}`;
};

// Receives the item's id that corresponds to the DB id
// Goes to the edit page with the id as a parameter
function editSpecial(id) {
    window.location = `../edit-special?id=${id}`;
};