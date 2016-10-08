// Var


/*
--------------------------
--------------------------
 */
// Functions


function rgbToHex(red, green, blue) {
    var rgb = blue | (green << 8) | (red << 16);
    return '#' + (0x1000000 + rgb).toString(16).slice(1)
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function syncRGB(hex) {
    var rgb = hexToRgb(hex);

    $("#html-color-picker").val(hex);

    $("#square-visu").css("background-color", hex);

    $("#r-color-picker").val(rgb.r);
    $("#g-color-picker").val(rgb.g);
    $("#b-color-picker").val(rgb.b);

    //TODO if visu then send ajax

}

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



    $("#html-color-picker").on("input", function(){

        //TODO select bonne phase si besoin
        syncRGB($(this).val());
    });


    $(".rgb-picker").change(function () {
        var hex = rgbToHex($("#r-color-picker").val(), $("#g-color-picker").val(), $("#b-color-picker").val());
        syncRGB(hex);
    });


    $("#button-picker-ok").click(function () {
        var hex = $("#html-color-picker").val();
        var rgb = hexToRgb(hex);
        var num_phase = 1;
        if (num_phase > 0) {
            $(".r-display[data-phase-number=" + num_phase + "]").html(('000' + rgb.r).substr(-3));
            $(".g-display[data-phase-number=" + num_phase + "]").html(('000' + rgb.g).substr(-3));
            $(".b-display[data-phase-number=" + num_phase + "]").html(('000' + rgb.b).substr(-3));
        }
    });



});
