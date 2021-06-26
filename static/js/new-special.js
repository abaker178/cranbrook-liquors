/*** Vue.js Code to dynamically populate the Preview Section ***/
var newSpecial = new Vue({
    el: '#new-special',
    data: {
        errors: [],
        category: "beer",
        brand: "",
        product: "",
        volAmt: "",
        volUnit: "",
        price: "",
        month: "",
        xpack: "",
        container: "",
        varietals: ""
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
        },
        /*** End Show uploaded image code from https://jsfiddle.net/bootstrapious/8w7a50n2/ ***/

        /*** Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/
        /*** Changes made by Andrew Baker to fit the requirements ***/
        checkForm: event => {
            // Fetch Special Form we want to apply custom Bootstrap validation styles to
            let form = document.getElementById('special-form')
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }
        /*** End Form validation code from https://getbootstrap.com/docs/5.0/forms/validation/ ***/
    },
    delimiters: ["[[ "," ]]"]
});