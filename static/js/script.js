/*
additional dynamic text fields - ingredients
*/
$(document).ready(function () {
    var max_ingredients = 15; //maximum input boxes allowed
    var wrapper_ingredients = $(".input_ingredients_wrap"); //Fields wrapper
    var add_ingredients_button = $(".add_ingredients_button"); //Add button ID

    var x = 1; //initlal text box count

    $(add_ingredients_button).click(function (e) { //on add input button click
        e.preventDefault();
        if (x < max_ingredients) { //max input box allowed
            //text box increment
            $(wrapper_ingredients).append('<div><input type="text" name="recipe_ingredient[]" id="recipe_ingredients" class="form-control mb-1" placeholder="Add Another Ingredient"/><a href="#" class="remove_ingredients btn btn-danger btn-sm"><i class="fa fa-trash"></i> remove</a></div>'); //add input box
            x++;
        }
        else {
            $(wrapper_ingredients).append('<p><small>That\'s a lot of ingredients are you sure you can\'t use less?</small></p>').css('color', 'red');
        }
    });

    $(wrapper_ingredients).on("click", ".remove_ingredients", function (e) { //user click on remove text

        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    })
});
/*
additional dynamic text fields - steps
*/
$(document).ready(function () {
    var max_steps = 10; //maximum input boxes allowed
    var wrapper_steps = $(".input_steps_wrap"); //Fields wrapper
    var add_steps_button = $(".add_steps_button"); //Add button ID

    var x = 1; //initlal text box count

    $(add_steps_button).click(function (e) { //on add input button click
        e.preventDefault();
        if (x < max_steps) { //max input box allowed
            //text box increment
            $(wrapper_steps).append('<div><input type="text" name="recipe_steps[]" id="recipe_steps" class="form-control mb-1" placeholder="Add Another Step"/><a href="#" class="remove_steps btn btn-danger btn-sm"><i class="fa fa-trash"></i> remove</a></div>'); //add input box
            x++;
        }
        else {
            $(wrapper_steps).append('<p><small>That\'s a lot of steps are you sure you can\'t use less?</small></p>').css('color', 'red');
        }
    });

    $(wrapper_steps).on("click", ".remove_steps", function (e) { //user click on remove text

        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    })
});

// matching passwords in registration form for validity check
$(document).ready(function () {
    $('#password-confirm').keyup(validate);
});

function validate() {
    var password = $('#password').val();
    var password_confirm = $('#password-confirm').val();

    if (password == password_confirm) {
        $("#validate-output").text("passwords are a match").css('color', 'green');
    }
    else {
        $("#validate-output").text("passwords do not match").css('color', 'red');
    }
}



// widget provided by https://rating-widget.com/get/rating/
// Ratings
(function (d, t, e, m) {

    // Async Rating-Widget initialization.
    window.RW_Async_Init = function () {

        RW.init({
            huid: "441979",
            uid: "15c790162584429bc0bfa9e00ac650d4",
            source: "website",
            options: {
                "advanced": {
                    "text": {
                        "rateThis": "rate this dish"
                    }
                },
                "size": "large",
                "type": "nero",
                "style": "thumbs",
                "isDummy": false
            }
        });
        RW.render();
    };

    // Append Rating-Widget JavaScript library.
    var rw, s = d.getElementsByTagName(e)[0], id = "rw-js",
        l = d.location, ck = "Y" + t.getFullYear() +
            "M" + t.getMonth() + "D" + t.getDate(), p = l.protocol,
        f = ((l.search.indexOf("DBG=") > -1) ? "" : ".min"),
        a = ("https:" == p ? "secure." + m + "js/" : "js." + m);

    if (d.getElementById(id))
        return;

    rw = d.createElement(e);

    rw.id = id; rw.async = true; rw.type = "text/javascript";

    rw.src = p + "//" + a + "external" + f + ".js?ck=" + ck;

    s.parentNode.insertBefore(rw, s);

}
    (document, new Date(), "script", "rating-widget.com/")
);