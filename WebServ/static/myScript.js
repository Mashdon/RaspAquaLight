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

    $('body').on("click", ".button-remove-phase", function () {
        var num_remove = $(this).attr("data-phase-number");

        //TODO ask confirmation

        $.ajax({
            url: '/RemovePhase',
            data: {
                num: num_remove
            },
            type: 'post',
            dataType: 'json'
        });

        $("div[data-phase-number=" + num_remove + "]").remove();

        $("div.div-phase").filter(function(){
            return $(this).attr("data-phase-number") > num_remove;

        }).each(function(){
            var new_num = $(this).attr("data-phase-number") - 1;

            $(this).attr("data-phase-number",new_num);
            $(this).find("strong.phase_number").html(new_num);
            $(this).find("[data-phase-number]").attr("data-phase-number", new_num);
        });
    });



});
