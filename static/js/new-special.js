/*** Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/
/*** Changes made by Andrew Baker to fit the requirements ***/
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'
  
    // Fetch Special Form we want to apply custom Bootstrap validation styles to
    let forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(form => {
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

/*** Vue.js Code to dynamically populate the Preview Section ***/
var newSpecial = new Vue({
    el: '#new-special',
    data: {
        category: "beer",
        brand: "",
        product: "",
        xpack: "",
        volAmt: "",
        volUnit: "",
        containers: "",
        varietals: "",
        price: "",
        image: ""
    },
    computed: {
        imageURL() {
            let itemImageURL = document.getElementById("item-image").src;
            let itemImageURLList = itemImageURL.split("/");
            let itemImageName = itemImageURLList[itemImageURLList.length-1];
            return itemImageName === "stock.jpg" ? `/static/img/specials/${this.category}/stock.jpg` : itemImageURL;
        }
    },
    methods: {
        /*** Show uploaded image code from https://jsfiddle.net/bootstrapious/8w7a50n2/ ***/
        /*** Changes made by Andrew Baker to fit the requirements ***/
        readURL(event) {
            let itemImageURL = document.getElementById("item-image");
            if (event.target.files && event.target.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    itemImageURL.src = e.target.result;
                };
                reader.readAsDataURL(event.target.files[0]);
            } else {
                itemImageURL.src = `/static/img/specials/${newSpecial.category}/stock.jpg`;
            }
        }
        /*** End Show uploaded image code from https://jsfiddle.net/bootstrapious/8w7a50n2/ ***/
    },
    delimiters: ["[[ "," ]]"]
});