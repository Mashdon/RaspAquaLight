// Var


/*
--------------------------
--------------------------
 */
// Functions



/*
--------------------------
--------------------------
 */
// Main
$(function() {


    $("#btn-test").click(function(){

        var durationTest = $("#number-test").val();
        if (!isNaN(durationTest)){
            durationTest = Math.abs(parseInt(durationTest));
            $("#btn-test").attr("disabled", true);

            $.ajax({
                url: '/StartTest',
                data: {
                    duration: durationTest
                },
                type: 'post',
                dataType: 'json'
            });

            setTimeout(function() {
                $("#btn-test").attr("disabled", false);
            }, (durationTest + 1) * 1000);

        }
    });

    $("#btn-add-phase").click(function () {
        $.ajax({
            url: '/AddPhase',
            type: 'post',
            async: false,
            success: function (response) {
                $("#phases").append(response);
            },
            error: function () {
                alert("bouh");
            }
        });

    });



});
