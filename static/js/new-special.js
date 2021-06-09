/*** Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    let forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})()
/*** End Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/


// Update available fields based on the category that is selected
function updateFields(category) {
    let fields = document.querySelectorAll(".field")
    Array.prototype.slice.call(fields)
        .forEach(field => {
            field.style.display = "none";
            field.classList.remove("active");
        });
    
    let fieldsOfSelected = document.querySelectorAll("."+category);
    Array.prototype.slice.call(fieldsOfSelected)
        .forEach(field => {
            field.style.display = "block";
            field.classList.add("active");
        });
};

/*** FOR BEER ***/
// Make sure either Bottles or Cans is selected at all times
function checkContainer(clicked) {
    let containerRadios = document.getElementsByClassName("container-type");
    let elementChecked = false;
    for(let radio of containerRadios) {
        if(radio.checked) {
            elementChecked = true;
            break;
        } 
    };
    if(!elementChecked) {
        let notClicked = clicked === "bottles" ? "cans" : "bottles";
        document.getElementById(notClicked).checked = true;
    }
}