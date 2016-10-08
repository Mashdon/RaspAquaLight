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


    // TEST DE LA PROGRAMATION
    $("#btn-test").click(function(){
        $('#checkbox-visu').prop('checked', false);
        $("#checkbox-visu").trigger("change");

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

    // AJOUT DE PHASE
    $("#btn-add-phase").click(function () {
        $.ajax({
            url: '/GetNewPhase/' + 3,
            type: 'get',
            async: false,
            success: function (response) {
                $("#phases").append(response);
            },
            error: function () {
                alert("");
            }
        });

    });

    // SUPPRIMER UNE PHASE
    $('body').on("click", ".button-remove-phase", function () {
        var num_remove = $(this).attr("data-phase-number");

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


    $("#button-cancel-phase").click(function () {
        $.ajax({
            url: '/GetAllPhases',
            type: 'get',
            success: function (response) {
                $("#phases").html(response);
            },
            async: false
        });
    });


    $("#checkbox-visu").change(function () {
        if (this.checked){
            $("#panel-right").removeClass("panel-default").addClass("panel-danger");
            $("#panel-left").removeClass("panel-primary").addClass("panel-default");
        } else {
            $("#panel-left").removeClass("panel-default").addClass("panel-primary");
            $("#panel-right").removeClass("panel-danger").addClass("panel-default");
        }

    });
    $("#checkbox-visu").trigger("change");





});
