/*** Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    let forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(form => {
            if (form.classList.contains("active")) {
                form.addEventListener('submit', event => {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            }
        })
})()
/*** End Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/


// Update available fields based on the category that is selected
function updateFields(category) {
    // Turn off all fields
    let fields = document.querySelectorAll(".field")
    Array.prototype.slice.call(fields)
        .forEach(field => {
            field.style.display = "none";
            field.classList.remove("active");
        });
    
    // Only show fields that are an aspect of the chosen category
    let fieldsOfSelected = document.querySelectorAll("." + category);
    Array.prototype.slice.call(fieldsOfSelected)
        .forEach(field => {
            field.style.display = "block";
            field.classList.add("active");
        });
    // Update the background image for the WYSIWYG
    let itemImageEle = document.getElementById("item-image");
    let itemImageURLList = itemImageEle.src.split("/");
    let itemImageName = itemImageURLList[itemImageURLList.length-1];
    itemImageName === "stock.jpg" ? itemImageEle.src = `/static/img/specials/${category}/stock.jpg` : false;
};

/*** Show uploaded image code from https://jsfiddle.net/bootstrapious/8w7a50n2/ ***/
function readURL(input) {
    console.log(input);
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById("item-image").src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
}


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